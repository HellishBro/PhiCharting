from pytweening import *

IN = 1
OUT = 2
IN_OUT = 3
ANY = 4

class Easing:
    def __init__(self, name: str, function, easing_type: int=ANY):
        self.name = name
        self.function = function
        self.easing_type = easing_type
        self.time = 0

    def __call__(self, time: float, start: float, end: float) -> float:
        return self.function(min(time, 1.0)) * (end - start) + start


EASE = [
    Easing("Linear", linear),

    Easing("Sine", easeOutSine, OUT),
    Easing("Sine", easeInSine, IN),
    Easing("Sine", easeInOutSine, IN_OUT),

    Easing("Quad", easeOutQuad, OUT),
    Easing("Quad", easeOutQuad, IN),
    Easing("Quad", easeInOutQuad, IN_OUT),

    Easing("Cubic", easeOutCubic, OUT),
    Easing("Cubic", easeInCubic, IN),
    Easing("Cubic", easeInOutCubic, IN_OUT),

    Easing("Quart", easeOutQuart, OUT),
    Easing("Quart", easeInQuart, IN),
    Easing("Quart", easeInOutQuart, IN_OUT),

    Easing("Quint", easeOutQuint, OUT),
    Easing("Quint", easeInQuint, IN),
    Easing("Quint", easeInOutQuint, IN_OUT),

    Easing("Expo", easeOutExpo, OUT),
    Easing("Expo", easeInExpo, IN),
    Easing("Expo", easeInOutExpo, IN_OUT),

    Easing("Circ", easeOutCirc, OUT),
    Easing("Circ", easeInCirc, IN),
    Easing("Circ", easeInOutCirc, IN_OUT),

    Easing("Back", easeOutBack, OUT),
    Easing("Back", easeInBack, IN),
    Easing("Back", easeInOutBack, IN_OUT),

    Easing("Elastic", easeOutElastic, OUT),
    Easing("Elastic", easeInElastic, IN),
    Easing("Elastic", easeInOutElastic, IN_OUT),

    Easing("Bounce", easeOutBounce, OUT),
    Easing("Bounce", easeInBounce, IN),
    Easing("Bounce", easeInOutBounce, IN_OUT)
]