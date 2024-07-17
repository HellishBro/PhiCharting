from .event import Event, Property
from .line import Line
from .note import Note, NoteType
from .easing import EASE, Easing

class BPMTiming:
    def __init__(self, time: float, bpm: float):
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
            "BPM": [[bpm.bpm, bpm.time] for bpm in self.bpm_list],
            "meta": {},
            "lines": [line.to_json() for line in self.lines]
        }
        for k, v in meta.items():
            d["meta"][k] = v

        return d

    @classmethod
    def from_json(cls, json):
        return cls(
            [BPMTiming(timing[1], timing[0]) for timing in json["BPM"]],
            [Line.from_json(line) for line in json["lines"]]
        )

if __name__ == "__main__":
    import json
    chart = Chart([BPMTiming(0, 200)], [
        Line([
            Note(NoteType.TAP, 0, 3),
            Note(NoteType.DRAG, 10, 3.1)
        ], "Line 0", events=[
            Event(Property.ALPHA, EASE[0], 0, 255, 0, 2),
            Event(Property.Y, EASE[3], 0, -300, 1, 2)
        ])
    ])
    print(chart)
    print(json.dumps(chart.to_json()))
