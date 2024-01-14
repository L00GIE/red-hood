import sys
sys.dont_write_bytecode = True

import pygame
from lib.core import Core

windowed = True

pygame.init()
if windowed:
    screen = pygame.display.set_mode((1366, 768))
else:
    screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
core = Core()
clock = pygame.time.Clock()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    if running:
        core.loop(events)
        clock.tick(60)
        pygame.display.update()
        pygame.display.set_caption(f"Red Hood | {round(clock.get_fps(), 2)} FPS | x: {round(core.player.x)} y: {round(core.player.y)}")

pygame.quit()
sys.exit(0)