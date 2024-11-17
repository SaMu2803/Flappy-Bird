import pygame
import random
import os

pygame.init()

screen_width = 400
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

white = (255, 255, 255)
blue = (0, 0, 255)
sky_blue = (135, 206, 235)
green = (0, 255, 0)
black = (0, 0, 0)

gravity = 0.25
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

bg_image = pygame.image.load('sky_background.png')
land_image = pygame.image.load('land_background.png')
bird_image = pygame.image.load('bird_sprite.png')

bird_image = pygame.transform.scale(bird_image, (34, 24))
bird_rect = bird_image.get_rect(center=(bird_x, bird_y))

pipe_top_image = pygame.image.load('pipe_top.png')
pipe_bottom_image = pygame.image.load('pipe_bottom.png')
pipe_top_image = pygame.transform.scale(pipe_top_image, (pipe_width, 300))
pipe_bottom_image = pygame.transform.scale(pipe_bottom_image, (pipe_width, 300))

clock = pygame.time.Clock()

def show_game_over():
    game_over_font = pygame.font.Font(None, 50)
    game_over_text = game_over_font.render("Game Over", True, black)
    restart_button = pygame.font.Font(None, 36).render("Press R to Restart", True, black)
    score_text = pygame.font.Font(None, 36).render(f"Final Score: {score}", True, black)
    high_score_text = pygame.font.Font(None, 36).render(f"High Score: {high_score}", True, black)

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 40))
    screen.blit(restart_button, (screen_width // 2 - restart_button.get_width() // 2, screen_height // 2 + 100))

def restart_game():
    global bird_y, bird_movement, pipe_x, pipe_y, score, game_over
    bird_y = screen_height // 2
    bird_movement = 0
    pipe_x = screen_width
    pipe_y = random.randint(100, screen_height - pipe_gap - 100)
    score = 0
    game_over = False

running = True
game_over = False

while running:
    screen.fill(sky_blue)
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = -6.5
            elif event.key == pygame.K_r and game_over:
                restart_game()

    if not game_over:
        bird_movement += gravity
        bird_y += bird_movement
        bird_rect.centery = bird_y

        pipe_x -= pipe_velocity
        if pipe_x < -pipe_width:
            pipe_x = screen_width
            pipe_gap = random.randint(120, 180)
            pipe_y = random.randint(100, screen_height - pipe_gap - 100)
            score += 1
            if score > high_score:
                high_score = score

        pipe_top_rect = pipe_top_image.get_rect(topleft=(pipe_x, pipe_y - pipe_top_image.get_height()))
        pipe_bottom_rect = pipe_bottom_image.get_rect(topleft=(pipe_x, pipe_y + pipe_gap))

        if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            game_over = True

        if bird_y > screen_height - 100 or bird_y < 0:
            game_over = True

        screen.blit(land_image, (0, screen_height - 100))
        screen.blit(bird_image, bird_rect)
        screen.blit(pipe_top_image, pipe_top_rect)
        screen.blit(pipe_bottom_image, pipe_bottom_rect)

        score_text = font.render(f"Score: {score}", True, black)
        high_score_text = font.render(f"High Score: {high_score}", True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (screen_width - high_score_text.get_width() - 10, 10))

    if game_over:
        show_game_over()

    pygame.display.update()
    clock.tick(60)

with open("high_score.txt", "w") as file:
    file.write(str(high_score))

pygame.quit()
