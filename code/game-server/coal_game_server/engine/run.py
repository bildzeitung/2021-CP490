import attr

import coal_game_server.engine.conditions as conditions
import coal_game_server.engine.actions as actions
from coal_game_server.models.game import EventConditionFalseItem

from ..models import GameEvent, EventConditionItem

@attr.s
class GameCommand:
    game_id = attr.ib()
    character_id = attr.ib()
    command = attr.ib()
    buffer = attr.ib(init=False, default=[])
    _status = attr.ib(init=False, default="OK")

    @property
    def result(self):
        self._run()

        return {
            "status": self._status,
            "game_id": self.game_id,
            "character_id": self.character_id,
            "text": self.text,
            "command": "self.command",
        }

    @property
    def text(self):
        return "\n".join(self.buffer)

    def _run(self):
        # reset
        self.buffer = []

        # parse command

        # execute filter-match event

        # execute no-pattern (global) events
        global_events = GameEvent().query.filter(GameEvent.command == "")
        g : GameEvent
        for g in global_events:
            print(f"XXX Processing... {g.id}")
            if self._applies(g):
                print("TODO: run true part")
            else:
                self._run_false_part(g.false_part)

    def _applies(self, event : GameEvent):
        c : EventConditionItem
        return all( 
            getattr(conditions, c.primitive.replace("-", "_"))(self, *[x.title for x in c.arguments]) for c in event.conditions
        )

    def _run_false_part(self, event):
        f : EventConditionFalseItem
        for f in event:
            arguments = [a.title for a in f.arguments]
            getattr(actions, f.primitive.replace("-", "_"))(self, *arguments)
