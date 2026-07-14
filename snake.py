"""
Snake Game

Author: Mohammad Reza Bakhshandeh
Year: 2026

A classic Snake game built with Python and Pygame.
"""

import pygame
import random
import os

pygame.init()
pygame.display.set_caption("🐍 Snake 🐍")

SNAKE_HEAD = [pygame.image.load(os.path.join("snake_head_U.jpg")),
              pygame.image.load(os.path.join("snake_head_R.jpg")),
              pygame.image.load(os.path.join("snake_head_D.jpg")),
              pygame.image.load(os.path.join("snake_head_L.jpg"))
              ]
FOOD = pygame.image.load(os.path.join("food.jpg"))

title_font = pygame.font.SysFont('arial', 50, bold=True)
font = pygame.font.SysFont('arial', 25)
small_font = pygame.font.SysFont('arial', 18)

# init colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 190, 20)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

GRID_SIZE = 10

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

# difficulty levels
SPEEDS = {
    'easy': 10,
    'medium': 20,
    'hard': 30
}
DIRECTIONS = {
    'UP': 0,
    'RIGHT': 1,
    'DOWN': 2,
    'LEFT': 3
}

class Snake:
    """Represents the player-controlled snake."""
    def __init__(self):
        self.size = 20

        self.snake_loc = []
        self.snake_len = 1
        self.snake_score = 0

        self.snake_direction = DIRECTIONS["RIGHT"]
        self.snake_difficulty = 'easy'

        self.loc_x = SCREEN_WIDTH // 2
        self.loc_y = SCREEN_HEIGHT // 2

        self.x_change = 0
        self.y_change = 0

    def update(self, user_input):
        """Update the snake's position based on keyboard input."""
        if user_input[pygame.K_w] or user_input[pygame.K_UP]:
            self.y_change = -GRID_SIZE
            self.x_change = 0
            self.snake_direction = DIRECTIONS["UP"]

        if user_input[pygame.K_a] or user_input[pygame.K_LEFT]:
            self.x_change = -GRID_SIZE
            self.y_change = 0
            self.snake_direction = DIRECTIONS["LEFT"]

        if user_input[pygame.K_s] or user_input[pygame.K_DOWN]:
            self.y_change = GRID_SIZE
            self.x_change = 0
            self.snake_direction = DIRECTIONS["DOWN"]

        if user_input[pygame.K_d] or user_input[pygame.K_RIGHT]:
            self.x_change = GRID_SIZE
            self.y_change = 0
            self.snake_direction = DIRECTIONS["RIGHT"]
            
        self.loc_x += self.x_change
        self.loc_y += self.y_change

        
        self.snake_loc.append([self.loc_x, self.loc_y])

        if len(self.snake_loc) > self.snake_len:
            del self.snake_loc[0]

    def eat(self, food):
        """Increase the snake length and score when food is collected."""
        snake_rect = pygame.Rect(self.snake_loc[-1][0], self.snake_loc[-1][1], self.size , self.size)
        rand_food = pygame.Rect(food.loc_x, food.loc_y, food.size, food.size)
        if snake_rect.colliderect(rand_food):
            food.update()
            self.snake_len += 1
            self.snake_score += 1

            
    def draw(self, screen):
        draw_text("Score= " + str(self.snake_score), font, RED, 70, 20)
        draw_text("Difficulty= " + str(self.snake_difficulty), font, RED, SCREEN_WIDTH-100, 20)
        pygame.draw.line(screen, RED, (0,40), (SCREEN_WIDTH,40), 5)
        pygame.draw.line(screen, RED, (0,40), (0, SCREEN_HEIGHT), 5)
        pygame.draw.line(screen, RED, (SCREEN_WIDTH-2,40), (SCREEN_WIDTH-2,SCREEN_HEIGHT), 5)
        pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH,SCREEN_HEIGHT-2), 5)
        
        for x,y in (self.snake_loc):
            main_rect = pygame.Rect(x, y, self.size , self.size)
            pygame.draw.rect(screen, GREEN, main_rect)
            screen.blit(SNAKE_HEAD[self.snake_direction], (x, y))

    def die(self):
        global game_over
        if self.snake_loc[-1][0] >= SCREEN_WIDTH-23 or self.snake_loc[-1][0] <= 2 \
        or self.snake_loc[-1][1] >= SCREEN_HEIGHT-23 or self.snake_loc[-1][1] <= 48:
            game_over = True


class Food:
    def __init__(self):
        self.size = 20
        self.loc_x = random.randrange(40, SCREEN_WIDTH-40, GRID_SIZE)
        self.loc_y = random.randrange(50, SCREEN_HEIGHT-40, GRID_SIZE)

    def update(self):
        self.loc_x = random.randrange(40, SCREEN_WIDTH-40, GRID_SIZE)
        self.loc_y = random.randrange(50, SCREEN_HEIGHT-40, GRID_SIZE)
                                    
    def draw(self, screen):
        screen.blit(FOOD, (self.loc_x, self.loc_y))

def draw_text(text, font_obj, color, x, y):
    screen_text = font_obj.render(text, True, color)
    screen_rect = screen_text.get_rect(center=(x, y))
    screen.blit(screen_text, screen_rect)

def draw_button(text, x, y, w, h, color, hover_color):
    """Draw an interactive button."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    # button text
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + w/2, y + h/2))
    screen.blit(text_surf, text_rect)
    
    return False

def game(difficulty):
    """Run the main game loop."""
    run = True
    player = Snake()
    food = Food()

    SPEED = SPEEDS[difficulty]
    player.snake_difficulty = difficulty
    global game_over
    game_over = False


    while run:
        if game_over:
            screen.fill(BLACK)
            draw_text("GAME OVER!", title_font, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-70)
            draw_text(f"Final Score: {player.snake_score}", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 -30)

            if draw_button("Play Again", SCREEN_WIDTH/2-130, SCREEN_HEIGHT/2, 120, 50, GREEN, DARK_GREEN):
                return difficulty
            if draw_button("Menu", SCREEN_WIDTH/2+10, SCREEN_HEIGHT/2, 120, 50, BLUE, (0, 0, 200)):
                return menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
        
        else:
            screen.fill(BLACK)

            user_input = pygame.key.get_pressed()
            
            player.update(user_input)
            player.draw(screen)
            player.eat(food)
            player.die()

            food.draw(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

        pygame.display.flip()
        clock.tick(SPEED)



def menu():
    while True:
        screen.fill(BLACK)
        
        # title
        draw_text(" SNAKE ", title_font, GREEN, SCREEN_WIDTH/2, 150)
        
        # buttons
        if draw_button("Easy", SCREEN_WIDTH/2 -150, SCREEN_HEIGHT/2 -70, 100, 50, GREEN, DARK_GREEN):
            return 'easy'
        if draw_button("Medium", SCREEN_WIDTH/2 -50, SCREEN_HEIGHT/2 -70, 100, 50, ORANGE, YELLOW):
            return 'medium'
        if draw_button("Hard", SCREEN_WIDTH/2 +50, SCREEN_HEIGHT/2 -70, 100, 50, RED, (200, 0, 0)):
            return 'hard'
        
        draw_text("Select Difficulty", font, GRAY, SCREEN_WIDTH/2, 200)
        
        # guide
        draw_text("Use Arrow Or WASD Keys to Move", small_font, GRAY, SCREEN_WIDTH/2, 350)
        draw_text("Press ESC to Return to Menu", small_font, GRAY, SCREEN_WIDTH/2, 380)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                raise SystemExit 

difficulty = menu()

while True:
    difficulty = game(difficulty)
