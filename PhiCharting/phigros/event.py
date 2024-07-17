from .easing import EASE

class Property:
    X = 0
    Y = 1
    ALPHA = 2
    ROTATION = 3
    SPEED = 4

class Event:
    def __init__(self, property: int, easing_type: int, start: float, end: float, start_time: float, end_time: float):
        self.property = property
        self.easing_type = easing_type
        self.start = start
        self.end = end
        self.start_time = start_time
        self.end_time = end_time

        # Set during render
        self.time = 0
        self.duration = -1

    def ease(self) -> float:
        return EASE[self.easing_type](self.time / self.duration, self.start, self.end)

    def __repr__(self):
        return f"Event(property={self.property!r}, easing_type={self.easing_type!r}, start={self.start!r}, start_time={self.start_time!r}, end={self.end!r}, end_time={self.end_time!r})"

    def to_json(self):
        return {
            "property": self.property,
            "easing": self.easing_type,
            "start": self.start,
            "end": self.end,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            json["property"],
            json["easing"],
            json["start"],
            json["end"],
            json["start_time"],
            json["end_time"]
        )
