import time

import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

while True:
  led.value = True
  time.sleep(1)
  led.value = False
  time.sleep(1)
