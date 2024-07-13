from .easing import EASE
from fractions import Fraction

class Event:
    def __init__(self, easing_type: int, start: float, end: float, start_time: tuple | float, end_time: tuple | float):
        self.easing_type = easing_type
        self.start = start
        self.end = end
        self.start_time = start_time[0] + start_time[1] / start_time[2] if isinstance(start_time, (tuple, list)) else start_time
        self.end_time = end_time[0] + end_time[1] / end_time[2] if isinstance(end_time, (tuple, list)) else end_time

        # Set during render
        self.time = 0
        self.duration = -1

    def ease(self) -> float:
        return EASE[self.easing_type](self.time / self.duration, self.start, self.end)

    def __repr__(self):
        return f"Event(easing_type={self.easing_type!r}, start={self.start!r}, start_time={self.start_time!r}, end={self.end!r}, end_time={self.end_time!r})"

    def to_json(self):
        start = Fraction(self.start_time).limit_denominator(1000)
        end = Fraction(self.end_time).limit_denominator(1000)
        return {
            "easingType": self.easing_type,
            "start": self.start,
            "end": self.end,
            "startTime": (start.numerator // start.denominator, start.numerator % start.denominator, start.denominator),
            "endTime": (end.numerator // end.denominator, end.numerator % end.denominator, end.denominator),
            "easingLeft": 0,
            "easingRight": 1,
            "bezier": 0,
            "bezierPoints": [0, 0, 0, 0]
        }

    @classmethod
    def from_json(cls, json):
        return cls(json["easingType"] if "easingType" in json else 1, json["start"], json["end"], json["startTime"], json["endTime"])

class EventLayer:
    def __init__(self, move_x: list[Event], move_y: list[Event], alpha: list[Event], rotate: list[Event], speed: list[Event]):
        self.move_x = move_x if move_x else [Event(1, 0, 0, (0, 0, 1), (1, 0, 1))]
        self.move_y = move_y if move_y else [Event(1, 0, 0, (0, 0, 1), (1, 0, 1))]
        self.alpha = alpha if alpha else [Event(1, 0, 0, (0, 0, 1), (1, 0, 1))]
        self.rotate = rotate if rotate else [Event(1, 0, 0, (0, 0, 1), (1, 0, 1))]
        self.speed = speed if speed else [Event(1, 10, 10, (0, 0, 1), (1, 0, 1))]

        self.curr_x = 0
        self.curr_y = 0
        self.curr_alpha = 0
        self.curr_rotate = 0
        self.curr_speed = 0

    def __repr__(self):
        return f"EventLayer(move_x={self.move_x!r}, move_y={self.move_y!r}, alpha={self.alpha!r}, rotate={self.rotate}, speed={self.speed})"

    def to_json(self):
        return {
            "moveXEvents": [event.to_json() for event in self.move_x],
            "moveYEvents": [event.to_json() for event in self.move_y],
            "alphaEvents": [event.to_json() for event in self.alpha],
            "rotateEvents": [event.to_json() for event in self.rotate],
            "speedEvents": [event.to_json() for event in self.speed]
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            [Event.from_json(event) for event in json["moveXEvents"]] if "moveXEvents" in json else [],
            [Event.from_json(event) for event in json["moveYEvents"]] if "moveYEvents" in json else [],
            [Event.from_json(event) for event in json["alphaEvents"]] if "alphaEvents" in json else [],
            [Event.from_json(event) for event in json["rotateEvents"]] if "rotateEvents" in json else [],
            [Event.from_json(event) for event in json["speedEvents"]] if "speedEvents" in json else [],
        )

class ExtendedEvents:
    def __init__(self, color: list[Event], text: list[Event], scale_x: list[Event], scale_y: list[Event], incline: list[Event], paint: list[Event]):
        self.color = color
        self.text = text
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.incline = incline
        self.paint = paint

    def __repr__(self):
        return f"ExtendedEvents(color={self.color!r}, text={self.text!r}, scale_x={self.scale_x!r}, scale_y={self.scale_y!r}, incline={self.incline!r}, paint={self.paint!r})"

    def to_json(self):
        d = {}
        if self.color:
            d["colorEvents"] = [event.to_json() for event in self.color]
        if self.text:
            d["textEvents"] = [event.to_json() for event in self.text]
        if self.scale_x:
            d["scaleXEvents"] = [event.to_json() for event in self.scale_x]
        if self.scale_y:
            d["scaleYEvents"] = [event.to_json() for event in self.scale_y]
        if self.incline:
            d["inclineEvents"] = [event.to_json() for event in self.incline]
        if self.paint:
            d["paintEvents"] = [event.to_json() for event in self.paint]
        return d

    @classmethod
    def from_json(cls, json):
        return cls(
            [Event.from_json(event) for event in json["colorEvents"]] if "colorEvents" in json else [],
            [Event.from_json(event) for event in json["textEvents"]] if "textEvents" in json else [],
            [Event.from_json(event) for event in json["scaleXEvents"]] if "scaleXEvents" in json else [],
            [Event.from_json(event) for event in json["scaleYEvents"]] if "scaleYEvents" in json else [],
            [Event.from_json(event) for event in json["inclineEvents"]] if "inclineEvents" in json else [],
            [Event.from_json(event) for event in json["paintEvents"]] if "paintEvents" in json else []
        )