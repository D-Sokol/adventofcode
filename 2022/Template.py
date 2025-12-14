#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--easy', action='store_true', dest="easy")
group.add_argument('--hard', action='store_false', dest="easy", default=False)
group = parser.add_mutually_exclusive_group()
group.add_argument('--debug', action='store_true', dest="debug")
group.add_argument('--real', action='store_false', dest="debug", default=False)
args = parser.parse_args()
EASY = args.easy
DEBUG = args.debug


def log(*args, **kwargs):
  if DEBUG:
    print(*args, **kwargs)


data = []
for line in sys.stdin:
  line = line.strip()
  # line = int(line)
  data.append(line)


result = len(data)

print(result)

