from os import path
import pygame as pg
from typing import Union
from tkinter import messagebox

__all__ = ["asset", "to_blit_center", "Vec", "text", "load_img", "scale", "fit"]

def asset(filename: str) -> str:
    return "assets/" + filename

def to_blit_center(surf: pg.Surface, relative_to: pg.Surface | pg.Rect) -> tuple:
    return (relative_to.width - surf.get_width()) / 2, (relative_to.height - surf.get_height()) / 2

class Vec:
    def __init__(self, item: Union[tuple, 'Vec', float], y: float=None):
        if isinstance(item, (float, int)):
            self.x = item
            self.y = y
        elif isinstance(item, (tuple, list)):
            self.x, self.y = item
        elif isinstance(item, Vec):
            self.x, self.y = item.x, item.y

    def __add__(self, other) -> 'Vec':
        other = Vec(other)
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Vec':
        other = Vec(other)
        return Vec(self.x - other.x, self.y + other.y)

    def __mul__(self, other) -> 'Vec':
        if isinstance(other, (int, float)):
            return Vec(self.x * other, self.y * other)

    def __call__(self, *args, **kwargs) -> tuple:
        """
        Turns the Vec into a tuple of (x, y)
        """
        return self.x, self.y

def text(content: str, size: int, color: pg.Color | tuple, background: pg.Color | tuple=None, italic=False):
    font = "NotoSans.ttf"
    if italic: font = "NotoSans-Italic.ttf"
    return pg.font.Font(asset(font), size).render(content, True, color, background)

shown = []

def load_img(filename: str, scale=1) -> pg.Surface:
    dir = asset(filename + ".png")
    try:
        return pg.transform.scale_by(pg.image.load(dir).convert_alpha(), scale)
    except FileNotFoundError:
        if not dir in shown:
            shown.append(dir)
            messagebox.showerror("Image not found!",
                                 f"The following path does not exist: {path.abspath(dir)}.\n\nThis is now replaced by a placeholder image.")
        surf = pg.Surface((16, 16))
        surf.fill((0, 0, 0))
        surf.fill((255, 0, 255), (0, 0, 7, 7))
        surf.fill((255, 0, 255), (8, 8, 15, 15))
        return pg.transform.scale_by(surf, scale)
    except pg.error:
        if not dir in shown:
            shown.append(dir)
            messagebox.showerror("Not an image!",
                                 f"The following path does not point to a valid image: {path.abspath(dir)}.\n\nThis is now replaced by a placeholder image.")
        surf = pg.Surface((16, 16))
        surf.fill((0, 0, 0))
        surf.fill((255, 0, 255), (0, 0, 7, 7))
        surf.fill((255, 0, 255), (8, 8, 15, 15))
        return pg.transform.scale_by(surf, scale)

def scale(image: pg.Surface, dimension: tuple):
    return pg.transform.scale(image, (max(0, dimension[0]), max(0, dimension[1])))

def fit(image: pg.Surface, target_dimensions: tuple, smooth=False):
    aspect_width = target_dimensions[0] / image.get_width()
    aspect_height = target_dimensions[1] / image.get_height()
    aspect_ratio = min(aspect_width, aspect_height)
    if smooth:
        try:
            s = pg.transform.smoothscale_by(image, aspect_ratio)
        except ValueError:
            s = pg.transform.scale_by(image, aspect_ratio)
    else:
        s = pg.transform.scale_by(image, aspect_ratio)
    return s
