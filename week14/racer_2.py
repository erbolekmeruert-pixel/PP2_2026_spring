import random
import pygame

pygame.init()

WIDTH, HEIGHT = 480, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 28)
SMALL_FONT = pygame.font.SysFont("arial", 22)

GREEN = (34, 139, 34)
GRAY = (45, 45, 45)
WHITE = (255, 255, 255)
BLUE = (50, 130, 255)
RED = (220, 50, 50)
BLACK = (0, 0, 0)

CAR_GLASS = (180, 220, 255)
REAR_GLASS = (120, 160, 200)
HEADLIGHT = (255, 245, 120)
TAILLIGHT = (255, 70, 70)

ROAD_X = 90
ROAD_W = 300
LANES = 3
LANE_W = ROAD_W // LANES

PLAYER_W, PLAYER_H = 50, 90
ENEMY_W, ENEMY_H = 50, 90

COIN_TYPES = [
    {"weight": 1, "radius": 12, "color": (255, 215, 0)},
    {"weight": 2, "radius": 15, "color": (0, 200, 255)},
    {"weight": 3, "radius": 18, "color": (255, 100, 100)},
]

SPEED_UP_EVERY = 5


def lane_center(lane_index):
    return ROAD_X + lane_index * LANE_W + LANE_W // 2


def circle_rect_collision(cx, cy, radius, rect):
    nearest_x = max(rect.left, min(cx, rect.right))
    nearest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - nearest_x
    dy = cy - nearest_y
    return dx * dx + dy * dy <= radius * radius


def reset_game():
    return {
        "player": pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 120, PLAYER_W, PLAYER_H),
        "player_speed": 7,
        "enemies": [],
        "coins": [],
        "coins_collected": 0,
        "enemy_speed": 5,
        "road_offset": 0,
        "last_enemy_spawn": 0,
        "last_coin_spawn": 0,
        "game_over": False,
    }


def spawn_enemy(state):
    lane = random.randrange(LANES)
    x = lane_center(lane) - ENEMY_W // 2
    color = random.choice([(220, 50, 50), (255, 120, 0), (180, 0, 180)])
    state["enemies"].append(
        {"rect": pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H), "color": color}
    )


def spawn_coin(state):
    lane = random.randrange(LANES)
    coin_type = random.choices(COIN_TYPES, weights=[60, 30, 10], k=1)[0]
    state["coins"].append(
        {
            "x": lane_center(lane),
            "y": -20,
            "radius": coin_type["radius"],
            "weight": coin_type["weight"],
            "color": coin_type["color"],
        }
    )


def draw_car(rect, color, facing="up"):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

    if facing == "up":
        windshield = pygame.Rect(rect.x + 8, rect.y + 12, rect.w - 16, 22)
        rear_window = pygame.Rect(rect.x + 10, rect.bottom - 30, rect.w - 20, 12)
        head_y = rect.y + 10
        tail_y = rect.bottom - 10
    else:
        windshield = pygame.Rect(rect.x + 8, rect.bottom - 34, rect.w - 16, 22)
        rear_window = pygame.Rect(rect.x + 10, rect.y + 18, rect.w - 20, 12)
        head_y = rect.bottom - 10
        tail_y = rect.y + 10

    pygame.draw.rect(screen, CAR_GLASS, windshield, border_radius=4)
    pygame.draw.rect(screen, REAR_GLASS, rear_window, border_radius=4)

    pygame.draw.circle(screen, HEADLIGHT, (rect.x + 12, head_y), 4)
    pygame.draw.circle(screen, HEADLIGHT, (rect.right - 12, head_y), 4)
    pygame.draw.circle(screen, TAILLIGHT, (rect.x + 12, tail_y), 4)
    pygame.draw.circle(screen, TAILLIGHT, (rect.right - 12, tail_y), 4)


def draw_road(offset):
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_X, 0, ROAD_W, HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_X, 0, ROAD_W, HEIGHT), 4)

    for lane in range(1, LANES):
        x = ROAD_X + lane * LANE_W
        for y in range(-50 + offset, HEIGHT, 100):
            pygame.draw.line(screen, WHITE, (x, y), (x, y + 50), 5)


state = reset_game()
running = True

while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and state["game_over"]:
            if event.key == pygame.K_r:
                state = reset_game()

    keys = pygame.key.get_pressed()

    if not state["game_over"]:
        if keys[pygame.K_LEFT]:
            state["player"].x -= state["player_speed"]
        if keys[pygame.K_RIGHT]:
            state["player"].x += state["player_speed"]

        state["player"].x = max(
            ROAD_X + 5,
            min(state["player"].x, ROAD_X + ROAD_W - state["player"].w - 5)
        )

        if now - state["last_enemy_spawn"] > 900:
            spawn_enemy(state)
            state["last_enemy_spawn"] = now

        if now - state["last_coin_spawn"] > 1100:
            spawn_coin(state)
            state["last_coin_spawn"] = now

        state["enemy_speed"] = 5 + state["coins_collected"] // SPEED_UP_EVERY
        state["road_offset"] = (state["road_offset"] + state["enemy_speed"] * 2) % 100

        for enemy in state["enemies"][:]:
            enemy["rect"].y += state["enemy_speed"]
            if enemy["rect"].top > HEIGHT:
                state["enemies"].remove(enemy)
            elif enemy["rect"].colliderect(state["player"]):
                state["game_over"] = True

        for coin in state["coins"][:]:
            coin["y"] += 4
            if coin["y"] - coin["radius"] > HEIGHT:
                state["coins"].remove(coin)
            elif circle_rect_collision(coin["x"], coin["y"], coin["radius"], state["player"]):
                state["coins_collected"] += coin["weight"]
                state["coins"].remove(coin)

    draw_road(state["road_offset"])

    for coin in state["coins"]:
        pygame.draw.circle(screen, coin["color"], (coin["x"], int(coin["y"])), coin["radius"])
        label = SMALL_FONT.render(str(coin["weight"]), True, BLACK)
        screen.blit(label, label.get_rect(center=(coin["x"], int(coin["y"]))))

    for enemy in state["enemies"]:
        draw_car(enemy["rect"], enemy["color"], facing="down")

    draw_car(state["player"], BLUE, facing="up")

    coins_text = FONT.render(f"Coins: {state['coins_collected']}", True, WHITE)
    speed_text = SMALL_FONT.render(f"Enemy speed: {state['enemy_speed']}", True, WHITE)
    info_text = SMALL_FONT.render(f"Speed increases every {SPEED_UP_EVERY} coins", True, WHITE)

    screen.blit(coins_text, (15, 15))
    screen.blit(speed_text, (15, 48))
    screen.blit(info_text, (15, 75))

    if state["game_over"]:
        over = FONT.render("Game Over", True, RED)
        retry = SMALL_FONT.render("Press R to restart", True, WHITE)
        screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(retry, retry.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

    pygame.display.flip()

pygame.quit()
