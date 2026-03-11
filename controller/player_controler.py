from model import Player, Entity
import pygame

class PlayerController:
    @staticmethod
    def handle_input(event, player):
        if player.x is None and player.y is None:
            return
        match event.key:
            case pygame.K_w:
                if player.y - 1 < 0:
                    return
                player.y -= 1
            case pygame.K_s:
                player.y += 1
                print(player.y)
            case pygame.K_a:
                if player.x - 1 < 0:
                    return
                player.x -= 1
            case pygame.K_d:
                player.x += 1