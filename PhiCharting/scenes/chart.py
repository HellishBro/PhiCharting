import pygame as pg

from .base import Scene
from PhiCharting.components import *
from PhiCharting.components.song_list import Song
from .chart_view import ChartView
from PhiCharting.utils import *
from PhiCharting.config import Config

class Chart(Scene):
    def __init__(self, song: Song):
        super().__init__()
        self.song = song
        self.view_window = pg.Window("Chart View")
        self.window_sc = self.view_window.get_surface()
        self.chart_view = ChartView(self)

    def update(self, dt: float):
        self.chart_view.update(dt)

    def draw_window(self):
        sc = self.window_sc
        self.window_sc.fill((0, 0, 0))



        self.view_window.flip()

    def draw(self, sc: pg.Surface):
        self.window_sc.fill((0, 0, 0))
        self.chart_view.draw(self.window_sc)
        self.view_window.flip()

        pg.draw.line(sc, (255, 0, 255), (0, 100), (100, 0))

    def event(self, ev: pg.Event):
        if not super().event(ev): return

        if ev.window == self.view_window:
            self.chart_view.event(ev)
            return

    def click(self, ev: pg.Event, pos: tuple):
        if ev.window == self.view_window:
            self.chart_view.click(ev, pos)
            return
