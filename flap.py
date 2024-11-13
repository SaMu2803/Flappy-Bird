import pygame
import random
import os

pygame.init()

screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
sky_blue = (135, 206, 235)
green = (0, 255, 0)

gravity = 0.5
bird_movement = 0
bird_y = screen_height // 2
bird_x = screen_width // 4

pipe_width = 70
pipe_gap = random.randint(120, 180)
pipe_x = screen_width
pipe_velocity = 5
pipe_y = random.randint(100, screen_height - pipe_gap - 100)

score = 0
high_score = 0
font = pygame.font.Font(None, 36)

if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())

# Load images for background and bird (replace with your own image paths)
# sky_bg = pygame.image.load("sky_background.png")  # Optional, if you have a sky image
# land_bg = pygame.image.load("land_background.png")  # Optional, if you have a land image
# You can use the built-in colors for simplicity or load your own images as backgrounds.

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(sky_blue)

    pygame.draw.rect(screen, green, (0, screen_height - 100, screen_width, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -8

    bird_movement += gravity
    bird_y += bird_movement

    pipe_x -= pipe_velocity
    if pipe_x < -pipe_width:
        pipe_x = screen_width
        pipe_gap = random.randint(120, 180)
        pipe_y = random.randint(100, screen_height - pipe_gap - 100)
        score += 1
        if score > high_score:
            high_score = score

    if (bird_x + 30 > pipe_x and bird_x < pipe_x + pipe_width) and (
        bird_y < pipe_y or bird_y + 30 > pipe_y + pipe_gap
    ):
        running = False

    if bird_y > screen_height - 100 or bird_y < 0:
        running = False

    pygame.draw.ellipse(screen, blue, (bird_x - 15, bird_y - 15, 30, 30))

    pygame.draw.rect(screen, black, (pipe_x, 0, pipe_width, pipe_y))
    pygame.draw.rect(screen, black, (pipe_x, pipe_y + pipe_gap, pipe_width, screen_height))

    score_text = font.render(f"Score: {score}", True, black)
    high_score_text = font.render(f"High Score: {high_score}", True, black)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    pygame.display.update()
    clock.tick(30)

with open("high_score.txt", "w") as file:
    file.write(str(high_score))

pygame.quit()
