import pygame
from event_info import EventInfo

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.player_fly_0 = pygame.image.load("assets//player_spaceship//player_spaceship_fly_0.png")
        self.player_fly_1 = pygame.image.load("assets//player_spaceship//player_spaceship_fly_1.png")
        self.player_frames = [self.player_fly_0, self.player_fly_1]
        self.animation_index = 0

        self.image = self.player_frames[self.animation_index]
        self.rect = self.image.get_rect()