#!/usr/bin/env python3
import sys
import numpy as np
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



def rotated(x: np.ndarray, step: int = 0) -> np.ndarray:
  assert x.ndim == 2
  assert step in range(4)
  if step == 0:
    return x
  elif step == 1:
    return x[:, ::-1]
  elif step == 2:
    return x.T
  else:
    return x.T[:, ::-1]


def count_visible(x: np.ndarray) -> np.ndarray:
  assert x.ndim == 1 and x.size > 0
  is_visible = np.ones_like(x, dtype=bool)
  # 3 3 5 4 9  --> 3 3 5 5 9
  highest = np.maximum.accumulate(x)
  is_visible[1:] = x[1:] > highest[:-1]
  return is_visible


data = []
for line in sys.stdin:
  line = line.strip()
  line = list(map(int, line))
  data.append(line)


data = np.array(data)
log(data, end='\n\n')
if EASY:
  is_visible = np.zeros_like(data, dtype=bool)
else:
  n_visibles = np.zeros((4, *data.shape), dtype=int)

# One step for each direction
for step in range(4):
  data_view = rotated(data, step)
  if EASY:
    is_visible_view = rotated(is_visible, step)
    for row, visible_row in zip(data_view, is_visible_view):
      visible_row |= count_visible(row)
    log(is_visible, end='\n\n\n')
  else:
    n_visibles_view = rotated(n_visibles[step], step)
    for i in range(data_view.shape[0]):
      for j in range(data_view.shape[1]):
        log(i, j, data_view[i, j:], count_visible(data_view[i, j:]))
        n_visibles_view[i, j] = count_visible(data_view[i, j:]).sum()  # FIXME: maybe off by 1
    log(n_visibles[step])


if EASY:
  result = is_visible.sum()
else:
  result = n_visibles.prod(axis=0).max()

print(result)

