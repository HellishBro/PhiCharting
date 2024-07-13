import pygame as pg

from .base import Scene
from PhiCharting.components import *
from PhiCharting.components.chart_render import ChartRender
from PhiCharting.utils import *
from PhiCharting.config import Config

class ChartView(Scene):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mouse_on = False
        self.chart_render = ChartRender((0, 0), self.parent.window_sc.get_size(), self.parent.chart, self.parent.song.path)
        self.thumbnail = pg.image.load(self.parent.song.thumbnail_path).convert_alpha()
        self.thumbnail = pg.transform.scale_by(self.thumbnail, self.parent.window_sc.get_height() / self.thumbnail.get_height())
        self.black = pg.Surface(self.thumbnail.get_size())
        self.thumbnail = pg.transform.gaussian_blur(self.thumbnail, 10)
        self.black.set_alpha(127)
        self.thumbnail.blit(self.black, (0, 0))
        self.thumbnail_x = (self.parent.window_sc.get_width() - self.thumbnail.get_width()) / 2
        self.thumbnail_fit = pg.transform.smoothscale(self.thumbnail, self.parent.window_sc.get_size())
        self.thumbnail_fit = pg.transform.gaussian_blur(self.thumbnail_fit, 50)

        self.song = self.parent.song.song_path
        pg.mixer.music.load(self.song)
        self.song_played = False

    def update(self, dt: float):
        Super(dt)
        self.chart_render.update(dt)

    def draw(self, sc: pg.Surface):
        Super(sc)
        sc.blit(self.thumbnail_fit, (0, 0))
        sc.blit(self.thumbnail, (self.thumbnail_x, 0))
        self.chart_render.draw(sc)

    def event(self, ev: pg.Event):
        if not Super(ev): return
        if ev.type == pg.WINDOWENTER:
            self.mouse_on = True
        elif ev.type == pg.WINDOWLEAVE:
            self.mouse_on = False

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_SPACE:
                self.chart_render.playing = not self.chart_render.playing
                if self.chart_render.playing:
                    print("Playing")
                    if self.song_played:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.play()
                        self.song_played = True
                else:
                    print("Paused")
                    pg.mixer.music.pause()

            elif ev.key == pg.K_LEFT:
                self.chart_render.time -= 5
                self.chart_render.time = max(self.chart_render.time, 0)
                pg.mixer.music.play(start=self.chart_render.time)

            elif ev.key == pg.K_RIGHT:
                self.chart_render.time += 5
                pg.mixer.music.play(start=self.chart_render.time)

    def click(self, ev: pg.Event, pos: tuple):
        pass
