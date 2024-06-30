import pygame as pg
from .base import Component
from .tooltipped import Tooltipped
from PhiCharting.utils import *
from PhiCharting.config import Config

class Button(Component, Tooltipped):
    # noinspection PyTypeChecker
    def __init__(self, position: tuple, size: tuple, image: pg.Surface, tooltip: str=None, callback=None, render_background=True):
        super().__init__(position, size)
        self.image = image
        self.callback = callback
        self.render_background = render_background
        self.show_tooltip = False
        self.press = False

        self.border = pg.Surface(size)
        button_scale = min(4, size[0] / 32)
        top_left = load_img("button_topleft", button_scale)
        left = load_img("button_left", button_scale)
        bottom_left = load_img("button_bottomleft", button_scale)
        bottom = load_img("button_bottom", button_scale)
        bottom_right = load_img("button_bottomright", button_scale)
        right = load_img("button_right", button_scale)
        top_right = load_img("button_topright", button_scale)
        top = load_img("button_top", button_scale)
        middle = load_img("button_middle", button_scale)
        self.border.blit(top_left, (0, 0))
        self.border.blit(top_right, (size[0] - top_right.get_width(), 0))
        self.border.blit(bottom_left, (0, size[1] - bottom_left.get_height()))
        self.border.blit(bottom_right, (size[0] - bottom_right.get_width(), size[1] - bottom_left.get_height()))
        self.border.blit(
            scale(top, (size[0] - top_right.get_width() - top_left.get_width(), top.get_height())),
            (top_left.get_width(), 0))
        self.border.blit(
            scale(left, (left.get_width(), size[1] - bottom_left.get_height() - top_left.get_height())),
            (0, top_left.get_height()))
        self.border.blit(
            scale(bottom, (size[0] - bottom_right.get_width() - bottom_left.get_width(), bottom.get_height())),
            (bottom_left.get_width(), size[1] - bottom_left.get_height()))
        self.border.blit(
            scale(right, (right.get_width(), size[1] - bottom_right.get_height() - top_right.get_height())),
            (size[0] - top_right.get_width(), top_right.get_height()))
        self.border.blit(
            scale(middle, (size[0] - top_right.get_width() - top_left.get_width(), size[1] - bottom_left.get_height() - top_left.get_height())),
            (top_right.get_width(), top_left.get_height()))

        self.dark = pg.Surface(size, flags=pg.SRCALPHA)
        self.dark.fill((0, 0, 0))
        self.dark.set_alpha(125)

        self.light = pg.Surface(size, flags=pg.SRCALPHA)
        self.light.fill((255, 255, 255))
        self.light.set_alpha(50)

        self.tooltip = tooltip
        self.tooltip_image: pg.Surface = None
        self.generate_tooltip(tooltip)

        self.hold_time = 0
        self.disable = False

    def generate_tooltip(self, tooltip):
        self.tooltip = tooltip
        tooltip_text = text(str(tooltip), 20, (255, 255, 255))
        self.tooltip_image = pg.Surface((tooltip_text.get_width() + 8, tooltip_text.get_height() + 8))
        self.tooltip_image.fill((0, 0, 0))
        self.tooltip_image.blit(tooltip_text, (4, 4))

    def update(self, dt: float):
        if not super().update(dt):
            return

        pos = pg.mouse.get_pos()
        self.show_tooltip = self.rect.collidepoint(pos) and (self.tooltip is not None)
        if self.rect.collidepoint(pos) and self.press:
            self.hold_time += dt
        else:
            self.hold_time = 0

    def click(self, ev: pg.Event, pos: tuple):
        if not super().click(ev, pos):
            return

        self.press = True

    def event(self, ev: pg.Event):
        if not super().event(ev):
            return

        if ev.type == pg.MOUSEBUTTONUP and ev.button == 1 and self.press:
            self.press = False
            if self.rect.collidepoint(pg.mouse.get_pos()) and self.callback:
                self.callback(self)

    def draw(self, sc: pg.Surface):
        if not super().draw(sc):
            return

        if self.render_background:
            sc.blit(self.border, self.position)

        sc.blit(self.image, (Vec(self.position) + to_blit_center(self.image, self.border)) ())
        if self.press or self.disable:
            sc.blit(self.dark, self.position)
        elif self.rect.collidepoint(pg.mouse.get_pos()):
            sc.blit(self.light, self.position)

        if ((self.show_tooltip and not self.press)
                or
            (self.press and self.hold_time >= 0.001 * Config.instance().get("tooltip_hold", 1000)
                    and
            Config.instance().get("mobile") and self.tooltip is not None)):
            self.set_tooltip(self.tooltip_image)
        elif self.scene.tooltip_of == self:
            self.remove_tooltip()
