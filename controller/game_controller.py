import pygame

from model import Player
from view import *
from config import *

import pygame

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.entities = []
        self.player = None
        self.running = True
        pygame.display.set_caption(GAME_TITLE)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.running = False
                    case pygame.K_w:
                        self.player.y -= 1
                    case pygame.K_s:
                        self.player.y += 1
                    case pygame.K_a:
                        self.player.x -= 1
                    case pygame.K_d:
                        self.player.x += 1

    def create_player(self, **kwargs):
        self.player = Player(**kwargs)
        self.entities.append(self.player)
        return self.player
    def create_npc(self, **kwargs):
        self.entities.append(NPC(**kwargs))
        return self.entities[-1]