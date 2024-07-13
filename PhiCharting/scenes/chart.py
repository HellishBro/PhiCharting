import pygame as pg

from .base import Scene
from PhiCharting.components.song_list import Song
from PhiCharting.utils import *
from PhiCharting import phigros as phi
from .chart_view import ChartView

import json

class Chart(Scene):
    def __init__(self, song: Song):
        super().__init__()
        self.song = song
        self.song_path = song.song_path
        self.name = song.song_name
        self.difficulty = song.level
        self.thumbnail = pg.image.load(song.thumbnail_path)
        with open(song.chart_path, encoding="utf-8") as f:
            self.chart = phi.Chart.from_json(json.loads(f.read()))

        factor = 0.75
        self.view_window = pg.Window("Chart View", (1350 * factor, 900 * factor))
        self.window_sc = self.view_window.get_surface()
        self.chart_view = ChartView(self)

        self.active_line_index = 0
        self.active_line = self.chart.lines[self.active_line_index]

    def load_line(self, index):
        self.active_line_index = 0
        self.active_line = self.chart.lines[self.active_line_index]

    def update(self, dt: float):
        Super(dt)
        self.chart_view.update(dt)

    def draw(self, sc: pg.Surface):
        self.chart_view.draw(self.window_sc)
        self.view_window.flip()

        Super(sc)
        #for i, line in enumerate(self.chart_view.chart_render.chart.lines):
        #    y = 100 * i + 50
        #    sc.blit(text(f"Line #{i}: \"{line.name}\"", 24, (255, 255,255)), (50, y))
        #    sc.blit(text(f"X: {round(line.x, 5)}, Y: {round(line.y, 5)}. Rot: {round(line.rotation, 5)}, A: {round(line.alpha, 5)}, S: {round(line.speed, 5)}", 20, (255, 255, 255)), (50, y + 30))

    def event(self, ev: pg.Event):
        if not Super(ev): return

        if hasattr(ev, "window") and hasattr(ev.window, "id"):
            if ev.window.id == self.view_window.id:
                self.chart_view.event(ev)
                return

        if self.chart_view.mouse_on:
            self.chart_view.event(ev)
            return

    def click(self, ev: pg.Event, pos: tuple):
        if ev.window == self.view_window:
            self.chart_view.click(ev, pos)
            return
