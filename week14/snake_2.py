import random
from collections import deque
import pygame

pygame.init()

CELL = 25
COLS, ROWS = 24, 24
TOP_BAR = 60
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + TOP_BAR

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 28)
SMALL_FONT = pygame.font.SysFont("arial", 22)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 180, 70)
DARK_GREEN = (20, 100, 40)
RED = (220, 60, 60)
BG = (25, 25, 25)

MOVE_DELAY = 120

FOOD_TYPES = [
    {"weight": 1, "color": (255, 215, 0), "lifetime": 7000},
    {"weight": 2, "color": (0, 210, 255), "lifetime": 5000},
    {"weight": 3, "color": (255, 90, 90), "lifetime": 3500},
]


def random_free_cell(snake):
    snake_set = set(snake)
    free_cells = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake_set]
    return random.choice(free_cells)


def spawn_food(snake):
    x, y = random_free_cell(snake)
    food_type = random.choices(FOOD_TYPES, weights=[60, 30, 10], k=1)[0]
    return {
        "pos": (x, y),
        "weight": food_type["weight"],
        "color": food_type["color"],
        "expires_at": pygame.time.get_ticks() + food_type["lifetime"],
    }


def reset_game():
    snake = deque([(12, 12), (11, 12), (10, 12)])
    return {
        "snake": snake,
        "direction": (1, 0),
        "next_direction": (1, 0),
        "growth": 0,
        "score": 0,
        "food": spawn_food(snake),
        "last_move": pygame.time.get_ticks(),
        "game_over": False,
    }


def draw_cell(color, pos, inset=2):
    x, y = pos
    rect = pygame.Rect(x * CELL + inset, TOP_BAR + y * CELL + inset, CELL - inset * 2, CELL - inset * 2)
    pygame.draw.rect(screen, color, rect, border_radius=6)


state = reset_game()
running = True

while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and state["direction"] != (0, 1):
                state["next_direction"] = (0, -1)
            elif event.key == pygame.K_DOWN and state["direction"] != (0, -1):
                state["next_direction"] = (0, 1)
            elif event.key == pygame.K_LEFT and state["direction"] != (1, 0):
                state["next_direction"] = (-1, 0)
            elif event.key == pygame.K_RIGHT and state["direction"] != (-1, 0):
                state["next_direction"] = (1, 0)
            elif event.key == pygame.K_r and state["game_over"]:
                state = reset_game()

    if not state["game_over"]:
        if now >= state["food"]["expires_at"]:
            state["food"] = spawn_food(state["snake"])

        if now - state["last_move"] >= MOVE_DELAY:
            state["direction"] = state["next_direction"]
            head_x, head_y = state["snake"][0]
            dx, dy = state["direction"]
            new_head = (head_x + dx, head_y + dy)

            out_of_bounds = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
            hits_self = new_head in state["snake"]

            if out_of_bounds or hits_self:
                state["game_over"] = True
            else:
                state["snake"].appendleft(new_head)

                if new_head == state["food"]["pos"]:
                    state["score"] += state["food"]["weight"]
                    state["growth"] += state["food"]["weight"]
                    state["food"] = spawn_food(state["snake"])
                else:
                    if state["growth"] > 0:
                        state["growth"] -= 1
                    else:
                        state["snake"].pop()

            state["last_move"] = now

    screen.fill(BG)

    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELL, TOP_BAR + y * CELL, CELL, CELL)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    for i, segment in enumerate(state["snake"]):
        draw_cell(GREEN if i == 0 else DARK_GREEN, segment)

    draw_cell(state["food"]["color"], state["food"]["pos"], inset=3)

    time_left = max(0, (state["food"]["expires_at"] - now) // 1000 + 1)
    score_text = FONT.render(f"Score: {state['score']}", True, WHITE)
    food_text = SMALL_FONT.render(f"Food weight: {state['food']['weight']}", True, WHITE)
    timer_text = SMALL_FONT.render(f"Disappears in: {time_left}s", True, WHITE)

    screen.blit(score_text, (12, 10))
    screen.blit(food_text, (180, 14))
    screen.blit(timer_text, (380, 14))

    if state["game_over"]:
        over = FONT.render("Game Over", True, RED)
        retry = SMALL_FONT.render("Press R to restart", True, WHITE)
        screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(retry, retry.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))

    pygame.display.flip()

pygame.quit()
