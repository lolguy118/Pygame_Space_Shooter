import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, player_x_position: int) -> None:
        super().__init__()
        self.image = pygame.image.load("assets//laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(player_x_position, 650))

    def destroy(self) -> None:
        if self.rect.bottom <= 0:
            self.kill()

    def update(self) -> None:
        self.destroy()
        self.rect.y -= 5
