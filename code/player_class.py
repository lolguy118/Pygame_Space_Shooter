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
        self.rect = self.image.get_rect(midbottom=(400, 450))
    
    def animate(self) -> None:
        self.animation_index += 0.1
        if int(self.animation_index) > 1:
            self.animation_index = 0
        self.image = self.player_frames[self.animation_index]
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def movement(self, event_info : EventInfo) -> None:
        keys_pressed = event_info["keys"]
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= 5
        elif keys_pressed[pygame.K_RIGHT]:
            self.rect.x += 5
