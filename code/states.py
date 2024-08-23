from abc import abstractmethod, ABC
import pygame
from event_info import EventInfo
from typing import Any


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
        self.title_font = pygame.font.Font("assets\PixelifySans-VariableFont_wght.ttf", 200)
        self.text_surf = self.font.render("Space Shooter", False, "white")
        self.text_rect = self.text_surf.get_rect(midtop=(400, 50))
        
        self.smaller_font = pygame.font.Font("assets\PixelifySans-VariableFont_wght.ttf", 50)
        self.smaller_text_surf = self.font.render("Press Enter To Begin", False, "white")
        self.smaller_text_rect = self.smaller_text_surf.get_rect(midbottom=(400, 750))
        self.text_timer = pygame.time.set_timer(pygame.USEREVENT, 500)
        self.text_is_visible = True
        
        pygame.mixer.init()

        self.background_music = pygame.mixer.music.load("music//title_screen.wav")
        pygame.mixer.music.play(-1)

        self.spaceship_frames = [pygame.image.load("assets//player_spaceship_fly_0.png"), pygame.image.load("assets//player_spaceship_fly_1.png")]
        self.spaceship_animation_index = 0
        self.spaceship_surf = self.spaceship_frames[self.spaceship_animation_index]
        self.spaceship_rect = self.spaceship_surf.get_rect(topleft=(0, 650))
    
    def spaceship_animate(self):
        self.spaceship_animation_index += 0.1
        if int(self.spaceship_animation_index) > 1:
            self.spaceship_animation_index = 0
        self.spaceship_surf = self.spaceship_frames[self.spaceship_animation_index]
        
        self.spaceship_rect.x += 5
        if self.spaceship_rect.left > 800:
            self.spaceship_rect.right = 0

    def update(self, event_info: EventInfo) -> None:
        for event in event_info["events"]:
            if event.type == pygame.USEREVENT:
                self.text_is_visible = not self.text_is_visible
            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                self.is_over = True
        
        self.spaceship_animate()
    
    def next_game_state(self) -> Any:
        return MainGame(self.screen)
    
    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

class MainGame(GameState):
    pass

class ResultScreen(GameState):
    pass