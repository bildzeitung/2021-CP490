import attr

@attr.s
class GameCommand:
  game_id = attr.ib()
  character_id = attr.ib()
  command = attr.ib()
  _status = attr.ib(init=False, default=None)
  _text = attr.ib(init=False, default=None)

  @property
  def result(self):
    if not (self._status and self._text):
      self._run()

    return {
      "status": self.status,
      "game_id": self.game_id,
      "character_id": self.character_id,
      "text": self.text,
    }

  @property
  def status(self):
    return self._status

  @property
  def text(self):
    return self._text

  def _run():
    # parse command

    # execute filter-match event

    # execute no-pattern (global) events

    # set result
    pass