import pygame
from event_info import EventInfo
from laser_class import Laser

class Player():
    def __init__(self) -> None:
        self.player_fly_0 = pygame.image.load("assets//player_spaceship//player_spaceship_fly_0.png").convert_alpha()
        self.player_fly_1 = pygame.image.load("assets//player_spaceship//player_spaceship_fly_1.png").convert_alpha()
        self.player_frames = [self.player_fly_0, self.player_fly_1]
        self.animation_index = 0

        self.image = self.player_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(400, 450))

        self.lasers = pygame.sprite.Group()
    
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
    
    def shoot_laser(self, event_info : EventInfo):
        events = event_info["events"]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.lasers.add(Laser(self.rect.centerx))
    
    def update(self, event_info : EventInfo):
        self.animate()
        self.movement(event_info)
        self.shoot_laser(event_info)
    
    def draw(self, screen : pygame.Surface):
        screen.blit(self.image, self.rect)
        self.lasers.update()
        self.lasers.draw()
