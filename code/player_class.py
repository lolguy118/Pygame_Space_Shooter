import pygame
from event_info import EventInfo
from laser_class import Laser

class Player():
    def __init__(self) -> None:
        self.player_fly_0 = pygame.transform.scale(pygame.image.load("assets//player_spaceship//player_spaceship_fly_0.png").convert_alpha(), (160, 150))
        self.player_fly_1 = pygame.transform.scale(pygame.image.load("assets//player_spaceship//player_spaceship_fly_1.png").convert_alpha(), (160, 150))
        self.player_frames = [self.player_fly_0, self.player_fly_1]
        self.animation_index = 0

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound("music//laser.wav")

        self.image = self.player_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(400, 800))

        self.lasers = pygame.sprite.Group()
    
    def animate(self) -> None:
        self.animation_index += 0.1
        if int(self.animation_index) > 1:
            self.animation_index = 0
        self.image = self.player_frames[int(self.animation_index)]
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def movement(self, event_info : EventInfo) -> None:
        keys_pressed = event_info["keys"]
        if keys_pressed[pygame.K_LEFT] and self.rect.left - 5 > 0:
            self.rect.x -= 5
        elif keys_pressed[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += 5
    
    def shoot_laser(self, event_info : EventInfo):
        events = event_info["events"]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(self.laser_sound)
                    pygame.mixer.music.stop()
                    self.lasers.add(Laser(self.rect.centerx))
    
    def update(self, event_info : EventInfo):
        self.animate()
        self.movement(event_info)
        self.shoot_laser(event_info)
    
    def draw(self, screen : pygame.Surface):
        screen.blit(self.image, self.rect)
        self.lasers.update()
        self.lasers.draw(screen)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    player = Player()
    clcok = pygame.time.Clock()
    while True:
        screen.fill("black")
        events = {"events" : pygame.event.get(), "keys" : pygame.key.get_pressed()}
        player.update(events)
        player.draw(screen)
        pygame.display.update()
        clcok.tick(60)