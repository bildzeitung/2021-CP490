import attr

@attr.s
class State:
  game = attr.ib(default=None)