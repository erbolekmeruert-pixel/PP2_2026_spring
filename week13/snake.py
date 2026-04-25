import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont("Verdana", 24)
big_font = pygame.font.SysFont("Verdana", 48, bold=True)

WALL_COLOR = (80, 80, 80)

score = 0
level = 1
foods_eaten = 0
base_speed = 4
FPS = base_speed


def create_walls():
    walls = set()

    for x in range(COLS):
        walls.add((x, 0))
        walls.add((x, ROWS - 1))

    for y in range(ROWS):
        walls.add((0, y))
        walls.add((COLS - 1, y))

    return walls


walls = create_walls()


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, colorGRAY, (x * CELL, y * CELL, CELL, CELL), 1)


def draw_walls():
    for x, y in walls:
        pygame.draw.rect(screen, WALL_COLOR, (x * CELL, y * CELL, CELL, CELL))


def draw_info():
    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)
    speed_text = font.render(f"Speed: {FPS}", True, colorWHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(speed_text, (10, 70))


def show_game_over():
    text = big_font.render("GAME OVER", True, colorRED)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(2000)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.body = [Point(5, 5), Point(4, 5), Point(3, 5)]
        self.dx = 1
        self.dy = 0

    def set_direction(self, dx, dy):
        if self.dx == -dx and self.dy == -dy:
            return
        self.dx = dx
        self.dy = dy

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def grow(self):
        tail = self.body[-1]
        self.body.append(Point(tail.x, tail.y))

    def hits_wall_or_border(self):
        head = self.body[0]
        return (
            head.x < 0
            or head.x >= COLS
            or head.y < 0
            or head.y >= ROWS
            or (head.x, head.y) in walls
        )

    def hits_itself(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_food_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.grow()
            return True
        return False


class Food:
    def __init__(self, snake):
        self.pos = Point(0, 0)
        self.generate_random_pos(snake)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        while True:
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)

            on_snake = False
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    on_snake = True
                    break

            if not on_snake and (x, y) not in walls:
                self.pos = Point(x, y)
                break


clock = pygame.time.Clock()
snake = Snake()
food = Food(snake)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.set_direction(1, 0)
            elif event.key == pygame.K_LEFT:
                snake.set_direction(-1, 0)
            elif event.key == pygame.K_DOWN:
                snake.set_direction(0, 1)
            elif event.key == pygame.K_UP:
                snake.set_direction(0, -1)

    snake.move()

    if snake.hits_wall_or_border() or snake.hits_itself():
        screen.fill(colorBLACK)
        draw_grid()
        draw_walls()
        snake.draw()
        food.draw()
        draw_info()
        show_game_over()
        running = False
        continue

    if snake.check_food_collision(food):
        score += 1
        foods_eaten += 1
        food.generate_random_pos(snake)

        if foods_eaten % 4 == 0:
            level += 1
            FPS += 2

    screen.fill(colorBLACK)
    draw_grid()
    draw_walls()
    snake.draw()
    food.draw()
    draw_info()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
