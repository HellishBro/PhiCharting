import pygame as pg
from pygame import gfxdraw
import math

from .base import Component
from PhiCharting.utils import *
from PhiCharting import phigros as phi

PERFECT = (255, 236, 159)


class ChartRender(Component):
    def __init__(self, position: tuple, size: tuple, chart: phi.Chart, directory: str):
        super().__init__(position, size)
        self.playing = False
        self.time = 0
        self.chart = chart
        self.directory = directory
        self.bpm = self.chart.bpm_list[0].bpm
        print("BPM", self.bpm)
        self.unit_y = size[1] / 900 # range: [-450, 450]
        # size of a Y unit in pixels
        self.unit_x = size[0] / 1350 # range: [-675, 675]

        print("Y-Unit", self.unit_y)

        self.texture_cache = {"line.png": load_img("line")}
        note_scale = 0.1
        self.note_images = [
            None,
            pg.transform.smoothscale_by(load_img("skin/click"), note_scale),
            pg.transform.smoothscale_by(load_img("skin/hold"), note_scale),
            pg.transform.smoothscale_by(load_img("skin/flick"), note_scale),
            pg.transform.smoothscale_by(load_img("skin/drag"), note_scale) # requires special processing
        ]

    def coord_from_unit(self, x: float, y: float) -> tuple:
        return x * self.unit_x + self.size[0] / 2, -y * self.unit_y + self.size[1] / 2

    def should_process_event(self, event: phi.Event):
        start = self.time_from_beats(event.start_time)
        end = self.time_from_beats(event.end_time)
        should = start <= self.time <= end
        do_break = False
        if should and event.duration == -1:
            event.duration = end - start
        if not should:
            if self.time < start:
                do_break = True
        return should, do_break

    def process_event(self, events: list[phi.Event], dt: float) -> float:
        active: phi.Event = next(filter(lambda ev: self.time_from_beats(ev.start_time) <= self.time <= self.time_from_beats(ev.end_time), events), False)
        if active:
            if active.duration == -1:
                active.duration = self.time_from_beats(active.end_time) - self.time_from_beats(active.start_time)
            active.time += dt
            return active.ease()

    @staticmethod
    def pos_relative_to_line(position: tuple, line: phi.Line):
        rad = math.radians(line.rotation)
        return (
            line.x + position[0] * math.cos(rad) - position[1] * math.sin(rad),
            line.y + position[0] * math.sin(rad) + position[1] * math.cos(rad)
        )

    def render_note(self, sc: pg.Surface, note: phi.Note, line: phi.Line):
        # speed = note_speed * line_speed * 120 (y units / second)
        # unit = base_units * note_speed * line_speed * 120?
        time_diff = self.time_from_beats(note.time) - self.time
        effective_speed = note.speed * line.speed
        units = time_diff * self.unit_y * effective_speed * 120 * (note.above * 2 - 1)

        pos = self.pos_relative_to_line((note.x, units), line)
        world = self.coord_from_unit(*pos)
        image = self.note_images[note.type]
        if note.type == 2: # hold note
            hold_length = abs((self.time_from_beats(note.end_time) - self.time_from_beats(note.time)) * self.unit_y * effective_speed * 120)
            image = pg.transform.scale(image, (image.get_width(), hold_length))
            pos = self.pos_relative_to_line((note.x, units + hold_length), line)
            world = self.coord_from_unit(*pos)
        image = pg.transform.rotate(image, -line.rotation + 180 * (not note.above))
        sc.blit(image, world)

    def get_visible_notes(self, line: phi.Line) -> list[phi.Note]:
        return filter(
            lambda note: self.time <= self.time_from_beats(note.time) or self.time <= self.time_from_beats(note.end_time),
            line.notes
        )

    def update_line(self, id: int, dt: float):
        line = self.chart.lines[id]
        for layer in line.events:
            if x := self.process_event(layer.move_x, dt):
                layer.curr_x = x
            if y := self.process_event(layer.move_y, dt):
                layer.curr_y = y
            if alpha := self.process_event(layer.alpha, dt):
                layer.curr_alpha = alpha
            if rotation := self.process_event(layer.rotate, dt):
                layer.curr_rotate = rotation
            if speed := self.process_event(layer.speed, dt):
                layer.curr_speed = speed

        x = y = alpha = rotation = speed = 0
        for layer in line.events:
            x += layer.curr_x
            y += layer.curr_y
            alpha += layer.curr_alpha
            rotation += layer.curr_rotate
            speed += layer.curr_speed

        line.x = x
        line.y = y
        line.alpha = max(min(255, alpha), 0)
        line.rotation = rotation
        line.speed = speed

        if line.texture not in self.texture_cache:
            try:
                surf = pg.image.load(self.directory + "/" + line.texture).convert_alpha()
            except FileNotFoundError:
                surf = pg.Surface((16, 16))
                surf.fill((0, 0, 0))
                surf.fill((255, 0, 255), (0, 0, 7, 7))
                surf.fill((255, 0, 255), (8, 8, 15, 15))
            self.texture_cache[line.texture] = surf

    def time_from_beats(self, beats: float):
        return beats * (60 / self.bpm)

    def update(self, dt: float):
        if self.playing:
            self.time += dt

            for i in range(len(self.chart.lines)):
                self.update_line(i, dt)

    def draw_line(self, sc: pg.Surface, angle: float, translation: tuple, alpha: float):
        radians = math.radians(angle)
        dir_x = math.cos(radians)
        dir_y = math.sin(radians)

        start_x, start_y = translation

        if dir_x != 0:
            t1 = -start_x / dir_x
            t2 = (self.size[0] - start_x) / dir_x
        else:
            t1 = -math.inf
            t2 = math.inf

        if dir_y != 0:
            t3 = -start_y / dir_y
            t4 = (self.size[1] - start_y) / dir_y
        else:
            t3 = -math.inf
            t4 = math.inf

        t_min = max(min(t1, t2), min(t3, t4))
        t_max = min(max(t1, t2), max(t3, t4))

        end_1_x = min(self.size[0], max(0, start_x + t_min * dir_x))
        end_1_y = min(self.size[0], max(0, start_y + t_min * dir_y))
        end_2_x = min(self.size[0], max(0, start_x + t_max * dir_x))
        end_2_y = min(self.size[0], max(0, start_y + t_max * dir_y))
        gfxdraw.line(sc, int(end_1_x), int(end_1_y), int(end_2_x), int(end_2_y), (*PERFECT, alpha))

    def draw(self, sc: pg.Surface):
        for i, line in enumerate(self.chart.lines):
            center = self.coord_from_unit(line.x, line.y)
            if line.texture == "line.png":
                self.draw_line(sc, line.rotation, center, line.alpha)

            else:
                texture = self.texture_cache[line.texture]
                if line.rotation:
                    texture = pg.transform.rotate(texture, line.rotation)
                texture.set_alpha(line.alpha)
                sc.blit(texture, center_coord(center, texture.size))

            for note in self.get_visible_notes(line):
                self.render_note(sc, note, line)

            #sc.blit(text(str(i), 20, (255, 255, 255)), center)
