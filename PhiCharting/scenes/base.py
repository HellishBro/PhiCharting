import pygame as pg
from abc import abstractmethod
from PhiCharting.components.base import Component
from PhiCharting.components.tooltipped import Tooltipped

class Scene:

    # noinspection PyTypeChecker
    def __init__(self):
        self.switch_scene = None
        self.switch_scene_args = ()
        self.tooltip: pg.Surface = None
        self.tooltip_of = None

        self.components = []

    def add_component[CompT: Component](self, component: CompT) -> CompT:
        if isinstance(component, Tooltipped):
            component.set_scene(self)
        self.components.append(component)
        return component

    def update(self, dt: float):
        for component in self.components:
            component.update(dt)

    def draw(self, sc: pg.Surface):
        for component in self.components:
            component.draw(sc)

    def event(self, ev: pg.Event):
        for component in self.components:
            component.event(ev)

        if ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.click(ev, pg.mouse.get_pos())
                return False
        return True

    @abstractmethod
    def click(self, ev: pg.Event, pos: tuple):
        pass