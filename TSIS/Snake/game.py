import random
from collections import deque

import pygame


CELL = 25
COLS = 24
ROWS = 24
TOP_BAR = 110
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + TOP_BAR

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (28, 28, 28)
GRID = (55, 55, 55)
RED = (220, 60, 60)
YELLOW = (255, 215, 0)
CYAN = (70, 210, 240)
PINK = (255, 120, 160)
DARK_RED = (120, 20, 20)
PURPLE = (140, 90, 210)
BLUE = (65, 120, 225)
ORANGE = (255, 155, 60)
STONE = (120, 120, 120)

SNAKE_COLORS = {
    "green": (50, 185, 80),
    "blue": (50, 120, 210),
    "yellow": (235, 200, 70),
    "purple": (150, 95, 210),
}

FOOD_TYPES = [
    {"weight": 1, "color": YELLOW, "lifetime": 7000},
    {"weight": 2, "color": CYAN, "lifetime": 5200},
    {"weight": 3, "color": PINK, "lifetime": 3600},
]

POWERUP_TYPES = {
    "speed": {"color": ORANGE, "duration": 5000, "label": "Speed Boost"},
    "slow": {"color": BLUE, "duration": 5000, "label": "Slow Motion"},
    "shield": {"color": PURPLE, "duration": None, "label": "Shield"},
}


class SnakeGame:
    def __init__(self, username, settings, personal_best=0):
        self.username = username
        self.settings = settings
        self.personal_best = personal_best
        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.reset()

    def reset(self):
        self.snake = deque([(12, 12), (11, 12), (10, 12)])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.growth = 0
        self.now = 0
        self.last_move_at = 0
        self.last_powerup_spawn = 0
        self.obstacles = set()
        self.active_powerup = None
        self.powerup_ends_at = 0
        self.powerup_item = None
        self.food = None
        self.poison = None
        self.food = self.spawn_food(0)
        self.poison = self.spawn_poison()
        self.finished = False

    def valid_cells(self):
        return {(x, y) for x in range(COLS) for y in range(ROWS)}

    def occupied_cells(self, include_powerup=True):
        cells = set(self.snake) | set(self.obstacles)
        if self.food:
            cells.add(self.food["pos"])
        if self.poison:
            cells.add(self.poison["pos"])
        if include_powerup and self.powerup_item:
            cells.add(self.powerup_item["pos"])
        return cells

    def random_free_cell(self, extra_blocked=None):
        blocked = set(self.snake) | set(self.obstacles)
        if self.food:
            blocked.add(self.food["pos"])
        if self.poison:
            blocked.add(self.poison["pos"])
        if self.powerup_item:
            blocked.add(self.powerup_item["pos"])
        if extra_blocked:
            blocked |= set(extra_blocked)
        self.now += dt_ms
        self._clear_expired_items()

        if self.powerup_item is None and self.now - self.last_powerup_spawn >= 9000:
            self.powerup_item = self.spawn_powerup(self.now)
            self.last_powerup_spawn = self.now

        if self.now - self.last_move_at < self.move_delay():
            return None

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        hits_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
        hits_body = new_head in self._body_collision_cells()
        hits_obstacle = new_head in self.obstacles

        if hits_wall or hits_body or hits_obstacle:
            if self._consume_shield():
                self.last_move_at = self.now
                return None
            self.finished = True
            return {
                "username": self.username,
                "score": self.score,
                "level": self.level,
                "personal_best": max(self.personal_best, self.score),
            }

        self.snake.appendleft(new_head)
        ate_food = self.food and new_head == self.food["pos"]
        ate_poison = self.poison and new_head == self.poison["pos"]
        ate_powerup = self.powerup_item and new_head == self.powerup_item["pos"]

        if ate_food:
            self.score += self.food["weight"]
            self.growth += self.food["weight"]
            self.foods_eaten += 1
            self.food = self.spawn_food(self.now)
            self._handle_level_up()

        elif ate_poison:
            self._apply_poison()
            self.poison = self.spawn_poison()

        else:
            if self.growth > 0:
                self.growth -= 1
            else:
                self.snake.pop()

        if ate_powerup and self.powerup_item:
            self._activate_powerup(self.powerup_item["kind"])
            self.powerup_item = None

        self.personal_best = max(self.personal_best, self.score)
        self.last_move_at = self.now

        if self.finished:
            return {
                "username": self.username,
                "score": self.score,
                "level": self.level,
                "personal_best": self.personal_best,
            }
        return None

    def draw_cell(self, surface, color, cell, inset=2):
        x, y = cell
        rect = pygame.Rect(x * CELL + inset, TOP_BAR + y * CELL + inset, CELL - inset * 2, CELL - inset * 2)
        pygame.draw.rect(surface, color, rect, border_radius=6)

    def draw(self, surface):
        surface.fill(BG)
        pygame.draw.rect(surface, (245, 245, 245), (0, 0, WIDTH, TOP_BAR))
        pygame.draw.line(surface, BLACK, (0, TOP_BAR), (WIDTH, TOP_BAR), 2)

        if self.settings["show_grid"]:
            for x in range(COLS):
                for y in range(ROWS):
                    rect = pygame.Rect(x * CELL, TOP_BAR + y * CELL, CELL, CELL)
                    pygame.draw.rect(surface, GRID, rect, 1)

        for obstacle in self.obstacles:
            self.draw_cell(surface, STONE, obstacle, inset=1)

        for index, segment in enumerate(self.snake):
            color_name = self.settings["snake_color"]
            body_color = SNAKE_COLORS.get(color_name, SNAKE_COLORS["green"])
            head_color = tuple(min(255, c + 25) for c in body_color)
            self.draw_cell(surface, head_color if index == 0 else body_color, segment)

        if self.food:
            self.draw_cell(surface, self.food["color"], self.food["pos"], inset=3)

        if self.poison:
            self.draw_cell(surface, self.poison["color"], self.poison["pos"], inset=3)

        if self.powerup_item:
            self.draw_cell(surface, self.powerup_item["color"], self.powerup_item["pos"], inset=3)
            px = self.powerup_item["pos"][0] * CELL + CELL // 2
            py = TOP_BAR + self.powerup_item["pos"][1] * CELL + CELL // 2
            label = self.small_font.render(self.powerup_item["kind"][0].upper(), True, WHITE)
            surface.blit(label, label.get_rect(center=(px, py)))

        power_text = "None"
        if self.active_powerup:
            power_text = POWERUP_TYPES[self.active_powerup]["label"]
            if self.active_powerup in {"speed", "slow"}:
                seconds_left = max(0, (self.powerup_ends_at - self.now) // 1000 + 1)
                power_text += f" ({seconds_left}s)"
            else:
                power_text += " (until hit)"

        food_timer = max(0, (self.food["expires_at"] - self.now) // 1000 + 1) if self.food else 0

        lines = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
            f"Food weight: {self.food['weight'] if self.food else '-'}",
            f"Food timer: {food_timer}s",
            f"Power-up: {power_text}",
        ]
        for index, line in enumerate(lines):
            text = self.small_font.render(line, True, BLACK)
            surface.blit(text, (18 + (index // 4) * 280, 16 + (index % 4) * 22))