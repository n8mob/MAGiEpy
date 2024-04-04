import time

import board
import digitalio
import audioio

BLINK_TIME = 0.4

if __name__ == '__main__':
  print('hello, console!')
  led = digitalio.DigitalInOut(board.LED)
  led.switch_to_output()

  audioOut = audioio.AudioOut()

  while True:
    led.value = True
    audioOut.play(tone1, loop=True)
    time.sleep(BLINK_TIME)
    led.value = False
    audioOut.stop()
    time.sleep(BLINK_TIME)

