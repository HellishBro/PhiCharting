from .note import Note
from .event import Event

class Line:
    def __init__(self, notes: list[Note], name="Line", texture="line.png", parent=-1, events: list[Event]=None):
        self.notes = notes
        self.name = name
        self.texture = texture
        self.parent = parent
        self.events = events if events else []

        self.x = 0
        self.y = 0
        self.rotation = 0
        self.alpha = 0
        self.speed = 10

    def __repr__(self):
        return f"Line(notes={self.notes!r}, name={self.name!r}, texture={self.texture!r}, parent={self.parent!r}, events={self.events!r})"

    def to_json(self):
        return {
            "name": self.name,
            "texture": self.texture,
            "events": [event.to_json() for event in self.events],
            "parent": self.parent,
            "notes": [note.to_json() for note in self.notes]
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            [Note.from_json(note) for note in json["notes"]] if "notes" in json else [],
            json["name"],
            json["texture"],
            json["parent"],
            [Event.from_json(layer) for layer in json["events"]]
        )