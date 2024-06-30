import pygame as pg

from .base import Scene
from PhiCharting.components import *
from PhiCharting.components.song_list import Song
from PhiCharting.utils import *
from PhiCharting.config import Config

class ChartView(Scene):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def update(self, dt: float):
        pass

    def draw(self, sc: pg.Surface):
        pg.draw.line(sc, (255, 0, 255), (0, 100), (100, 0))
        pg.draw.circle(sc, (255, 0, 0), (100, 100), 10)

    def event(self, ev: pg.Event):
        if not super().event(ev): return

    def click(self, ev: pg.Event, pos: tuple):
        print(pos)
