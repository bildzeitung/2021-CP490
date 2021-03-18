import attr

@attr.s
class State:
  game = attr.ib(default=None)
  player = attr.ib(default=None)
  character = attr.ib(default=None)