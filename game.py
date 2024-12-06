import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Ball class
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move_up(self):
        self.y -= 5

# Game class
class Game:
    def __init__(self):
        self.level = 1
        self.level_times = {1: 3, 2: 4, 3: 5, 4: 7, 5: 8}  # Define time limits for each level
        self.time_left = self.level_times[self.level]
        self.balls = []
        self.running = False
        self.paused = False
        self.start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
        self.font = pygame.font.SysFont("Arial", 30)
        self.clock = pygame.time.Clock()
        self.yellow_line_y = HEIGHT - 50  # Initial yellow line position
        self.game_over = False

    def create_balls(self):
        """Create five balls with random positions and colors."""
        self.balls = []
        radius = 20  # Set all balls to the same size
        for _ in range(5):
            color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE])
            x = random.randint(radius, WIDTH - radius)
            y = HEIGHT - radius  # Balls start at the bottom
            ball = Ball(x, y, radius, color)
            self.balls.append(ball)

    def update(self):
        """Update the game state."""
        if not self.paused and not self.game_over:
            self.time_left -= 1 / FPS
            if self.time_left <= 0:
                self.failed_screen()

            if all(ball.y <= self.yellow_line_y for ball in self.balls):
                self.next_level()

    def draw(self):
        """Draw the game elements on the screen."""
        screen.fill((97, 92, 92))
        for ball in self.balls:
            ball.draw(screen)

        # Draw yellow line for level progress
        pygame.draw.line(screen, YELLOW, (0, self.yellow_line_y), (WIDTH, self.yellow_line_y), 5)

        # Draw level and time left
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        time_text = self.font.render(f"Time Left: {int(self.time_left)}s", True, BLACK)
        screen.blit(level_text, (10, 10))
        screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

        # Start button screen
        if not self.running:
            pygame.draw.rect(screen, (0, 255, 0), self.start_button_rect)
            start_text = self.font.render("Start Game", True, BLACK)
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 25))

        # Game Over screen
        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, BLACK)

            failed_text = self.font.render(f"Level Reached: {self.level}", True, BLACK)
            instructions = self.font.render("Press ENTER to Restart or ESC to Exit", True, BLACK)
            screen.blit(failed_text, (WIDTH // 2 - failed_text.get_width() // 2, HEIGHT // 3 + 50))
            screen.blit(game_over_text,(WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))  # Offset vertically
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    def handle_key_event(self, event):
        """Handle key events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.paused:
                for ball in self.balls:
                    ball.move_up()
            elif event.key == pygame.K_p and not self.paused:
                self.paused = True
            elif event.key == pygame.K_r and self.paused:
                self.paused = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:  # Enter key works everywhere
                if self.game_over:
                    self.reset_game()
                if not self.running:
                    self.start_game()

    def handle_mouse_event(self, event):
        """Handle mouse events, especially clicking the start button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos) and not self.running:
                self.start_game()

    def start_game(self):
        """Start the game when the start button is clicked."""
        self.running = True
        self.create_balls()

    def next_level(self):
        """Move to the next level and increase the yellow line position."""
        if self.level < 5:
            self.level += 1
            self.time_left = self.level_times.get(self.level, 5)  # Adjust time for each level
            self.yellow_line_y -= 50  # Move the yellow line higher for difficulty
            self.create_balls()
        else:
            self.game_over = True

    def failed_screen(self):
        """Display the failed screen when time runs out."""
        self.game_over = True

    def reset_game(self):
        """Reset the game to its initial state."""
        self.level = 1
        self.time_left = self.level_times[self.level]
        self.yellow_line_y = HEIGHT - 50
        self.create_balls()
        self.running = False
        self.paused = False
        self.game_over = False

# Main game loop
def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.handle_key_event(event)
            game.handle_mouse_event(event)

        if game.running:
            game.update()
            game.draw()
        else:
            game.draw()  # Draw the start screen with the start button

        pygame.display.update()
        game.clock.tick(FPS)

if __name__ == "__main__":
    main()
