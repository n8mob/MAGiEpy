#!/usr/bin/env python3

import time

import better_lcd_2004

SHORT_PAUSE = 0.06
PAUSE = 0.16
LONG_PAUSE = 1.8


def show_n(start, n):
  s = ''
  for c in range(start, start + n):
    s += chr(c)
  return s


if __name__ == '__main__':
  better_lcd = better_lcd_2004.BetterLcd(0x27, True)

  better_lcd.write(0, 0, '  Hello  from')
  time.sleep(PAUSE)
  better_lcd.write(0, 1, '  the LCD of')
  time.sleep(PAUSE)
  better_lcd.write(0, 2, '    KC7III  ')
  time.sleep(LONG_PAUSE)
  better_lcd.clear()
  time.sleep(PAUSE)
  better_lcd.write_line(1, '   HACK THE PLANET!', blip=0.03)
  time.sleep(LONG_PAUSE)
  better_lcd.write_line(2, ' HACK THE PLANET!', blip=0.13)
  time.sleep(LONG_PAUSE)
  better_lcd.clear()
  time.sleep(LONG_PAUSE)
  better_lcd.write_line(0, 'Knock, knock, Neo.')
  time.sleep(LONG_PAUSE)
  time.sleep(LONG_PAUSE)
  better_lcd.light_on = False
  better_lcd.write(0, 0, 'Knock, knock, Neo.')
  time.sleep(LONG_PAUSE)
  better_lcd.clear()
