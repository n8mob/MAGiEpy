import time

import adafruit_pcf8574
import board
import busio

INIT_WAIT = 0.005
WRITE_WAIT = 0.002
I2C_1 = 1

ROW_OFFSETS = [0x00, 0x40, 0x14, 0x54]


class BetterLcd:
  def __init__(self, address=0x27, light_on=True):
    """bus = smbus2.SMBus(1)

    (not sure if 1 is always the right answer. or what it even means)
    """
    i2c = busio.I2C(board.GP1, board.GP0)
    self.bus_adapter = adafruit_pcf8574.PCF8574(i2c, address)
    self.address = address
    self.light_on = light_on

    self.send_command(0x33)
    time.sleep(INIT_WAIT)
    self.send_command(0x32)
    time.sleep(INIT_WAIT)
    self.send_command(0x28)
    time.sleep(INIT_WAIT)
    self.send_command(0x0C)
    time.sleep(INIT_WAIT)
    self.send_command(0x01)

  def write_word(self, buffer):
    temp = buffer
    if self.light_on == 1:
      temp |= 0x08
    else:
      temp &= 0xF7
    self.bus_adapter.write_gpio(temp)

  def send_command(self, command):
    buffer = command & 0xF0
    buffer |= 0x04
    self.write_word(buffer)
    time.sleep(WRITE_WAIT)
    buffer &= 0xFB
    self.write_word(buffer)

    buffer = (command & 0x0F) << 4
    buffer |= 0x04
    self.write_word(buffer)
    time.sleep(0.002)
    buffer &= 0xFB
    self.write_word(buffer)

  def send_data(self, data):
    if isinstance(data, str):
      data = ord(data[0])

    buffer = data & 0xF0
    buffer |= 0x05
    self.write_word(buffer)
    time.sleep(WRITE_WAIT)
    buffer &= 0xFB
    self.write_word(buffer)

    buffer = (data & 0x0F) << 4
    buffer |= 0x05
    self.write_word(buffer)
    time.sleep(WRITE_WAIT)
    buffer &= 0xFB
    self.write_word(buffer)

  def clear(self):
    self.send_command(0x01)

  def open_light(self):
    self.bus_adapter.write_gpio(0x08)

  def write(self, x, y, message):
    if x < 0:
      x = 0
    if x > 19:
      x = 19

    if y < 0:
      y = 0
    if y > 3:
      y = 3

    message_address = 0x80 + ROW_OFFSETS[y]
    self.send_command(message_address)

    for c in message:
      self.send_data(ord(c))

  def write_line(self, row_index, message, blip=0.1, message_index=0):
    char_address = 0x80 + ROW_OFFSETS[row_index]

    while message_index < min(20, len(message)):
      self.send_command(char_address)
      self.send_data(message[message_index])
      message_index += 1
      char_address += 1
      time.sleep(blip)


if __name__ == '__main__':
  lcd = BetterLcd(0x27, 1)
  lcd.write(0, 0, "Hello, world,")
  lcd.write(0, 1, "I'm LCD driver!")
  lcd.write(0, 3, "  HACK THE PLANET!!")
