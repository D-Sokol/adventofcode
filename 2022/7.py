#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List, Dict, Optional, Iterator
from functools import cached_property

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


@dataclass
class Dir:
  files: Dict[str, int]
  dirs: Dict[str, 'Dir']
  parent: Optional['Dir'] = None

  @cached_property
  def total_size(self) -> int:
    return sum(self.files.values()) + sum(d.total_size for d in self.dirs.values())

  def walk(self) -> Iterator['Dir']:
    yield self
    for d in self.dirs.values():
      yield from d.walk()


pwd: List[str] = None
root = current = Dir({}, {})

for line in sys.stdin:
  if line.startswith('$'):
    _, cmd, *args = line.split()
    assert cmd in {"ls", "cd"}
    if cmd == "cd":
      assert len(args) == 1
      arg, = args
      if arg == "/":
        pwd = []
        current = root
      elif arg == "..":
        pwd.pop()
        current = current.parent or root
      else:
        pwd.append(arg)
        current = current.dirs[arg]
    elif cmd == "ls":
      assert not args
  else:
    # Processing `ls` output
    size, name = line.split()
    if size == "dir":
      current.dirs[name] = new_dir = Dir({}, {})
      new_dir.parent = current
    else:
      current.files[name] = int(size)

if EASY:
  result = sum(d.total_size for d in root.walk() if d.total_size <= 100_000)
else:
  space_required = root.total_size - 40000000
  dir_to_remove = min(
    (
      d
      for d in root.walk()
      if d.total_size >= space_required
    ),
    key=lambda d: d.total_size
  )
  result = dir_to_remove.total_size

print(result)
