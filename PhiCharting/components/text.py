import pygame as pg
from .base import Component
from PhiCharting.utils import *

class Text(Component):
    def __init__(self, position: tuple, content: str, font_size: int, color: pg.Color | tuple, background: pg.Color | tuple=None, italic=False):
        self.text = text(content, font_size, color, background, italic)
        super().__init__(position, self.text.get_size())

    def draw(self, sc: pg.Surface):
        if not super().draw(sc):
            return

        sc.blit(self.text, self.position)
