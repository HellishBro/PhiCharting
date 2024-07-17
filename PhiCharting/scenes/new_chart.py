import pygame as pg

from .base import Scene
from PhiCharting.components import *
from PhiCharting.utils import *
from PhiCharting.config import Config

from PhiCharting import phigros as phi

from pathlib import Path
from tkinter import messagebox
from os import path
import json5, json
import shutil

class NewChart(Scene):
    # noinspection PyTypeChecker
    def __init__(self):
        super().__init__()
        self.back_button = self.add_component(Button(
            (30, 30), (150, 100),
            text("Back", 40, (255, 255, 255)), "Go back to title", self.go_back))

        self.page = 0

        screen_width, screen_height = Config.instance().get("screen_size")
        self.current_screen = Text((0, 0), "Asset Information", 50, (255, 255, 255))
        self.current_screen.position = (screen_width - self.current_screen.size[0] - 50, 30)

        self.next_screen = self.add_component(Button((screen_width - 250, screen_height - 125), (200, 75), text("Next", 30, (255, 255, 255)), "Go to next page", self.next_page))
        self.prev_screen = self.add_component(Button((screen_width - 450, screen_height - 125), (200, 75), text("Previous", 30, (255, 255, 255)), "Go to previous page", self.prev_page))
        self.prev_screen.disable = True

        # Asset Information

        self.audio_track_text = Text((30, 160), "Audio:", 40, (200, 200, 200))
        self.audio_track = FileChooser((300, 160), (screen_width - 350, 50)).set_scene(self)
        self.audio_preview_button = Button((250, 160), (50, 50), load_img("speaker"), "Preview song", self.preview_song).set_scene(self)
        self.audio_previewing = False

        self.thumbnail_text = Text((30, 260), "Thumbnail:", 40, (200, 200, 200))
        self.thumbnail = FileChooser((250, 260), (screen_width - 300, 50), self.load_thumbnail).set_scene(self)
        self.thumbnail_image: pg.Surface = None
        self.thumbnail_blur: pg.Surface = None

        # Chart Information

        self.chart_name_text = Text((30, 160), "Chart Name:", 40, (200, 200, 200))
        self.chart_name = TextInput((300, 160), (screen_width - 350, 50), 20, placeholder="Chart Name")
        self.chart_save_text = Text((30, 220), "Will be saved in:", 20, (125, 125, 125), italic=True)
        self.chart_save = TextInput((40 + self.chart_save_text.size[0], 220), (screen_width - 90 - self.chart_save_text.size[0], 30), 15, placeholder="Chart_Path")

        self.difficulty_text = Text((30, 270), "Difficulty:", 40, (200, 200, 200))
        self.difficulty = TextInput((300, 270), (screen_width - 350, 50), 20, placeholder="IN Lv.15")

        self.composer_text = Text((30, 340), "Composer:", 40, (200, 200, 200))
        self.composer = TextInput((300, 340), (screen_width - 350, 50), 20, placeholder="Composer")

        self.thumbnail_artist_text = Text((30, 410), "Illustrator:", 40, (200, 200, 200))
        self.thumbnail_artist = TextInput((300, 410), (screen_width - 350, 50), 20, placeholder="Unknown")

        self.charter_text = Text((30, 480), "Charter:", 40, (200, 200, 200))
        self.charter = TextInput((300, 480), (screen_width - 350, 50), 20, placeholder="Charter")

        # Starting Information

        self.default_speed_text = Text((30, 160), "Scroll Speed:", 40, (200, 200, 200))
        self.default_speed = TextInput((300, 160), (screen_width - 350, 50), 20, placeholder="10", allowed_characters=lambda s, v, a: s in "0123456789-." and a.count(".") < 2)

        self.default_bpm_text = Text((30, 230), "BPM:", 40, (200, 200, 200))
        self.default_bpm = TextInput((300, 230), (screen_width - 350, 50), 20, placeholder="120", allowed_characters=lambda s, v, a: s in "0123456789." and a.count(".") < 2 and a[0] != "0")

        self.line_amount_text = Text((30, 300), "Lines:", 40, (200, 200, 200))
        self.line_amount = TextInput((300, 300), (screen_width - 350, 50), 20, placeholder="24", allowed_characters=lambda s, v, a: s in "0123456789" and a[0] != "0")

        self.start = Button(self.next_screen.position, self.next_screen.size, text("Create!", 30, (255, 255, 255)), "Create the chart files!", self.create_chart).set_scene(self)

        self.pages = [
            [],
            [
                self.audio_track_text, self.audio_track, self.audio_preview_button,
                self.thumbnail_text, self.thumbnail_image, self.thumbnail
            ],
            [
                self.chart_name_text, self.chart_name, self.chart_save_text, self.chart_save,
                self.difficulty_text, self.difficulty,
                self.composer_text, self.composer,
                self.thumbnail_artist_text, self.thumbnail_artist,
                self.charter_text, self.charter
            ],
            [
                self.default_speed_text, self.default_speed,
                self.default_bpm_text, self.default_bpm,
                self.line_amount_text, self.line_amount,
                self.start
            ]
        ]
        self.require_input = [
            [],
            [
                self.audio_track, self.thumbnail
            ],
            [
                self.chart_name, self.chart_save, self.difficulty, self.composer, self.thumbnail_artist, self.charter
            ],
            [
                self.default_speed, self.default_bpm, self.line_amount
            ]
        ]
        self.page_names = [
            None,
            "Asset Information",
            "Chart Information",
            "Starting Information"
        ]
        self.load_page(1)

    def create_chart(self, b: Button):
        directory = Path(self.chart_save.value)
        directory.mkdir(parents=True, exist_ok=True)
        song_path = "song." + self.audio_track.file_path.split(".")[-1]
        thumbnail_path = "thumbnail." + self.thumbnail.file_path.split(".")[-1]

        with open(directory / "info.json5", "w") as f:
            f.write(json5.dumps({
                "name": self.chart_name.value,
                "chart": "chart.json",
                "song": song_path,
                "thumbnail": thumbnail_path,
                "level": self.difficulty.value,
                "composer": self.composer.value,
                "charter": self.charter.value,
                "illustrator": self.thumbnail_artist.value,
            }, indent=4))

        shutil.copy2(self.audio_track.file_path, directory / song_path)
        shutil.copy2(self.thumbnail.file_path, directory / thumbnail_path)

        lines = [phi.Line([], f"Unnamed {i}", events=[
            phi.Event(phi.Property.SPEED, 0, float(self.default_speed.value), float(self.default_speed.value), 0, 60 / float(self.default_bpm.value))
        ] + ([phi.Event(phi.Property.ALPHA, 0, 0, 255, 0, 60 / float(self.default_bpm.value))] if i == 0 else [])) for i in range(int(self.line_amount.value))]

        with open(directory / "chart.json", "w") as f:
            f.write(json.dumps(phi.Chart([phi.BPMTiming(0, float(self.default_bpm.value))], lines).to_json(
                defaultSpeed=float(self.default_speed.value)
            ), indent=4))

        messagebox.showinfo("Chart Creation Done!", f"Chart files for {self.chart_name.value} is now created!")
        self.switch_scene = "Title"

    def next_page(self, b: Button):
        self.load_page(min(self.page + 1, len(self.pages) - 1))

        if self.page == 2:
            if not self.chart_name.value:
                name = Path(self.audio_track.file_path).name.split('.', 2)[0]
                self.chart_name.value = name
                self.chart_name.update_text()
                name_clean = name.replace(" ", "_")
                name_clean = "".join(char for char in name_clean if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
                chart_save = path.abspath(f"charts/{name_clean}")

                index = 2
                while path.exists(chart_save):
                    chart_save = chart_save + "_" + str(index)
                    index += 1

                self.chart_save.value = chart_save
                self.chart_save.update_text()

    def prev_page(self, b: Button):
        self.load_page(max(self.page - 1, 1))

    def load_page(self, new_page):
        error = False
        for item in self.require_input[self.page]:
            if isinstance(item, FileChooser):
                if item.file_path is None:
                    item.text_input.error()
                    error = True
            elif isinstance(item, TextInput):
                if not item.value:
                    item.error()
                    error = True

        if error:
            return

        for item in self.pages[self.page]:
            if item:
                item.active = False
                item.visible = False
        self.page = new_page
        for item in self.pages[self.page]:
            if item:
                item.active = True
                item.visible = True

        screen_width = Config.instance().get("screen_size")[0]
        self.current_screen = Text((0, 0), self.page_names[self.page], 50, (255, 255, 255))
        self.current_screen.position = (screen_width - self.current_screen.size[0] - 50, 30)

        self.prev_screen.disable = self.page == 1
        self.next_screen.disable = self.page == len(self.pages) - 1
        self.next_screen.visible = not self.page == len(self.pages) - 1
        self.next_screen.active = not self.page == len(self.pages) - 1

    def load_thumbnail(self, f: FileChooser):
        try:
            img = pg.image.load(f.file_path).convert_alpha()
            self.thumbnail_image = fit(img, (200, 200), True)
            self.thumbnail_blur = pg.transform.smoothscale_by(pg.transform.box_blur(img, 10), Config.instance().get("screen_size")[0] / img.get_width())
            self.thumbnail_blur.set_alpha(127)
        except pg.error:
            self.thumbnail.text_input.error()

    def preview_song(self, button: Button):
        if not self.audio_previewing:
            if self.audio_track.file_path is not None:
                previous = pg.mouse.get_cursor()
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_WAIT)
                try:
                    pg.mixer.music.load(self.audio_track.file_path)
                    pg.mixer.music.play()
                    self.audio_preview_button.generate_tooltip("Stop preview")
                    self.audio_previewing = True
                except pg.error:
                    self.audio_track.text_input.error()

                pg.mouse.set_cursor(previous)
        else:
            pg.mixer.music.stop()
            self.audio_preview_button.generate_tooltip("Preview song")
            self.audio_previewing = False

    def go_back(self, button: Button):
        self.switch_scene = 'Title'

    def update(self, dt: float):
        Super(dt)

        for item in self.pages[self.page]:
            if item:
                item.update(dt)

    def draw(self, sc: pg.Surface):
        if self.thumbnail_blur:
            sc.blit(self.thumbnail_blur, (0, 0))
        self.current_screen.draw(sc)

        for item in self.pages[self.page]:
            if item:
                item.draw(sc)

        if self.thumbnail_image and self.page == 1:
            sc.blit(self.thumbnail_image, (250, 320))

        Super(sc)

    def event(self, ev: pg.Event):
        Super(ev)

        for item in self.pages[self.page]:
            if item:
                item.event(ev)

    def click(self, ev: pg.Event, pos: tuple):
        pass

