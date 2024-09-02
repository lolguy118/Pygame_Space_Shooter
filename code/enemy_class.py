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
        "astroid" : [
    "assets//astroid//astroid_spin_0.png",
    "assets//astroid//astroid_spin_1.png",
    "assets//astroid//astroid_spin_2.png",
    "assets//astroid//astroid_spin_3.png",
    "assets//astroid//astroid_spin_4.png",
    "assets//astroid//astroid_spin_5.png",
    "assets//astroid//astroid_spin_6.png",
    "assets//astroid//astroid_spin_7.png",
    "assets//astroid//astroid_spin_8.png",
    "assets//astroid//astroid_spin_9.png",
    "assets//astroid//astroid_spin_10.png",
    "assets//astroid//astroid_spin_11.png",
    "assets//astroid//astroid_spin_12.png",
    "assets//astroid//astroid_spin_13.png",
    "assets//astroid//astroid_spin_14.png",
    "assets//astroid//astroid_spin_15.png",
    "assets//astroid//astroid_spin_16.png",
    "assets//astroid//astroid_spin_17.png",
    "assets//astroid//astroid_spin_18.png",
    "assets//astroid//astroid_spin_19.png",
    "assets//astroid//astroid_spin_20.png",
    "assets//astroid//astroid_spin_21.png"
    ]

    }

    def __init__(self) -> None:
        super().__init__()
        self.type = choice(["astroid", "spaceship"])
        self.frames = self.type_to_frames[self.type]
        self.animation_index = 0

        self.image = pygame.image.load(
            self.frames[self.animation_index]
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 150))
        self.rect = self.image.get_rect(right=choice([160, 320, 480, 640, 800]))
        self.rect.top = -100

    def animate(self) -> None:
        self.animation_index += 0.5
        if int(self.animation_index) > len(self.frames) - 1:
            self.animation_index = 0

        self.image = pygame.image.load(
            self.frames[int(self.animation_index)]
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 150))

    def update(self) -> None:
        self.animate()
        self.rect.centery += 5
