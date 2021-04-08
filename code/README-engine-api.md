# Coal Game Engine API

## Example JSON
For example, consider the following JSON fragment:

```
[
  {
    "command": "",
    "conditions": [
        {"primitive": "has-key", "arguments": ["character", "first-turn"]}
    ],
    "true_part": [],
    "false_part": [
      {"primitive": "set-key",  "arguments": ["character", "first-turn", "true"]},
      {"primitive": "message",  "arguments": ["game", "starting-message"]},
      {"primitive": "set-room", "arguments": ["game", "starting-room"]}
    ]
  },
  ...
```
This is _one_ event. There is no _command_, which means that the event is run every turn. The _condition_ checks to see if the character has a certain attribute. If so, then nothing happens, as there are no actions in the _true\_part_.

On the other hand, if the character does not have the _first-turn_ key, then three (3) actions are run. The first sets the _first-turn_ to the value _"true"_. The second sends a message (found in the _game_ attributes) back to the user. The last transports the character to the room given in the _game_'s _starting-room_ attribute.


## Format
All Engine API functions consist of:

`<name> <arguments>`

Where the `<name>` is the text in the _primitive_ field and shown in this document.

The `<arguments>` specify what the function should use or operate on. Arguments consist of a set of: `object`, `key`, and `value`. An `object` is one of: `game`, `character`, `room`, or `item`. A `key` is the name of an object attribute. A `value` is a text string.

A `value` text string may be a _variable reference_. That is, if a command has a variable: `GO !DIRECTION`, then a `value` can be `!DIRECTION`. Whatever the user entered for `!DIRECTION` will be used by the primitive.

## Conditions
Events use conditions to decide what to do. If the `object` is `game` or `character`, then it's in the context of the _current game_ and the _player character that is acting_. If the `object` is `item`, then _which_ item needs to be specified in a 3rd `title` argument.

| Primitive          | Arguments                 | Description                                                  |
|-------------------:|---------------------------|:-------------------------------------------------------------|
| is-equal           | object, title, key, value | True if `object[title][key]` == `value`                      |
| is-gt              | object, title, key, value | True if `object[title][key]` & `object[title][key]` > `value`|
| is-lt              | object, title, key, value | True if `object[title][key]` & `object[title][key]` < `value`|
| obj-loc-is-equal   | object, title, value      | True if `object[title]` location == `value`                  |


## Actions
Actions alter game state and send messages back to the player.

| Primitive          | Arguments                 | Description                                                  |
|-------------------:|---------------------------|:-------------------------------------------------------------|
| look               |                           | send room description to the user                            |
| message            | object, title, key        | send text from `object[title][key]` to the user              |
| go                 | object, title, key        | move character to `object[title][key]`                       |
| set-key            | object, title, key, value | set `object[title][key] <- value`                            |
| mv-item-to-char    | title                     | move `item[title]` to character's inventory                  |
| mv-item-to-room    | title1, title2            | move `item[title2]` to `room[title1]`                        |
| inventory          |                           | list items located with the character (and not in a room)    |
| dec                | object, title, key        | `object[title][key]` <- `object[title][key]` - 1             |
| inc                | object, title, key        | `object[title][key]` <- `object[title][key]` + 1             |