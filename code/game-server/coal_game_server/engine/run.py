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
    varmap = attr.ib(default={})
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

    @property
    def tokens(self):
        return [x.strip() for x in self.command.split()]

    def _run(self):
        # reset
        self.buffer = []

        m = self._filter_match()
        if m:
            self._run_filter_match(m)

        # execute no-pattern (global) events
        global_events = GameEvent().query.filter(GameEvent.command == "")
        g: GameEvent
        for g in global_events:
            if self._applies(g):
                self._run_true_part(g.true_part)
            else:
                self._run_false_part(g.false_part)

    def _applies(self, event: GameEvent):

        return all(
            getattr(conditions, c.primitive.replace("-", "_"))(
                self,
                *[
                    self.varmap[a.title] if a.title.startswith("!") else a.title
                    for a in c.arguments
                ],
            )
            for c in event.conditions
        )

    def _run_false_part(self, event):
        f: EventConditionFalseItem
        for f in event:
            arguments = [
                self.varmap[a.title] if a.title.startswith("!") else a.title
                for a in f.arguments
            ]
            getattr(actions, f.primitive.replace("-", "_"))(self, *arguments)

    def _run_true_part(self, event):
        f: EventConditionTrueItem
        for f in event:
            arguments = [
                self.varmap[a.title] if a.title.startswith("!") else a.title
                for a in f.arguments
            ]
            getattr(actions, f.primitive.replace("-", "_"))(self, *arguments)

    def _filter_match(self):
        # do not process anything if there's no command
        if not self.command:
            return

        all_events = {
            g.id: g for g in GameEvent().query.filter(GameEvent.command != "")
        }
        events = {x.id: x.command.split() for x in all_events.values()}

        # only use events with the same number of tokens
        events = {k: v for k, v in events.items() if len(v) == len(self.tokens)}

        # sort out a list of candidate rules
        for i in range(len(self.tokens)):
            if not events:
                self._status = "ERROR"
                self.buffer.append("Sorry, I don't understand you.")
                return

            events = {
                k: v
                for k, v in events.items()
                if self.tokens[i] == v[i] or v[i].startswith("!")
            }

        # no matches left, so we don't know what the player wants
        if not events:
            self._status = "ERROR"
            self.buffer.append("Sorry, I don't think I know what you want.")
            return

        # there's room for ambiguity between variables and special cases
        for i in range(len(self.tokens)):
            # if there's exactly one match -- we're done
            if len(events) == 1:
                self._status = "OK"
                return all_events[list(events)[0]]

            # disambiguation is to prefer special cases over variables
            keeplist = {k: v for k, v in events.items() if self.tokens[i] == v[i]}
            if keeplist:
                events = keeplist

        # final check
        if len(events) == 1:
            self._status = "OK"
            return all_events[list(events)[0]]

        self._status = "ERROR"
        self.buffer.append(
            f"That could mean so much. I don't know what to do. {events}"
        )

    def _resolve_vars(self, event: GameEvent):
        self.varmap = {
            x: self.tokens[i]
            for i, x in enumerate(event.command.split())
            if x.startswith("!")
        }

    def _run_filter_match(self, event: GameEvent):
        self._resolve_vars(event)
        if self._applies(event):
            self._run_true_part(event.true_part)
        else:
            self._run_true_part(event.false_part)
