class NoteType:
    TAP = 0
    DRAG = 1
    FLICK = 2
    HOLD = 3

class Note:
    def __init__(self, type: int, x: float, time: float, end_time: float=None, fake=False, alpha=255, downscroll=True, speed=1):
        self.type = type
        self.x = x
        self.time = time
        self.end_time = end_time if end_time else self.time
        self.fake = fake
        self.alpha = alpha
        self.downscroll = downscroll
        self.speed = speed

    def to_json(self):
        return {
            "type": self.type,
            "x": self.x,
            "time": self.time,
            "end_time": self.end_time,
            "downscroll": self.downscroll,
            "alpha": self.alpha,
            "speed": self.speed,
            "fake": self.fake
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            json["type"],
            json["x"],
            json["time"],
            json["end_time"],
            json["fake"],
            json["alpha"],
            json["downscroll"],
            json["speed"],
        )
