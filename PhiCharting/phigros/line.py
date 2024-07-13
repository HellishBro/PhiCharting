from .note import Note
from .layers import EventLayer, ExtendedEvents

class Line:
    def __init__(self, notes: list[Note], name="Line", texture="line.png", parent=-1, events: list[EventLayer]=None, extended: ExtendedEvents=None):
        self.notes = notes
        self.name = name
        self.texture = texture
        self.parent = parent
        self.events = events if events else [EventLayer([], [], [], [], [])] * 4
        self.extended = extended if extended else ExtendedEvents([], [], [], [], [], [])

        self.x = 0
        self.y = 0
        self.rotation = 0
        self.alpha = 0
        self.speed = 10

        print("==========")
        for ev in self.events:
            print(ev) # debug be like

    def __repr__(self):
        return f"Line(notes={self.notes!r}, name={self.name!r}, texture={self.texture!r}, parent={self.parent!r}, events={self.events!r}, extended={self.extended!r})"

    def to_json(self):
        return {
            "Group": 0,
            "Name": self.name,
            "Texture": self.texture,
            "eventLayers": [layer.to_json() for layer in self.events],
            "extended": self.extended.to_json(),
            "father": self.parent, # smh RPE u gotta up ur english game
            "notes": [note.to_json() for note in self.notes],
            "isCover": 0,
            "alphaControl": [
                {"alpha": 1, "easing": 1, "x": 0},
                {"alpha": 1, "easing": 1, "x": 9_999_999}
            ], # idk why this is here
            "posControl": [
                {"pos": 1, "easing": 1, "x": 0},
                {"pos": 1, "easing": 1, "x": 9_999_999}
            ], # idk why this is here also
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            [Note.from_json(note) for note in json["notes"]] if "notes" in json else [],
            json["Name"],
            json["Texture"],
            json["father"],
            [EventLayer.from_json(layer) for layer in json["eventLayers"]],
            ExtendedEvents.from_json(json["extended"])
        )