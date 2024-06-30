import pygame as pg
from typing import Callable, Union

class Component:
    def __init__(self, position: tuple, size: tuple, active=True, visible=True):
        self.parent: Union['Component', None] = None
        self.children: list['Component'] = []
        self.active = active
        self.visible = visible

        self.position = [*position]
        self.size = [*size]
        self.rect = pg.Rect(self.position, self.size)

    def update(self, dt: float):
        self.rect = pg.Rect(self.position, self.size)
        if not self.active:
            return

        for child in self.children:
            child.update(dt)
        return True

    def draw(self, sc: pg.Surface):
        if not self.visible:
            return

        for child in self.children:
            child.draw(sc)
        return True

    def event(self, ev: pg.Event):
        if not self.active:
            return
        if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
            self.click(ev, pg.mouse.get_pos())
            return

        for child in self.children:
            child.event(ev)
        return True

    def click(self, ev: pg.Event, pos: tuple):
        if not self.active:
            return
        if not self.rect.collidepoint(pos):
            return

        for child in self.children:
            child.click(ev, pos)
        return True

    def add_child(self, component: 'Component'):
        component.attach(self)
        self.children.append(component)

    def remove_child(self, component: 'Component'):
        component.detach()
        self.children.remove(component)

    def attach(self, parent: 'Component'):
        self.parent = parent

    def detach(self):
        self.parent = None

    def locate_child(self, predicate: Callable[['Component'], bool]):
        t = []
        for child in self.children:
            if predicate(child):
                t.append(child)

        return t
