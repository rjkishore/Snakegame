import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)  # Food color (white)
orange = (255, 165, 0)  # Snake head color (orange)
green = (0, 255, 0)  # Snake body color (green)
blue = (50, 153, 213)
yellow = (255, 255, 0)  # Bonus food color

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Mouth Animation")

# Clock
clock = pygame.time.Clock()

# Snake and food block sizes
block_size = 20
head_size = 25  # Make the snake head larger

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
title_font = pygame.font.SysFont("comicsansms", 35)

# Display the score
def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

# Snake structure (using circles)
def draw_snake(block_size, snake_list, eating, direction):
    for index, block in enumerate(snake_list):
        # Make the first block (head) larger and with a different color
        if index == len(snake_list) - 1:
            # Draw the head
            pygame.draw.circle(screen, orange, [block[0] + block_size // 2, block[1] + block_size // 2], head_size // 2)

            if eating:
                # Draw a mouth (triangle) to simulate eating
                mouth_size = head_size // 3
                mouth_color = green  # Mouth color matches snake body (green)

                if direction == "UP":
                    # Mouth opens upwards
                    pygame.draw.polygon(screen, mouth_color, [
                        (block[0] + block_size // 2, block[1] + block_size // 2),  # Center of the head
                        (block[0] + block_size // 2 - mouth_size, block[1] + block_size // 2 - mouth_size),  # Left corner
                        (block[0] + block_size // 2 + mouth_size, block[1] + block_size // 2 - mouth_size)   # Right corner
                    ])
                elif direction == "DOWN":
                    # Mouth opens downwards
                    pygame.draw.polygon(screen, mouth_color, [
                        (block[0] + block_size // 2, block[1] + block_size // 2),  # Center of the head
                        (block[0] + block_size // 2 - mouth_size, block[1] + block_size // 2 + mouth_size),  # Left corner
                        (block[0] + block_size // 2 + mouth_size, block[1] + block_size // 2 + mouth_size)   # Right corner
                    ])
                elif direction == "LEFT":
                    # Mouth opens to the left
                    pygame.draw.polygon(screen, mouth_color, [
                        (block[0] + block_size // 2, block[1] + block_size // 2),  # Center of the head
                        (block[0] + block_size // 2 - mouth_size, block[1] + block_size // 2 - mouth_size),  # Left corner
                        (block[0] + block_size // 2 - mouth_size, block[1] + block_size // 2 + mouth_size)   # Bottom left corner
                    ])
                elif direction == "RIGHT":
                    # Mouth opens to the right
                    pygame.draw.polygon(screen, mouth_color, [
                        (block[0] + block_size // 2, block[1] + block_size // 2),  # Center of the head
                        (block[0] + block_size // 2 + mouth_size, block[1] + block_size // 2 - mouth_size),  # Right corner
                        (block[0] + block_size // 2 + mouth_size, block[1] + block_size // 2 + mouth_size)   # Bottom right corner
                    ])
        else:
            pygame.draw.circle(screen, green, [block[0] + block_size // 2, block[1] + block_size // 2], block_size // 2)

# Message display
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + y_offset])

# Speed selection menu
def speed_menu():
    screen.fill(black)
    title = title_font.render("Select Game Speed", True, yellow)
    screen.blit(title, [width / 3, height / 4])

    message("Press S for Slow", white, 50)
    message("Press M for Medium", white, 100)
    message("Press F for Fast", white, 150)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return 10  # Slow speed
                elif event.key == pygame.K_m:
                    return 15  # Medium speed
                elif event.key == pygame.K_f:
                    return 20  # Fast speed

# Pause function
def game_pause():
    paused = True
    message("Game Paused. Press P to Resume", white)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# Game over screen with play again / quit option
def game_over_screen(score):
    screen.fill(black)
    message("Game Over", yellow, -50)
    message(f"Your Score: {score}", white, 0)
    message("Press P to Play Again or Q to Quit", white, 50)
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press P to play again
                    game_loop()
                if event.key == pygame.K_q:  # Press Q to quit
                    pygame.quit()
                    quit()

# Game loop
def game_loop():
    # Select speed before starting the game
    snake_speed = speed_menu()

    game_over = False

    # Snake initial position and direction
    x, y = width / 2, height / 2
    x_change, y_change = 0, 0
    current_direction = None  # Keeps track of current direction ('UP', 'DOWN', 'LEFT', 'RIGHT')

    # Snake structure
    snake_list = []
    length_of_snake = 1

    # Food position
    food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0

    # Bonus food logic
    bonus_food_x, bonus_food_y = None, None
    bonus_food_active = False
    bonus_food_spawn_time = pygame.time.get_ticks()
    bonus_food_lifetime = 5000  # Bonus food lifetime in milliseconds (5 seconds)

    # To control the mouth opening duration
    eating = False
    mouth_open_time = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Pause the game if 'P' is pressed
                    game_pause()
                # Restrict direction changes to valid moves
                if event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    x_change = -block_size
                    y_change = 0
                    current_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    x_change = block_size
                    y_change = 0
                    current_direction = "RIGHT"
                elif event.key == pygame.K_UP and current_direction != "DOWN":
                    y_change = -block_size
                    x_change = 0
                    current_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    y_change = block_size
                    x_change = 0
                    current_direction = "DOWN"

        # Implement screen wrapping behavior
        if x >= width:
            x = 0  # Wrap to the left side
        elif x < 0:
            x = width - block_size  # Wrap to the right side
        if y >= height:
            y = 0  # Wrap to the top
        elif y < 0:
            y = height - block_size  # Wrap to the bottom

        x += x_change
        y += y_change

        # Snake head
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Keep snake length
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if the snake collides with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        # Draw everything
        screen.fill(black)  # Background color is black
        pygame.draw.rect(screen, white, [food_x, food_y, block_size, block_size])  # Food color is white

        # Draw the snake
        draw_snake(block_size, snake_list, eating, current_direction)

        # Check if snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            length_of_snake += 1
            eating = True
            mouth_open_time = pygame.time.get_ticks()  # Record the time when the mouth opens

        # Close the mouth after a short time
        if eating and pygame.time.get_ticks() - mouth_open_time > 200:
            eating = False

        # Bonus food every 30 seconds
        if pygame.time.get_ticks() - bonus_food_spawn_time > 30000:  # 30 seconds
            bonus_food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            bonus_food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            bonus_food_active = True
            bonus_food_spawn_time = pygame.time.get_ticks()

        # Show bonus food for 5 seconds and blink every 500ms
        if bonus_food_active and pygame.time.get_ticks() - bonus_food_spawn_time < bonus_food_lifetime:
            if pygame.time.get_ticks() % 500 < 250:  # Blink every 500ms
                pygame.draw.rect(screen, yellow, [bonus_food_x, bonus_food_y, block_size, block_size])
        else:
            bonus_food_active = False  # Deactivate bonus food after 5 seconds

        # Check if snake eats the bonus food
        if x == bonus_food_x and y == bonus_food_y:
            length_of_snake += 3  # Increase the snake length more for bonus food
            bonus_food_active = False  # Deactivate bonus food

        display_score(length_of_snake - 1)

        pygame.display.update()

        clock.tick(snake_speed)

    game_over_screen(length_of_snake - 1)

# Start the game loop
game_loop()
pygame.quit()
quit()
