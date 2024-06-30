import pygame as pg
from abc import abstractmethod

class Scene:

    # noinspection PyTypeChecker
    def __init__(self):
        self.switch_scene = None
        self.switch_scene_args = ()
        self.tooltip: pg.Surface = None
        self.tooltip_of = None

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, sc: pg.Surface):
        pass

    @abstractmethod
    def event(self, ev: pg.Event):
        if ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.click(ev, pg.mouse.get_pos())
                return False

    @abstractmethod
    def click(self, ev: pg.Event, pos: tuple):
        pass