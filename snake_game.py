import pygame
import time
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Window settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Snake settings
BLOCK_SIZE = 10
SPEED = 15

# Initialize pygame
pygame.init()
FONT = pygame.font.SysFont("bahnschrift", 25)
CLOCK = pygame.time.Clock()

# Create window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize joystick (if available)
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Display text on screen
def display_message(msg, color, x, y):
    text = FONT.render(msg, True, color)
    window.blit(text, [x, y])

class Snake:
    """Represents the snake in the game, including movement and growth."""

    def __init__(self):
        self.body = []
        self.length = 1
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.dx = 0
        self.dy = 0

    def move(self):
        """Move the snake in the current direction."""
        self.x += self.dx
        self.y += self.dy
        self.body.append([self.x, self.y])
        if len(self.body) > self.length:
            del self.body[0]  # Remove oldest segment to keep correct length

    def draw(self, window):
        """Draw the snake on the window."""
        for segment in self.body:
            pygame.draw.rect(window, BLUE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

class Food:
    """Represents the food the snake can eat."""

    def __init__(self):
        self.x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        self.y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

    def draw(self, window):
        """Draw the food on the window."""
        pygame.draw.rect(window, GREEN, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    snake = Snake()
    food = Food()

    start_time = time.time()  # Track when the snake last ate
    time_limit = 20  # Time limit in seconds

    while not game_over:
        while game_close:
            window.fill(BLACK)
            display_message("Game Over", RED, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 40)
            display_message("R: Restart", GREEN, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 10)
            display_message("Q: Quit", RED, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 15)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.dx = -BLOCK_SIZE
                    snake.dy = 0
                elif event.key == pygame.K_RIGHT:
                    snake.dx = BLOCK_SIZE
                    snake.dy = 0
                elif event.key == pygame.K_UP:
                    snake.dx = 0
                    snake.dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    snake.dx = 0
                    snake.dy = BLOCK_SIZE

            # Handle joystick input (if available)
            if joystick_count > 0:
                x_axis = joystick.get_axis(0)
                y_axis = joystick.get_axis(1)

                if x_axis < -0.5:  # Left
                    snake.dx = -BLOCK_SIZE
                    snake.dy = 0
                elif x_axis > 0.5:  # Right
                    snake.dx = BLOCK_SIZE
                    snake.dy = 0
                elif y_axis < -0.5:  # Up
                    snake.dx = 0
                    snake.dy = -BLOCK_SIZE
                elif y_axis > 0.5:  # Down
                    snake.dx = 0
                    snake.dy = BLOCK_SIZE

        snake.move()

        # Check wall collision
        if snake.x >= SCREEN_WIDTH or snake.x < 0 or snake.y >= SCREEN_HEIGHT or snake.y < 0:
            game_close = True

        window.fill(BLACK)
        food.draw(window)

        # Draw walls
        pygame.draw.rect(window, BLUE, [0, 0, SCREEN_WIDTH, BLOCK_SIZE])  # Top wall
        pygame.draw.rect(window, BLUE, [0, SCREEN_HEIGHT - BLOCK_SIZE, SCREEN_WIDTH, BLOCK_SIZE])  # Bottom wall
        pygame.draw.rect(window, BLUE, [0, 0, BLOCK_SIZE, SCREEN_HEIGHT])  # Left wall
        pygame.draw.rect(window, BLUE, [SCREEN_WIDTH - BLOCK_SIZE, 0, BLOCK_SIZE, SCREEN_HEIGHT])  # Right wall

        snake.draw(window)

        # Countdown timer
        time_elapsed = time.time() - start_time
        time_remaining = time_limit - int(time_elapsed)

        display_message(f"Score: {snake.length - 1}", WHITE, 10, 10)

        if time_remaining > 0:
            display_message(f"Time Left: {time_remaining}", WHITE, SCREEN_WIDTH - 200, 10)
        else:
            game_close = True
            display_message("Game Over", RED, 100, SCREEN_HEIGHT / 2 + 40)

        pygame.display.update()

        # Snake eats food
        if snake.x == food.x and snake.y == food.y:
            food = Food()  # Generate new food
            snake.length += 1
            start_time = time.time()  # Reset timer

        CLOCK.tick(SPEED)

    pygame.quit()
    quit()

game_loop()
