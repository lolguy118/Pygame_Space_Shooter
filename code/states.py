from abc import abstractmethod, ABC
import pygame
from event_info import EventInfo
from typing import Any
from player_class import Player


class GameState(ABC):
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = pygame.transform.scale(
            pygame.image.load("assets//space_background.png"), (800, 800)
        )
        self.is_over = False

    @abstractmethod
    def update(self, event_info: EventInfo) -> None:
        pass

    @abstractmethod
    def next_game_state(self) -> Any:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

class TitleScreen(GameState):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.title_font = pygame.font.Font("assets//PixelifySans-VariableFont_wght.ttf", 100)
        self.text_surf = self.title_font.render("Space Shooter", False, "white")
        self.text_rect = self.text_surf.get_rect(midtop=(400, 50))
        
        self.smaller_font = pygame.font.Font("assets//PixelifySans-VariableFont_wght.ttf", 50)
        self.smaller_text_surf = self.smaller_font.render("Press Enter To Begin", False, "white")
        self.smaller_text_rect = self.smaller_text_surf.get_rect(midbottom=(400, 750))
        self.text_event = pygame.USEREVENT + 1
        self.text_timer = pygame.time.set_timer(self.text_event, 500)
        self.text_is_visible = True
        
        pygame.mixer.init()

        self.background_music = pygame.mixer.music.load("music//title_screen.wav")
        pygame.mixer.music.play(-1)

        self.spaceship_frames = [pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets//player_spaceship//player_spaceship_fly_0.png"), -90), (150, 150)), pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets//player_spaceship//player_spaceship_fly_1.png"), -90), (150, 150))]
        self.spaceship_animation_index = 0
        self.spaceship_surf = self.spaceship_frames[self.spaceship_animation_index]
        self.spaceship_rect = self.spaceship_surf.get_rect(midleft=(0, 400))
    
    def spaceship_animate(self):
        self.spaceship_animation_index += 0.1
        if int(self.spaceship_animation_index) > 1:
            self.spaceship_animation_index = 0
        self.spaceship_surf = self.spaceship_frames[int(self.spaceship_animation_index)]
        
        self.spaceship_rect.x += 5
        if self.spaceship_rect.left > 800:
            self.spaceship_rect.right = 0

    def update(self, event_info: EventInfo) -> None:
        for event in event_info["events"]:
            if event.type == self.text_event:
                self.text_is_visible = not self.text_is_visible
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.is_over = True
                print("over")
        
        self.spaceship_animate()
    
    def next_game_state(self) -> Any:
        return MainGame(self.screen)
    
    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.spaceship_surf, self.spaceship_rect)
        self.screen.blit(self.text_surf, self.text_rect)
        if self.text_is_visible:
            self.screen.blit(self.smaller_text_surf, self.smaller_text_rect)

class MainGame(GameState):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.player = Player()
        self.enemies = pygame.sprite.Group()

        self.spawn_rate = 500
        self.spawn_rate_adjuster = 1
        self.spawn_enemy_event = pygame.USEREVENT + 1
        self.spawn_enemy_timer = pygame.time.set_timer(self.spawn_enemy_event, self.spawn_rate)

        self.score = 0
    def update_spawn_rate(self):
        if self.score % 10 == 0:
            self.spawn_rate_adjuster += 1
            self.spawn_rate = int(self.spawn_rate / self.spawn_rate_adjuster)
            self.spawn_enemy_timer = pygame.time.set_timer(self.spawn_enemy_event, self.spawn_rate)
    def check_if_enemy_went_kaboom(self):
        pass


class ResultScreen(GameState):
    pass

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
titlescreen = TitleScreen(screen)
while True:
    eventinfo = {"events" : pygame.event.get()}
    for event in eventinfo["events"]:
        if event.type == pygame.QUIT:
            raise SystemExit
    titlescreen.update(eventinfo)
    titlescreen.draw()
    pygame.display.update()
