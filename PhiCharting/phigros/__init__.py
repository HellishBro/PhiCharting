from .layers import Event, EventLayer, ExtendedEvents
from .line import Line
from .note import Note, Tap, Drag, Flick, Hold
from .easing import EASE, Easing

class BPMTiming:
    def __init__(self, time: tuple, bpm: float):
        self.time = time
        self.bpm = bpm

    def __repr__(self):
        return f"BPMTiming(time={self.time!r}, bpm={self.bpm!r})"

class Chart:
    def __init__(self, bpm_list: list[BPMTiming], lines: list[Line]):
        self.bpm_list = bpm_list
        self.lines = lines

    def __repr__(self):
        return f"Chart(bpm_list={self.bpm_list!r}, lines={self.lines!r})"

    def to_json(self, **meta):
        d = {
            "BPMList": [{"bpm": timing.bpm, "startTime": timing.time} for timing in self.bpm_list],
            "META": {
                "program": "PhiCharting",
                "offset": 0
            },
            "judgeLineList": [line.to_json() for line in self.lines]
        }
        for k, v in meta.items():
            d["META"][k] = v

        return d

    @classmethod
    def from_json(cls, json):
        return cls(
            [BPMTiming(timing["startTime"], timing["bpm"]) for timing in json["BPMList"]],
            [Line.from_json(line) for line in json["judgeLineList"]]
        )

if __name__ == "__main__":
    import json
    chart = Chart([BPMTiming((0, 0, 1), 178)], [
        Line([
            Tap(-100, (2, 0, 1)),
            Tap(-75, (2, 0, 1), True),
            Tap(0, (4, 0, 1)),
            Tap(-25, (4, 0, 1), True),
            Tap(25, (4, 0, 1), True),
            Tap(100, (6, 0, 1)),
            Tap(75, (6, 0, 1), True)
        ], events=[
            EventLayer([], [
                Event(1, 0, -250, (0, 0, 1), (4, 0, 1))
            ], [
                Event(1, 0, 255, (0, 0, 1), (4, 0, 1))
            ], [], [
                Event(1, 10, 10, (0, 0, 1), (1, 0, 1))
            ])
        ])
    ])
    print(chart)
    print(json.dumps(chart.to_json()))
