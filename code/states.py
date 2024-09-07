from abc import abstractmethod, ABC
import pygame
from event_info import EventInfo
from typing import Any
from player_class import Player
from enemy_class import Enemy
from laser_class import Laser
from explosion_class import Explosion
import random


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
        self.title_font = pygame.font.Font(
            "assets//PixelifySans-VariableFont_wght.ttf", 100
        )
        self.text_surf = self.title_font.render("Space Shooter", False, "white")
        self.text_rect = self.text_surf.get_rect(midtop=(400, 50))

        self.smaller_font = pygame.font.Font(
            "assets//PixelifySans-VariableFont_wght.ttf", 50
        )
        self.smaller_text_surf = self.smaller_font.render(
            "Press Enter To Begin", False, "white"
        )
        self.smaller_text_rect = self.smaller_text_surf.get_rect(midbottom=(400, 750))
        self.text_event = pygame.USEREVENT + 1
        self.text_timer = pygame.time.set_timer(self.text_event, 500)
        self.text_is_visible = True

        pygame.mixer.init()

        self.background_music = pygame.mixer.music.load("music//title_screen.wav")
        pygame.mixer.music.play(-1)

        self.spaceship_frames = [
            pygame.transform.scale(
                pygame.transform.rotate(
                    pygame.image.load(
                        "assets//player_spaceship//player_spaceship_fly_0.png"
                    ),
                    -90,
                ),
                (150, 150),
            ),
            pygame.transform.scale(
                pygame.transform.rotate(
                    pygame.image.load(
                        "assets//player_spaceship//player_spaceship_fly_1.png"
                    ),
                    -90,
                ),
                (150, 150),
            ),
        ]
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
        self.explosions = pygame.sprite.Group()

        self.spawn_rate = 1000  # Start with a 1-second spawn rate
        self.min_spawn_distance = 100  # Minimum distance between enemies
        self.last_spawn_time = pygame.time.get_ticks()

        pygame.mixer.init()

        self.background_music = pygame.mixer_music.load("music//main_game.wav")
        pygame.mixer_music.play(-1)

        self.score = 0
        self.score_font = pygame.font.Font(
            "assets//PixelifySans-VariableFont_wght.ttf", 50
        )
        self.score_text_surf = self.score_font.render(str(self.score), False, "white")
        self.score_text_rect = self.score_text_surf.get_rect(midtop=(400, 0))

    def update_spawn_rate(self) -> None:
        if self.score % 10 == 0 and self.score > 0:
            self.spawn_rate = max(300, int(self.spawn_rate * 0.9))  # Reduce spawn rate
            self.min_spawn_distance = min(200, self.min_spawn_distance + 10)  # Increase minimum distance

    def check_if_enemy_went_kaboom_or_made_it_through(self) -> None:
        for enemy in self.enemies:
            if enemy.rect.bottom >= 800 or enemy.rect.colliderect(self.player.rect):
                self.is_over = True
                break
            for laser in self.player.lasers:
                if laser.rect.colliderect(enemy.rect):
                    laser.kill()
                    self.explosions.add(Explosion(enemy.rect.center))
                    enemy.kill()
                    self.score += 1
                    self.score_text_surf = self.score_font.render(
                        str(self.score), False, "white"
                    )
                    self.score_text_rect = self.score_text_surf.get_rect(midtop=(400, 0))
                    break

    def check_to_add_new_enemy(self, event_info: EventInfo) -> None:
        current_time = pygame.time.get_ticks()

        if current_time - self.last_spawn_time >= self.spawn_rate:
            new_enemy_x = random.randint(50, 750)  # Random X position

            # Ensure no enemies are too close to the new one
            for enemy in self.enemies:
                if abs(new_enemy_x - enemy.rect.x) < self.min_spawn_distance:
                    return  # Skip spawning this enemy if too close

            self.enemies.add(Enemy())
            self.last_spawn_time = current_time  # Reset the spawn timer

    def update(self, event_info: EventInfo) -> None:
        self.player.update(event_info)
        self.enemies.update()
        self.explosions.update()
        self.update_spawn_rate()
        self.check_if_enemy_went_kaboom_or_made_it_through()
        self.check_to_add_new_enemy(event_info)
    
    def next_game_state(self) -> Any:
        return ResultScreen(self.screen, self.score)

    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.explosions.draw(self.screen)
        self.screen.blit(self.score_text_surf, self.score_text_rect)

class ResultScreen(GameState):
    def __init__(self, screen: pygame.Surface, score : int) -> None:
        super().__init__(screen)

        pygame.mixer.init()
        self.background_music = pygame.mixer_music.load("music//end_screen.wav")
        pygame.mixer_music.play(-1)
        
        self.play_again_font = pygame.font.Font("assets//PixelifySans-VariableFont_wght.ttf", 50)
        self.play_again_text_surf = self.play_again_font.render(
            "Press Enter To Play Again", False, "white"
        )
        self.play_again_text_rect = self.play_again_text_surf.get_rect(midbottom=(400, 750))
        self.text_event = pygame.USEREVENT + 1
        self.text_timer = pygame.time.set_timer(self.text_event, 500)
        self.text_is_visible = True

        self.title_font = pygame.font.Font("assets//PixelifySans-VariableFont_wght.ttf", 100)
        self.title_text_surf = self.title_font.render(f"Score: {score}", False, "white")
        self.title_rect = self.title_text_surf.get_rect(midtop=(400, 50))
    
    def update(self, event_info : EventInfo):
        for event in event_info["events"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.is_over = True
            elif event.type == self.text_event:
                self.text_is_visible = not self.text_is_visible
    
    def next_game_state(self) -> Any:
        return MainGame(self.screen)
    
    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_text_surf, self.title_rect)
        if self.text_is_visible:
            self.screen.blit(self.play_again_text_surf, self.play_again_text_rect)
