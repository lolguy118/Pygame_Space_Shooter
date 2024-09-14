import pygame
from states import TitleScreen, MainGame, ResultScreen
from event_info import EventInfo

class Game:
    
    SCREEN_SIZE = (800, 800)
    CLOCK = pygame.time.Clock()
    FPS_CAP = 60

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.current_game_state = TitleScreen(self.screen)
    def get_events(self) -> EventInfo:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        return {"events" : events, "mouse_pos" : mouse_pos, "keys" : keys}
    def run(self):
        while True:
            event_info = self.get_events()
            for event in event_info["events"]:
                if event.type == pygame.QUIT:
                    raise SystemExit
            
            self.screen.fill("black")
            self.current_game_state.update(event_info)
            if self.current_game_state.is_over:
                self.current_game_state = self.current_game_state.next_game_state()
            self.current_game_state.draw()
            pygame.display.update()
            self.CLOCK.tick(self.FPS_CAP)

if __name__ == "__main__":
    game = Game()
    game.run()