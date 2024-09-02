import pygame
from random import choice
from os import listdir


class Enemy(pygame.sprite.Sprite):
    # TODO add "assets//astroid" to all of the asteroid frames
    type_to_frames = {
        "spaceship": [
            "assets//enemy_spaceship//enemy_spaceship_fly_0.png",
            "assets//enemy_spaceship//enemy_spaceship_fly_1.png",
        ],
        "asteroid": sorted(
            listdir("assets/astroid"), key=lambda f: int(f.split("_")[-1].split(".")[0])
        ),
    }

    def __init__(self) -> None:
        super().__init__()
        self.type = choice(["spaceship", "asteroid"])
        self.frames = self.type_to_frames[self.type]
        self.animation_index = 0

        self.image = pygame.image.load(
            self.frames[self.animation_index]
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 150))
        self.rect = self.image.get_rect(right=choice([160, 320, 480, 640, 800]))
        self.rect.top = -100

    def animate(self) -> None:
        self.animation_index += 0.1
        if int(self.animation_index) > len(self.frames):
            self.animation_index = 0

        self.image = pygame.image.load(
            self.frames[self.animation_index]
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 150))

    def update(self) -> None:
        self.animate()
        self.rect.centery += 5
