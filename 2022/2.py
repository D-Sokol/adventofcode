#!/usr/bin/env python3
import sys
from enum import Enum, auto


# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False


class Sign(Enum):
  rock = auto()
  paper = auto()
  scissors = auto()
  
  def against(self, other):
    if not isinstance(other, Sign):
      return NotImplemented

    if self == other:
      return 3
    elif (self, other) in {(Sign.rock, Sign.scissors), (Sign.scissors, Sign.paper), (Sign.paper, Sign.rock)}:
      return 6
    return 0


def result(r1, r2) -> int:
  assert r1 in set("ABC")
  assert r2 in set("XYZ")
  
  s1 = {"A": Sign.rock, "B": Sign.paper, "C": Sign.scissors}[r1]
  if EASY:
    s2 = {"X": Sign.rock, "Y": Sign.paper, "Z": Sign.scissors}[r2]
  else:
    target_score = dict(X=0, Y=3, Z=6)[r2]
    s2 = next(s for s in Sign if s.against(s1) == target_score)

  shape_cost = {Sign.rock: 1, Sign.paper: 2, Sign.scissors: 3}[s2]
  result_cost = s2.against(s1)
  return shape_cost + result_cost


score = 0
for line in sys.stdin:
    r1, r2 = line.split()
    score += result(r1, r2)


print(score)

