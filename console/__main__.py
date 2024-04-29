import argparse

import requests
from urllib3.util import parse_url
import os

from console.console_magie import ConsoleMAGiE
from game import Game
from magie_model import Menu


def start_game(json_path=None, json_content=None):
  if json_path and os.path.exists(json_path):
    with open(json_path, encoding='utf-8') as menu_file:
      menu = Menu(file=menu_file)
  else:
    menu = Menu(deserialized=json_content)

  magie = ConsoleMAGiE()

  game = Game(menu, magie)
  game.run()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('menu_location')
  args = parser.parse_args()
  parsed_url = parse_url(args.menu_location)
  if parsed_url.scheme in ['http', 'https']:
    response = requests.get(parsed_url)
    menu_json = response.json()
    start_game(json_content=menu_json)
  elif os.path.exists(parsed_url.path):
    start_game(json_path=parsed_url.path)
  else:
    raise FileNotFoundError(f"Can't figure out how to open {parsed_url}")
