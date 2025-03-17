import pygame
import time
import random

# إعداد الألوان
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# إعدادات النافذة
width = 600
height = 400

# حجم المربع في الثعبان
block_size = 10
speed = 15

# تهيئة اللعبة
pygame.init()
font = pygame.font.SysFont("bahnschrift", 25)
clock = pygame.time.Clock()

# إنشاء النافذة
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slang speel")


def display_message(msg, color, x, y):
    text = font.render(msg, True, color)
    window.blit(text, [x, y])


def game_loop():
    game_over = False
    game_close = False

    x = width / 2
    y = height / 2
    dx = 0
    dy = 0

    snake_body = []
    length = 1

    food_x = random.randrange(0, width - block_size, block_size)
    food_y = random.randrange(0, height - block_size, block_size)

    start_time = time.time()  # Starttijd om bij te houden wanneer de slang voor het laatst gegeten heeft
    time_limit = 20  # Tijdslimiet in seconden (20 seconden)

    while not game_over:
        while game_close:
            window.fill(black)
            display_message(f"Game over !  {length - 1} ", red, 150, height / 2 - 20)
            display_message("herstarten R of Q voor afsluiten ", red, 100, height / 2 + 20)
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
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -block_size
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = block_size

        x += dx
        y += dy

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        window.fill(black)
        pygame.draw.rect(window, green, [food_x, food_y, block_size, block_size])
        pygame.draw.rect(window, blue, [0, 0, width, block_size])  # جدار علوي
        pygame.draw.rect(window, blue, [0, height - block_size, width, block_size])  # جدار سفلي
        pygame.draw.rect(window, blue, [0, 0, block_size, height])  # جدار يساري
        pygame.draw.rect(window, blue, [width - block_size, 0, block_size, height])  # جدار يميني

        snake_head = [x, y]
        snake_body.append(snake_head)

        if len(snake_body) > length:
            del snake_body[0]

        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True

        for segment in snake_body:
            pygame.draw.rect(window, blue, [segment[0], segment[1], block_size, block_size])

        display_message(f": score {length - 1}", white, 10, 10)

        # حساب الوقت المتبقي
        time_elapsed = time.time() - start_time
        time_remaining = time_limit - int(time_elapsed)

        if time_remaining > 0:
            display_message(f"rest tijd: {time_remaining} Seconden", white, width - 200, 10)
        else:
            game_close = True
            display_message("Game over", red, 100, height / 2 + 40)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = random.randrange(0, width - block_size, block_size)
            food_y = random.randrange(0, height - block_size, block_size)
            length += 1
            start_time = time.time()  # Reset de timer bij het eten van voedsel

        clock.tick(speed)

    pygame.quit()
    quit()


game_loop()
