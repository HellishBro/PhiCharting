from fractions import Fraction

class Note:
    def __init__(self, type: int, x: float, time: tuple | float, end_time: tuple | float=None, fake=False, alpha=255, upscroll=False, size=1, speed=1, visible_time=999_999, y_offset=0):
        self.type = type
        self.x = x
        self.time = time[0] + time[1] / time[2] if isinstance(time, (tuple, list)) else time
        self.end_time = (end_time[0] + end_time[1] / end_time[2] if isinstance(time, (tuple, list)) else end_time) if end_time else self.time
        self.fake = fake
        self.alpha = alpha
        self.above = 2 if upscroll else 1
        self.size = size
        self.speed = speed
        self.visible_time = visible_time
        self.y_offset = y_offset

    def to_json(self):
        start_time = Fraction(self.time).limit_denominator(1000)
        end_time = Fraction(self.end_time).limit_denominator(1000)
        return {
            "type": self.type,
            "positionX": self.x,
            "startTime": (start_time.numerator // start_time.denominator, start_time.numerator % start_time.denominator, start_time.denominator),
            "endTime": (end_time.numerator // end_time.denominator, end_time.numerator % end_time.denominator, end_time.denominator),
            "above": self.above,
            "alpha": self.alpha,
            "size": self.size,
            "speed": self.speed,
            "isFake": int(self.fake),
            "visibleTime": self.visible_time,
            "yOffset": self.y_offset
        }

    @classmethod
    def from_json(cls, json):
        return cls(
            json["type"],
            json["positionX"],
            json["startTime"],
            json["endTime"],
            bool(json["isFake"]),
            json["alpha"],
            True if json["above"] == 2 else False,
            json["size"],
            json["speed"],
            json["visibleTime"],
            json["yOffset"]
        )

class Tap(Note):
    def __init__(self, x: float, time: tuple | float, fake=False, alpha=255, upscroll=False, size=1, speed=1, visible_time=999_999, y_offset=0):
        super().__init__(1, x, time, time, fake, alpha, upscroll, size, speed, visible_time, y_offset)

    def __repr__(self):
        return f"Tap(x={self.x!r}, time={self.time!r}, fake={self.fake!r}, alpha={self.alpha!r})"

class Drag(Note):
    def __init__(self, x: float, time: tuple | float, fake=False, alpha=255, upscroll=False, size=1, speed=1, visible_time=999_999, y_offset=0):
        super().__init__(4, x, time, time, fake, alpha, upscroll, size, speed, visible_time, y_offset)

    def __repr__(self):
        return f"Drag(x={self.x!r}, time={self.time!r}, fake={self.fake!r}, alpha={self.alpha!r})"

class Flick(Note):
    def __init__(self, x: float, time: tuple | float, fake=False, alpha=255, upscroll=False, size=1, speed=1, visible_time=999_999, y_offset=0):
        super().__init__(3, x, time, time, fake, alpha, upscroll, size, speed, visible_time, y_offset)

    def __repr__(self):
        return f"Flick(x={self.x!r}, time={self.time!r}, fake={self.fake!r}, alpha={self.alpha!r})"

class Hold(Note):
    def __init__(self, x: float, time: tuple | float, end_time: tuple | float, fake=False, alpha=255, upscroll=False, size=1, speed=1, visible_time=999_999, y_offset=0):
        super().__init__(2, x, time, end_time, fake, alpha, upscroll, size, speed, visible_time, y_offset)

    def __repr__(self):
        return f"Hold(x={self.x!r}, start_time={self.time!r}, end_time={self.end_time!r}, fake={self.fake!r}, alpha={self.alpha!r})"
