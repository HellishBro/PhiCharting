import pygame as pg
from .base import Component
from .tooltipped import Tooltipped
from tkinter import messagebox
from PhiCharting.utils import *
from PhiCharting.config import Config
from .button import Button
import os
import json5
from dataclasses import dataclass

@dataclass
class Song:
    song_name: str
    composer: str
    level: str
    charter: str
    path: str
    song_path: str
    thumbnail_path: str
    chart_path: str

class SongList(Component, Tooltipped):
    # noinspection PyTypeChecker
    def __init__(self, position: tuple, size: tuple):
        super().__init__(position, size)
        self.scroll = 0

        self.songs: list[Song] = []
        for dir in os.listdir("charts/"):
            if not os.path.isdir("charts/" + dir):
                continue

            try:
                with open("charts/" + dir + "/info.json5") as f:
                    info = json5.loads(f.read())
                    self.songs.append(Song(info["name"], info["composer"], info["level"], info["charter"], "charts/" + dir,
                                           "charts/" + dir + "/" + info["song"], "charts/" + dir + "/" + info["thumbnail"],
                                           "charts/" + dir + "/" + info["chart"]))
            except FileNotFoundError:
                messagebox.showerror("Cannot Load Metadata", f"Cannot load metadata for {dir} because 'info.json5' is not found.\n\nSkipping.")

        y = position[1]
        button_height = 100
        self.max_scroll = button_height * len(self.songs)
        for index, song in enumerate(self.songs):
            bg_img = pg.transform.box_blur(pg.image.load(song.thumbnail_path), 10)
            bg_img = pg.transform.smoothscale_by(bg_img, size[0] / bg_img.get_width())
            button_image = pg.Surface((size[0], button_height))
            button_image.blit(bg_img, to_blit_center(bg_img, button_image))
            pg.draw.rect(button_image, (255, 255, 255), pg.Rect((0, 0), button_image.get_size()), 2, border_radius=3)
            song_text = text(song.song_name, 30, (255, 255, 255))
            button_image.blit(song_text, (14, 4))
            composer_text = text(song.composer, 20, (255, 255, 255))
            button_image.blit(composer_text, (14, 45))
            level_text = text(song.level, 30, (255, 255, 255))
            button_image.blit(level_text, (size[0] - level_text.get_width() - 10, 50))
            path_text = text(song.path, 15, (100, 100, 100), italic=True)
            button_image.blit(path_text, (14, 70))

            button = Button(
                (position[0], y),
                (size[0], button_height),
                button_image,
                callback=self.select_song_button,
                render_background=False
            )
            button.target_song = index
            self.add_child(button)
            y += button_height

        self.selected_song = 0
        self.song_thumbnail_blur: pg.Surface = None
        self.song_thumbnail_blur_400x400: pg.Surface = None
        self.song_thumbnail: pg.Surface = None

        self.select_song(0)
        self.locate_child(lambda b: b.target_song == self.selected_song)[0].disable = True

    def select_song(self, song_id):
        before_icon = pg.mouse.get_cursor()
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_WAIT)
        pg.mixer.music.stop()
        self.selected_song = song_id
        self.song_thumbnail = pg.image.load(self.songs[song_id].thumbnail_path).convert_alpha()
        self.song_thumbnail = fit(self.song_thumbnail, (400, 400))
        blur = pg.transform.gaussian_blur(self.song_thumbnail, 10)
        self.song_thumbnail_blur_400x400 = pg.transform.smoothscale(blur, (400, 400))
        self.song_thumbnail_blur_400x400.set_alpha(100)
        tn_aspect = blur.get_width() / blur.get_height()
        if tn_aspect > Config.instance().get("screen_size")[0] / Config.instance().get("screen_size")[1]:
            self.song_thumbnail_blur = pg.transform.smoothscale(blur, Config.instance().get("screen_size"))
        else:
            self.song_thumbnail_blur = pg.transform.smoothscale_by(blur, Config.instance().get("screen_size")[0] / blur.get_width())
        pg.mixer.music.load(self.songs[song_id].song_path)
        pg.mixer.music.rewind()
        pg.mixer.music.play()
        pg.mouse.set_cursor(before_icon)

    def select_song_button(self, button: Button):
        self.locate_child(lambda b: b.target_song == self.selected_song)[0].disable = False
        id = button.target_song
        button.disable = True
        self.select_song(id)

    def event(self, ev: pg.Event):
        if not Super(ev):
            return

        if ev.type == pg.MOUSEWHEEL and self.rect.collidepoint(pg.mouse.get_pos()):
            amount = ev.y * 25 * (pg.key.get_pressed()[pg.K_LSHIFT] * 3 + 1)
            self.scroll -= amount
            if self.scroll < 0:
                self.scroll = 0
                return
            elif self.scroll > self.max_scroll:
                self.scroll = self.max_scroll
                return

            for child in self.locate_child(lambda b: hasattr(b, "target_song")):
                child.position = (child.position[0], child.position[1] + amount)
