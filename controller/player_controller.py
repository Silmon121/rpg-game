import pygame
import registry


class PlayerController:
    def handle_input(self, event):
        player = registry.game.player
        if player.x is None and player.y is None:
            return
        match event.key:
            case pygame.K_w:
                player.move(0,-1)
            case pygame.K_s:
                player.move(0,1)
            case pygame.K_a:
                player.move(-1,0)
            case pygame.K_d:
                player.move(1,0)