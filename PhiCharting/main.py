import pygame as pg
from config import Config
import scenes
from tkinter import messagebox

pg.init()
SIZE = Config.instance().get("screen_size")
sc = pg.display.set_mode(SIZE)
pg.display.set_caption("PhiCharting")

current_scene: scenes.Scene = scenes.Title()

run = True
clock = pg.Clock()

while run:
    dt = clock.tick() / 1000

    for ev in pg.event.get():
        if ev.type == pg.QUIT or (ev.type == pg.WINDOWCLOSE and ev.window is None):
            run = False
            break

        current_scene.event(ev)

    sc.fill((0, 0, 0))

    if current_scene.switch_scene is not None:
        pg.mixer.music.stop()
        next_scene = getattr(scenes, current_scene.switch_scene)
        next_scene = next_scene(*current_scene.switch_scene_args)
        current_scene = next_scene

    current_scene.update(dt)
    current_scene.draw(sc)

    if current_scene.tooltip:
        if pg.mouse.get_pos()[0] + current_scene.tooltip.get_width() + 10 > SIZE[0]:
            sc.blit(current_scene.tooltip, (pg.mouse.get_pos()[0] - current_scene.tooltip.get_width() - 10, pg.mouse.get_pos()[1]))
        else:
            sc.blit(current_scene.tooltip, (pg.mouse.get_pos()[0] + 10, pg.mouse.get_pos()[1]))

    pg.display.flip()

Config.instance().save()
