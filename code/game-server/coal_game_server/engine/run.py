import attr

import coal_game_server.engine.conditions as conditions
import coal_game_server.engine.actions as actions
from coal_game_server.models.game import EventConditionFalseItem, EventConditionTrueItem

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

        m = self._filter_match()
        if m:
            self._run_filter_match(m)

        # execute no-pattern (global) events
        global_events = GameEvent().query.filter(GameEvent.command == "")
        g : GameEvent
        for g in global_events:
            if self._applies(g):
                self._run_true_part(g.true_part)
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

    def _run_true_part(self, event):
        f : EventConditionTrueItem
        for f in event:
            arguments = [a.title for a in f.arguments]
            getattr(actions, f.primitive.replace("-", "_"))(self, *arguments)

    def _filter_match(self):
        # do not process anything if there's no command
        if not self.command:
            return

        all_events = {g.id: g for g in GameEvent().query.filter(GameEvent.command != "")}
        events = { x.id: x.command.split() for x in all_events.values() }
        elements = [x.strip() for x in self.command.split()]

        idx = 0
        while elements and events:
            p = elements.pop(0)
            events = {k : v for k, v in events.items() if len(v) > idx and p == v[idx]}
            print("YYY", p, events)
            idx += 1
        
        if not events:
            self.buffer.append(f"Sorry, I don't understand you. elements: {elements} {events}")
            self._status = "ERROR"
            return

        if len(events) > 1:
            self.buffer.append("That could mean so many things.")
            self._status = "ERROR"
            return
        
        print("ZZZ", elements, events)

        # events is now constrained to exactly one elements, so run that
        self._status = "OK"
        return all_events[list(events)[0]]

    def _run_filter_match(self, event : GameEvent):
        if self._applies(event):
            self._run_true_part(event.true_part)
        else:
            self._run_true_part(event.false_part)