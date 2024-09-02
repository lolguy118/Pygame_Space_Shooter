from typing import Tuple
import pygame
from os import listdir


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]) -> None:
        super().__init__()
        self.frames = []
        for frame in listdir("assets//explosion"):
            self.frames.append(f"assets//explosion//{frame}")
        self.animation_index = 0

        pygame.mixer.init()
        self.explosion_sound = pygame.mixer.Sound("music//explosion.wav")
        pygame.mixer.Sound.play(self.explosion_sound)

        self.image = pygame.transform.scale(
            pygame.image.load(self.frames[self.animation_index]), (160, 150)
        )
        self.rect = self.image.get_rect(center=position)

        self.animation_is_over = False

    def animate(self) -> None:
        self.animation_index += 0.5
        if int(self.animation_index) > len(self.frames) - 1:
            self.animation_is_over = True
            self.animation_index = len(self.frames) - 1
        self.image = pygame.transform.scale(
            pygame.image.load(self.frames[int(self.animation_index)]), (160, 150)
        )

    def update(self) -> None:
        if self.animation_is_over:
            self.kill()
        else:
            self.animate()
