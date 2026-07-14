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
SCREEN_HIGHT = 640

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
clock = pygame.time.Clock()

# سطوح دشواری
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
    def __init__(self):
        self.size = 20

        self.snake_loc = []
        self.snake_len = 1
        self.snake_score = 0

        self.snake_direction = DIRECTIONS["RIGHT"]
        self.snake_difficulty = 'easy'

        self.loc_x = SCREEN_WIDTH // 2
        self.loc_y = SCREEN_HIGHT // 2

        self.x_change = 0
        self.y_change = 0

    def update(self, userInput):
        if userInput[pygame.K_w] or userInput[pygame.K_UP]:
            self.y_change = -10
            self.x_change = 0
            self.snake_direction = DIRECTIONS["UP"]

        if userInput[pygame.K_a] or userInput[pygame.K_LEFT]:
            self.x_change = -10
            self.y_change = 0
            self.snake_direction = DIRECTIONS["LEFT"]

        if userInput[pygame.K_s] or userInput[pygame.K_DOWN]:
            self.y_change = 10
            self.x_change = 0
            self.snake_direction = DIRECTIONS["DOWN"]

        if userInput[pygame.K_d] or userInput[pygame.K_RIGHT]:
            self.x_change = 10
            self.y_change = 0
            self.snake_direction = DIRECTIONS["RIGHT"]
            
        self.loc_x += self.x_change
        self.loc_y += self.y_change

        

        snake_Head = []
        snake_Head.append(self.loc_x)
        snake_Head.append(self.loc_y)
        self.snake_loc.append(snake_Head)

        if len(self.snake_loc)>self.snake_len:
            del self.snake_loc[0]

    def eat(self, SCREEN, food):
        snake_rect = pygame.Rect(self.snake_loc[-1][0], self.snake_loc[-1][1], self.size , self.size)
        rand_food = pygame.Rect(food.loc_x, food.loc_y, food.size, food.size)
        if snake_rect.colliderect(rand_food):
            pygame.draw.rect(SCREEN, (255,20,20), snake_rect)
            food.update()
            self.snake_len += 1
            self.snake_score += 1

            
    def draw(self, SCREEN):
        draw_text("Score= " + str(self.snake_score), font, RED, 70, 20)
        draw_text("Difficulty= " + str(self.snake_difficulty), font, RED, SCREEN_WIDTH-100, 20)
        pygame.draw.line(SCREEN, RED, (0,40), (SCREEN_WIDTH,40), 5)
        pygame.draw.line(SCREEN, RED, (0,40), (0, SCREEN_HIGHT), 5)
        pygame.draw.line(SCREEN, RED, (SCREEN_WIDTH-2,40), (SCREEN_WIDTH-2,SCREEN_HIGHT), 5)
        pygame.draw.line(SCREEN, RED, (0, SCREEN_HIGHT-2), (SCREEN_WIDTH,SCREEN_HIGHT-2), 5)
        for x,y in (self.snake_loc):
            
            main_rect = pygame.Rect(x, y, self.size , self.size)
            pygame.draw.rect(SCREEN, GREEN, main_rect)
            SCREEN.blit(SNAKE_HEAD[self.snake_direction], (x, y))

    def die(self):
        global game_over
        if self.snake_loc[-1][0] >= SCREEN_WIDTH-23 or self.snake_loc[-1][0] <= 2 \
        or self.snake_loc[-1][1] >= SCREEN_HIGHT-23 or self.snake_loc[-1][1] <= 48:
            game_over = True


class Food:
    def __init__(self):
        self.size = 20
        self.loc_x = random.randrange(40, SCREEN_WIDTH-40, 10)
        self.loc_y = random.randrange(50, SCREEN_HIGHT-40, 10)

    def update(self):
        self.loc_x = random.randrange(40, SCREEN_WIDTH-40, 10)
        self.loc_y = random.randrange(50, SCREEN_HIGHT-40, 10)
                                    
    def draw(self, SCREEN):
        SCREEN.blit(FOOD, (self.loc_x, self.loc_y))

def draw_text(text, font_obj, color, x, y):
    screen_text = font_obj.render(text, True, color)
    screen_rect = screen_text.get_rect(center=(x, y))
    SCREEN.blit(screen_text, screen_rect)

def draw_button(text, x, y, w, h, color, hover_color):
    """رسم دکمه"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(SCREEN, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(SCREEN, color, (x, y, w, h))
    
    # متن دکمه
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + w/2, y + h/2))
    SCREEN.blit(text_surf, text_rect)
    
    return False

def Game(difficulty):
    run = True
    player = Snake()
    food = Food()

    SPEED = SPEEDS[difficulty]
    player.snake_difficulty = difficulty
    global game_over
    game_over = False


    while run:
        if game_over:
            SCREEN.fill(BLACK)
            draw_text("GAME OVER!", title_font, RED, SCREEN_WIDTH/2, SCREEN_HIGHT/2-70)
            draw_text(f"Final Score: {player.snake_score}", font, WHITE, SCREEN_WIDTH/2, SCREEN_HIGHT/2 -30)

            if draw_button("Play Again", SCREEN_WIDTH/2-130, SCREEN_HIGHT/2, 120, 50, GREEN, DARK_GREEN):
                Game(difficulty)
            if draw_button("Menu", SCREEN_WIDTH/2+10, SCREEN_HIGHT/2, 120, 50, BLUE, (0, 0, 200)):
                Game(menu())
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    Game(difficulty)
        
        else:
            SCREEN.fill(BLACK)

            userInput = pygame.key.get_pressed()
            
            player.update(userInput)
            player.draw(SCREEN)
            player.eat(SCREEN, food)
            player.die()

            food.draw(SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # if event.type == pygame.K_ESCAPE:
                #     return

        pygame.display.flip()
        clock.tick(SPEED)



def menu():
    while True:
        SCREEN.fill(BLACK)
        
        # title
        draw_text(" SNAKE ", title_font, GREEN, SCREEN_WIDTH/2, 150)
        
        # bottoms
        if draw_button("Easy", SCREEN_WIDTH/2 -150, SCREEN_HIGHT/2 -70, 100, 50, GREEN, DARK_GREEN):
            return 'easy'
        if draw_button("Medium", SCREEN_WIDTH/2 -50, SCREEN_HIGHT/2 -70, 100, 50, ORANGE, YELLOW):
            return 'medium'
        if draw_button("Hard", SCREEN_WIDTH/2 +50, SCREEN_HIGHT/2 -70, 100, 50, RED, (200, 0, 0)):
            return 'hard'
        
        draw_text("Select Difficulty", font, GRAY, SCREEN_WIDTH/2, 200)
        
        # guide
        draw_text("Use Arrow Or WASD Keys to Move", small_font, GRAY, SCREEN_WIDTH/2, 350)
        draw_text("Press ESC to Return to Menu", small_font, GRAY, SCREEN_WIDTH/2, 380)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   

Game(menu())
