from pytweening import *

IN = 1
OUT = 2
IN_OUT = 3
ANY = 4

class Easing:
    def __init__(self, name: str, function, easing_type: int=ANY, RPE_incompatible=False):
        self.name = name
        self.function = function
        self.easing_type = easing_type
        self.RPE_incompatible = RPE_incompatible
        self.time = 0

    def __call__(self, time: float, start: float, end: float) -> float:
        return self.function(min(time, 1.0)) * (end - start) + start


EASE = {
     0: Easing("Instant", lambda n: 1, RPE_incompatible=True),
     1: Easing("Linear", linear),
######## SINE
     2: Easing("Sine", easeOutSine, OUT),
     3: Easing("Sine", easeInSine, IN),
     6: Easing("Sine", easeInOutSine, IN_OUT),
######## QUAD
     4: Easing("Quad", easeOutQuad, OUT),
     5: Easing("Quad", easeOutQuad, IN),
     7: Easing("Quad", easeInOutQuad, IN_OUT),
######## CUBIC
     8: Easing("Cubic", easeOutCubic, OUT),
     9: Easing("Cubic", easeInCubic, IN),
    12: Easing("Cubic", easeInOutCubic, IN_OUT),
######## QUART
    10: Easing("Quart", easeOutQuart, OUT),
    11: Easing("Quart", easeInQuart, IN),
    13: Easing("Quart", easeInOutQuart, IN_OUT),
######## QUINT
    14: Easing("Quint", easeOutQuint, OUT),
    15: Easing("Quint", easeInQuint, IN),
    -1: Easing("Quint", easeInOutQuint, IN_OUT, True),
######## EXPO
    16: Easing("Expo", easeOutExpo, OUT),
    17: Easing("Expo", easeInExpo, IN),
    -2: Easing("Expo", easeInOutExpo, IN_OUT, True),
######## CIRC
    18: Easing("Circ", easeOutCirc, OUT),
    19: Easing("Circ", easeInCirc, IN),
    22: Easing("Circ", easeInOutCirc, IN_OUT),
######## BACK
    20: Easing("Back", easeOutBack, OUT),
    21: Easing("Back", easeInBack, IN),
    23: Easing("Back", easeInOutBack, IN_OUT),
######## ELASTIC
    24: Easing("Elastic", easeOutElastic, OUT),
    25: Easing("Elastic", easeInElastic, IN),
    -3: Easing("Elastic", easeInOutElastic, IN_OUT, True),
######## BOUNCE
    26: Easing("Bounce", easeOutBounce, OUT),
    27: Easing("Bounce", easeInBounce, IN),
    28: Easing("Bounce", easeInOutBounce, IN_OUT)
}