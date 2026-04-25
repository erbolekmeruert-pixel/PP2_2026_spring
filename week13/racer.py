import pygame
import random

pygame.init()


WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 52, bold=True)


WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 180, 0)
RED = (220, 40, 40)
BLUE = (50, 100, 230)
YELLOW = (250, 220, 0)
SKY = (80, 200, 255)


ROAD_LEFT = 60
ROAD_RIGHT = WIDTH - 60
LANES = [120, 200, 280]


PLAYER_WIDTH = 50
PLAYER_HEIGHT = 85
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 85
player_speed = 6
enemy_speed = 5


COIN_RADIUS = 12
coins_collected = 0


player = pygame.Rect(LANES[1] - PLAYER_WIDTH // 2, HEIGHT - 120, PLAYER_WIDTH, PLAYER_HEIGHT)


enemies = []
coins = []

SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_ENEMY, 900)
pygame.time.set_timer(SPAWN_COIN, 1400)


line_offset = 0


def draw_road():
    
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    
    for lane_x in [160, 240]:
        for y in range(-40, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (lane_x - 4, y + line_offset, 8, 40))


def draw_car(rect, color):
    # Main car body
    pygame.draw.rect(screen, color, rect, border_radius=8)

    # Windows
    pygame.draw.rect(screen, SKY, (rect.x + 8, rect.y + 10, rect.width - 16, 18), border_radius=4)
    pygame.draw.rect(screen, SKY, (rect.x + 8, rect.y + 35, rect.width - 16, 18), border_radius=4)

    # Wheels
    pygame.draw.rect(screen, BLACK, (rect.x - 4, rect.y + 10, 8, 18), border_radius=3)
    pygame.draw.rect(screen, BLACK, (rect.right - 4, rect.y + 10, 8, 18), border_radius=3)
    pygame.draw.rect(screen, BLACK, (rect.x - 4, rect.y + rect.height - 28, 8, 18), border_radius=3)
    pygame.draw.rect(screen, BLACK, (rect.right - 4, rect.y + rect.height - 28, 8, 18), border_radius=3)


def draw_coin(coin):

    pygame.draw.circle(screen, YELLOW, (coin["x"], coin["y"]), COIN_RADIUS)
    pygame.draw.circle(screen, (240, 180, 0), (coin["x"], coin["y"]), COIN_RADIUS - 4)


def show_game_over():
    text = big_font.render("GAME OVER", True, RED)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

    info = font.render(f"Coins: {coins_collected}", True, WHITE)
    info_rect = info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(info, info_rect)

    pygame.display.flip()
    pygame.time.delay(2000)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
        elif event.type == SPAWN_ENEMY:
            lane_center = random.choice(LANES)
            enemy = pygame.Rect(
                lane_center - ENEMY_WIDTH // 2,
                -ENEMY_HEIGHT,
                ENEMY_WIDTH,
                ENEMY_HEIGHT
            )
            enemies.append(enemy)


        elif event.type == SPAWN_COIN:
            lane_center = random.choice(LANES)
            coins.append({"x": lane_center, "y": -COIN_RADIUS})


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed


    if player.x < ROAD_LEFT + 10:
        player.x = ROAD_LEFT + 10
    if player.x > ROAD_RIGHT - player.width - 10:
        player.x = ROAD_RIGHT - player.width - 10

    
    line_offset += enemy_speed
    if line_offset >= 80:
        line_offset = 0

    
    for enemy in enemies:
        enemy.y += enemy_speed

    
    for coin in coins:
        coin["y"] += enemy_speed

    
    enemies = [enemy for enemy in enemies if enemy.y < HEIGHT + 100]

    
    coins = [coin for coin in coins if coin["y"] < HEIGHT + COIN_RADIUS]

    
    for enemy in enemies:
        if player.colliderect(enemy):
            draw_road()
            draw_car(player, BLUE)
            for e in enemies:
                draw_car(e, RED)
            for coin in coins:
                draw_coin(coin)
            show_game_over()
            running = False

    
    for coin in coins[:]:
        coin_rect = pygame.Rect(
            coin["x"] - COIN_RADIUS,
            coin["y"] - COIN_RADIUS,
            COIN_RADIUS * 2,
            COIN_RADIUS * 2
        )
        if player.colliderect(coin_rect):
            coins.remove(coin)
            coins_collected += 1

            
            if coins_collected % 5 == 0:
                enemy_speed += 1

    
    draw_road()
    draw_car(player, BLUE)

    for enemy in enemies:
        draw_car(enemy, RED)

    for coin in coins:
        draw_coin(coin)

    
    coin_text = font.render(f"Coins: {coins_collected}", True, WHITE)
    screen.blit(coin_text, coin_text.get_rect(topright=(WIDTH - 15, 15)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
