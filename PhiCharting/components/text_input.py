import pygame as pg
from .base import Component
from PhiCharting.utils import *
from typing import Callable

class TextInput(Component):
    # noinspection PyTypeChecker
    def __init__(self, position: tuple, size: tuple, font_size: int, callback=None, placeholder="", value="",
                 background_color: pg.Color=(0, 0, 0), text_color: pg.Color=(255, 255, 255), placeholder_color: pg.Color=(100, 100, 100),
                 border_color: pg.Color=(125, 125, 125),
                 allowed_characters: Callable[[str, str, str], bool]=None):
        super().__init__(position, size)
        self.font_size = font_size
        self.placeholder = placeholder
        self.value = value
        self.background_color = background_color
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.border_color = border_color
        self.callback = callback

        self.allowed_characters = allowed_characters if allowed_characters else lambda c, s, a: True

        self.focus = False
        self.cursor_index = len(self.value)
        self.text: pg.Surface = None

        self.selection_anchor = 0
        self.selection_end = 0
        self.selecting = False
        self.erroring = False

        self.update_text()

    def update_text(self):
        if self.value:
            bg_color = None
            if self.focus:
                bg_color = [min(self.background_color[x] + 20, 255) for x in range(3)]

            if self.selecting:
                select_start, select_end = min(self.selection_anchor, self.selection_end), max(self.selection_anchor, self.selection_end)
                text_1 = text(self.value[:select_start], self.font_size, self.text_color, bg_color)
                text_2 = text(self.value[select_end:], self.font_size, self.text_color, bg_color)
                text_s = text(self.value[select_start:select_end], self.font_size, self.text_color, (55, 80, 99))
                self.text = pg.Surface((text_1.get_width() + text_s.get_width() + text_2.get_width() + 4, text_1.get_height()),
                                       pg.SRCALPHA)
                self.text.fill((0, 0, 0, 0))
                self.text.blit(text_1, (0, 0))
                self.text.blit(text_s, (text_1.get_width() + 2, 0))
                self.text.blit(text_2, (text_1.get_width() + text_s.get_width() + 4, 0))
            else:
                text_1 = text(self.value[:self.cursor_index], self.font_size, self.text_color, bg_color)
                text_2 = text(self.value[self.cursor_index:], self.font_size, self.text_color, bg_color)
                self.text = pg.Surface((text_1.get_width() + 7 * self.focus + text_2.get_width(), text_1.get_height()), pg.SRCALPHA)
                self.text.fill((0, 0, 0, 0))
                self.text.blit(text_1, (0, 0))
                if self.focus:
                    self.text.fill(self.text_color, (text_1.get_width() + 2, 0, 3, text_1.get_height()))
                self.text.blit(text_2, (text_1.get_width() + 7 * self.focus, 0))
                if not self.focus:
                    t = self.text.copy()
                    self.text = pg.Surface((self.size[0] - 20, t.get_height()), pg.SRCALPHA)
                    self.text.fill((0, 0, 0, 0))
                    self.text.blit(t, (0, 0))

        else:
            self.text = text(self.placeholder, self.font_size, self.placeholder_color)
            if self.focus:
                self.text.fill(self.text_color, (2, 0, 3, self.text.get_height()))

    def error(self):
        self.erroring = True
        prev_text_color = self.text_color
        self.text_color = (255, 0, 0)
        self.update_text()
        self.text_color = prev_text_color

    def unfocus(self):
        self.focus = False
        self.selection_anchor = 0
        self.selection_end = 0
        self.selecting = False
        self.update_text()

    def update(self, dt: float):
        if not super().update(dt):
            return

    def event(self, ev: pg.Event):
        def redef_event():
            if not self.active:
                return

            if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                if self.rect.collidepoint(pg.mouse.get_pos()):
                    self.click(ev, pg.mouse.get_pos())
                    return

            elif ev.type == pg.MOUSEBUTTONUP and ev.button == 1:
                if self.focus and not self.rect.collidepoint(pg.mouse.get_pos()):
                    self.unfocus()
                    return

            for child in self.children:
                child.event(ev)
            return True

        if not redef_event():
            return

        elif ev.type == pg.TEXTINPUT and self.focus:
            ctrl = pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]
            select_start, select_end = min(self.selection_anchor, self.selection_end), max(self.selection_anchor, self.selection_end)
            before_value = self.value
            before_cursor = self.cursor_index
            before_selecting = self.selecting

            if self.selecting:
                self.selecting = False
                self.value = self.value[:select_start] + ev.text + self.value[select_end:]
                self.cursor_index = select_start + 1
                self.cursor_index = max(min(self.cursor_index, len(self.value)), 0)
            else:
                self.value = self.value[:self.cursor_index] + ev.text + self.value[self.cursor_index:]
                self.cursor_index += 1

            if not self.allowed_characters(ev.text, before_value, self.value):
                self.value = before_value
                self.cursor_index = before_cursor
                self.selecting = before_selecting

            self.update_text()

        elif ev.type == pg.KEYDOWN and self.focus:
            ctrl = pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]
            shift = pg.key.get_pressed()[pg.K_LSHIFT] or pg.key.get_pressed()[pg.K_RSHIFT]
            select_start, select_end = min(self.selection_anchor, self.selection_end), max(self.selection_anchor, self.selection_end)

            if ev.key == pg.K_BACKSPACE:
                if self.selecting:
                    self.value = self.value[:select_start] + self.value[select_end:]
                    self.cursor_index = select_start
                    self.selecting = False

                elif ctrl and self.cursor_index > 0:
                    start = self.cursor_index
                    while start > 0 and self.value[start - 1].isspace():
                        start -= 1
                    while start > 0 and not self.value[start - 1].isspace():
                        start -= 1

                    self.value = self.value[:start] + self.value[self.cursor_index:]
                    self.cursor_index = start
                else:
                    self.cursor_index -= 1
                    self.value = self.value[:max(self.cursor_index, 0)] + self.value[self.cursor_index + 1:]
                    self.cursor_index = max(0, self.cursor_index)
            if ev.key == pg.K_DELETE:
                if self.selecting:
                    self.value = self.value[:select_start] + self.value[select_end:]
                    self.cursor_index = select_start
                    self.selecting = False

                elif ctrl and self.cursor_index < len(self.value):
                    end = self.cursor_index
                    while end < len(self.value) and self.value[end].isspace():
                        end += 1
                    while end < len(self.value) and not self.value[end].isspace():
                        end += 1

                    self.value = self.value[:self.cursor_index] + self.value[end:]
                else:
                    self.value = self.value[:max(self.cursor_index, 0)] + self.value[self.cursor_index + 1:]

            elif ev.key == pg.K_LEFT:
                if shift:
                    if not self.selecting:
                        self.selecting = True
                        self.selection_anchor = self.cursor_index
                        self.selection_end = self.selection_anchor
                    self.selection_end -= 1
                    self.selection_end = max(self.selection_end, 0)
                elif (not shift) and self.selecting:
                    self.selecting = False
                    self.cursor_index = min(self.selection_anchor, self.selection_end)

                if ctrl and self.cursor_index > 0:
                    try:
                        while self.cursor_index > 0 and self.value[self.cursor_index - 1].isspace():
                            self.cursor_index -= 1
                        while self.cursor_index > 0 and not self.value[self.cursor_index - 1].isspace():
                            self.cursor_index -= 1
                    except: pass
                    self.selection_end = self.cursor_index
                else:
                    self.cursor_index -= 1
                    self.cursor_index = max(0, self.cursor_index)

            elif ev.key == pg.K_RIGHT:
                if shift:
                    if not self.selecting:
                        self.selecting = True
                        self.selection_anchor = self.cursor_index
                        self.selection_end = self.selection_anchor
                    self.selection_end += 1
                    self.selection_end = min(self.selection_end, len(self.value))
                elif (not shift) and self.selecting:
                    self.selecting = False
                    self.cursor_index = max(self.selection_anchor, self.selection_end)

                if ctrl and self.cursor_index < len(self.value):
                    while self.cursor_index < len(self.value) and self.value[self.cursor_index].isspace():
                        self.cursor_index += 1
                    while self.cursor_index < len(self.value) and not self.value[self.cursor_index].isspace():
                        self.cursor_index += 1
                    self.selection_end = self.cursor_index
                else:
                    self.cursor_index += 1
                    self.cursor_index = min(len(self.value), self.cursor_index)

            if ev.key == pg.K_ESCAPE:
                self.unfocus()

            if ev.key == pg.K_c and ctrl:
                pg.scrap.put_text(self.value[select_start:select_end])
            elif ev.key == pg.K_v and ctrl:
                if not all(self.allowed_characters(c, self.value, self.value + pg.scrap.get_text()) for c in pg.scrap.get_text()):
                    return

                if self.selecting:
                    self.selecting = False
                    self.value = self.value[:select_start] + pg.scrap.get_text() + self.value[select_end:]
                    self.cursor_index = select_end + len(pg.scrap.get_text())
                    self.cursor_index = min(self.cursor_index, len(self.value))
                else:
                    self.value = self.value[:self.cursor_index] + pg.scrap.get_text() + self.value[self.cursor_index:]
                    self.cursor_index += len(pg.scrap.get_text())
                    self.cursor_index = min(self.cursor_index, len(self.value))
            elif ev.key == pg.K_x and ctrl:
                pg.scrap.put_text(self.value[select_start:select_end])
                self.value = self.value[:select_start] + self.value[select_end:]
                self.cursor_index = select_start
            elif ev.key == pg.K_a and ctrl:
                self.selecting = True
                self.selection_anchor = 0
                self.selection_end = len(self.value)

            self.update_text()
            if ev.key == pg.K_RETURN or ev.key == pg.K_KP_ENTER:
                self.unfocus()
                if self.callback:
                    self.callback(self)

    def click(self, ev: pg.Event, pos: tuple):
        if not super().click(ev, pos):
            return

        self.focus = True
        self.cursor_index = len(self.value)
        self.update_text()
        pg.key.start_text_input()
        pg.key.set_repeat(500, 50)
        self.erroring = False

    def draw(self, sc: pg.Surface):
        if not super().draw(sc):
            return

        pg.draw.rect(sc, self.background_color, self.rect)
        border = self.border_color
        if self.erroring: border = (255, 0, 0)
        pg.draw.rect(sc, border, self.rect, 2 + self.focus * 2)
        sc.blit(self.text, (Vec(self.position) + (10, (self.size[1] - self.text.get_height()) / 2)) ())

