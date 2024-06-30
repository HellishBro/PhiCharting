import pygame as pg
from .base import Component
from .button import Button
from .text_input import TextInput
from .tooltipped import Tooltipped
import os
from ..utils import *
from tkinter import filedialog

class FileChooser(Component, Tooltipped):
    def __init__(self, position: tuple, size: tuple, callback=None):
        super().__init__(position, size)
        self.text_input = TextInput(position, (size[0] - size[1], size[1]), 20, self.file_enter, "Type/Browse/Drag in file")
        self.browse_button = Button((position[0] + size[0] - size[1], position[1]), (size[1], size[1]), load_img("folder", 1.5), "Browse your computer for files", self.browse)
        self.add_child(self.text_input)
        self.add_child(self.browse_button)

        self.file_path = None
        self.callback = callback

    def browse(self, b: Button):
        filename = filedialog.askopenfilename()
        if filename:
            if os.path.exists(filename):
                self.text_input.value = filename
                self.text_input.update_text()
                self.file_path = filename
                self.text_input.erroring = False
                if self.callback: self.callback(self)

    def file_enter(self, t: TextInput):
        if os.path.exists(t.value):
            self.file_path = t.value
            self.text_input.erroring = False
            if self.callback: self.callback(self)
        else:
            self.text_input.error()

    def update(self, dt: float):
        if not super().update(dt):
            return

    def draw(self, sc: pg.Surface):
        if not super().draw(sc):
            return

    def event(self, ev: pg.Event):
        if not super().event(ev):
            return

    def click(self, ev: pg.Event, pos: tuple):
        if not super().click(ev, pos):
            return