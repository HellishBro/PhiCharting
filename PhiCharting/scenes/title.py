import pygame as pg

from .base import Scene
from PhiCharting.components import *
from PhiCharting.utils import *
from PhiCharting.config import Config

class Title(Scene):
    def __init__(self):
        super().__init__()
        screen_size = Config.instance().get("screen_size")
        self.go_button = self.add_component(Button((
            screen_size[0] - 325, screen_size[1] - 125
        ), (300, 100), text("Start Charting", 40, (255, 255, 255)), "Start charting this song!", self.start_charting))
        self.new_button = self.add_component(Button((
            screen_size[0] - 325, screen_size[1] - 225
        ), (300, 100), text("New Chart", 40, (255, 255, 255)), "Create a new chart!", self.new_chart))
        self.song_list = self.add_component(SongList((30, 30), (700, screen_size[1])))
        self.thumbnail_center = Vec(800, 30)

    def start_charting(self, button: Button):
        self.switch_scene = "Chart"
        self.switch_scene_args = (self.song_list.songs[self.song_list.selected_song], )

    def new_chart(self, button: Button):
        self.switch_scene = 'NewChart'

    def draw(self, sc: pg.Surface):
        sc.blit(self.song_list.song_thumbnail_blur, to_blit_center(self.song_list.song_thumbnail_blur, sc))
        
        Super(sc)

        sc.blit(self.song_list.song_thumbnail_blur_400x400, self.thumbnail_center ())
        sc.blit(self.song_list.song_thumbnail, (self.thumbnail_center + to_blit_center(self.song_list.song_thumbnail, pg.Rect(0, 0, 400, 400))) ())

    def event(self, ev: pg.Event):
        Super(ev)

    def click(self, ev: pg.Event, pos: tuple[int]):
        pass

    def update(self, dt: float):
        Super(dt)