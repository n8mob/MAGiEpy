import os
import sys

sys.path.append(os.path.expanduser('~/c/DFRobot_RGB1602_RaspberryPi/python'))
import rgb1602
import time

if __name__ == '__main__':
  lines = [
    'one',
    'two',
    'three',
    'four'
  ]

  prev_line = ''

  lcd = rgb1602.RGB1602(16, 2)

  for line in lines:
    lcd.setCursor(0, 0)
    lcd.printout(prev_line)
    lcd.setCursor(0, 1)
    lcd.printout(line)
    prev_line = line
    time.sleep(0.5)
