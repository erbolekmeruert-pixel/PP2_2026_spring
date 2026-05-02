import random
from datetime import datetime

import pygame


WIDTH, HEIGHT = 560, 760
ROAD_X = 110
ROAD_WIDTH = 340
LANES = 3
LANE_WIDTH = ROAD_WIDTH // LANES

PLAYER_WIDTH, PLAYER_HEIGHT = 54, 96
TRAFFIC_WIDTH, TRAFFIC_HEIGHT = 54, 96
OBSTACLE_SIZE = 52
POWERUP_SIZE = 42

GREEN = (48, 148, 75)
ROAD = (52, 52, 52)
ROAD_LINE = (245, 245, 245)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
BLUE = (60, 110, 220)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (150, 90, 200)
CYAN = (70, 210, 240)
GRAY = (130, 130, 130)

COIN_TYPES = [
    {"value": 1, "radius": 11, "color": YELLOW},
    {"value": 2, "radius": 14, "color": CYAN},
    {"value": 3, "radius": 16, "color": (255, 110, 110)},
]

CAR_COLORS = {
    "blue": (60, 110, 220),
    "red": (215, 70, 70),
    "green": (55, 170, 95),
    "yellow": (240, 200, 60),
}

DIFFICULTY_PROFILES = {
    "easy": {
        "base_speed": 260,
        "traffic_spawn": 1350,
        "hazard_spawn": 1500,
        "coin_spawn": 900,
        "event_spawn": 3300,
        "powerup_spawn": 7800,
        "finish_distance": 2600,
    },
    "normal": {
        "base_speed": 320,
        "traffic_spawn": 1120,
        "hazard_spawn": 1280,
        "coin_spawn": 850,
        "event_spawn": 3000,
        "powerup_spawn": 7200,
        "finish_distance": 3400,
    },
    "hard": {
        "base_speed": 380,
        "traffic_spawn": 900,
        "hazard_spawn": 1120,
        "coin_spawn": 780,
        "event_spawn": 2700,
        "powerup_spawn": 6500,
        "finish_distance": 4200,
    },
}

POWERUP_DURATION_MS = {
    "nitro": 4500,
    "shield": None,
    "repair": None,
}


def lane_center(lane):
    return ROAD_X + lane * LANE_WIDTH + LANE_WIDTH // 2


def lane_rect(lane, y, width, height):
    return pygame.Rect(lane_center(lane) - width // 2, int(y), width, height)


def draw_car(surface, rect, color, facing="up"):
    glass = (190, 225, 255)
    rear_glass = (120, 165, 210)
    headlight = (255, 250, 150)
    taillight = (255, 90, 90)

    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10)

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

    pygame.draw.rect(surface, glass, windshield, border_radius=4)
    pygame.draw.rect(surface, rear_glass, rear_window, border_radius=4)
    pygame.draw.circle(surface, headlight, (rect.x + 12, head_y), 4)
    pygame.draw.circle(surface, headlight, (rect.right - 12, head_y), 4)
    pygame.draw.circle(surface, taillight, (rect.x + 12, tail_y), 4)
    pygame.draw.circle(surface, taillight, (rect.right - 12, tail_y), 4)


class RacerGame:
    def __init__(self, settings, username):
        self.settings = settings
        self.username = username
        self.profile = DIFFICULTY_PROFILES[settings["difficulty"]]
        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.reset()

    def reset(self):
        self.player_lane = 1
        self.player_rect = lane_rect(self.player_lane, HEIGHT - 140, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.coins = []
        self.traffic = []
        self.hazards = []
        self.events = []
        self.powerups = []
        self.coins_collected = 0
        self.distance = 0.0
        self.score = 0
        self.score_bonus = 0
        self.scroll_offset = 0.0
        self.now = 0
        self.last_coin_spawn = 0
        self.last_traffic_spawn = 0
        self.last_hazard_spawn = 0
        self.last_event_spawn = 0
        self.last_powerup_spawn = 0
        self.active_powerup = None
        self.powerup_ends_at = 0
        self.slow_until = 0
        self.event_boost_until = 0
        self.hit_flash_until = 0
        self.finished = False
        self.victory = False

    def _progress_ratio(self):
        return min(1.0, self.distance / self.profile["finish_distance"])

    def _current_speed(self):
        base = self.profile["base_speed"]
        base += (self.coins_collected // 5) * 18
        base += int(self._progress_ratio() * 110)

        if self.now < self.slow_until:
            base *= 0.68
        if self.active_powerup == "nitro" and self.now < self.powerup_ends_at:
            base *= 1.45
        if self.now < self.event_boost_until:
            base *= 1.2
        return base

    def _safe_spawn_lanes(self):
        blocked = set()
        for collection in (self.traffic, self.hazards, self.events, self.powerups):
            for item in collection:
                if item["y"] < 220:
                    blocked.add(item["lane"])

        choices = [lane for lane in range(LANES) if lane not in blocked]
        if not choices:
            choices = list(range(LANES))

        if self.player_lane in choices and len(choices) > 1:
            choices.remove(self.player_lane)
        return choices

    def _spawn_coin(self):
        lane = random.choice(self._safe_spawn_lanes())
        coin = random.choices(COIN_TYPES, weights=[60, 30, 10], k=1)[0]
        self.coins.append(
            {
                "lane": lane,
                "y": -30,
                "radius": coin["radius"],
                "value": coin["value"],
                "color": coin["color"],
            }
        )

    def _spawn_traffic(self):
        lane = random.choice(self._safe_spawn_lanes())
        self.traffic.append(
            {
                "lane": lane,
                "y": -TRAFFIC_HEIGHT - 20,
                "color": random.choice([RED, ORANGE, PURPLE, CYAN]),
            }
        )

    def _spawn_hazard(self):
        lane = random.choice(self._safe_spawn_lanes())
        kind = random.choice(["barrier", "pothole", "oil"])
        self.hazards.append({"lane": lane, "y": -OBSTACLE_SIZE - 20, "kind": kind})

    def _spawn_event(self):
        lane = random.randrange(LANES)
        kind = random.choice(["moving_barrier", "speed_bump", "boost_strip"])
        item = {"lane": lane, "y": -88, "kind": kind}
        if kind == "moving_barrier":
            item["direction"] = random.choice([-1, 1])
            item["last_shift"] = self.now
        self.events.append(item)

    def _spawn_powerup(self):
        lane = random.choice(self._safe_spawn_lanes())
        kind = random.choice(["nitro", "shield", "repair"])
        self.powerups.append(
            {
                "lane": lane,
                "y": -POWERUP_SIZE - 20,
                "kind": kind,
                "expires_at": self.now + 6500,
            }
        )

    def _activate_powerup(self, kind):
        self.active_powerup = kind
        duration = POWERUP_DURATION_MS[kind]
        self.powerup_ends_at = self.now + duration if duration else 0
        self.score_bonus += 40

    def _consume_protection(self, source_kind):
        if self.active_powerup == "shield":
            self.active_powerup = None
            self.powerup_ends_at = 0
            self.hit_flash_until = self.now + 250
            self.score_bonus += 25
            return True

        if self.active_powerup == "repair" and source_kind in {"barrier", "pothole", "moving_barrier"}:
            self.active_powerup = None
            self.powerup_ends_at = 0
            self.hit_flash_until = self.now + 250
            self.score_bonus += 20
            return True

        return False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.player_lane = max(0, self.player_lane - 1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.player_lane = min(LANES - 1, self.player_lane + 1)

    def _update_player_rect(self):
        self.player_rect = lane_rect(self.player_lane, HEIGHT - 140, PLAYER_WIDTH, PLAYER_HEIGHT)

    def _move_entities(self, speed, dt_seconds):
        delta = speed * dt_seconds
        self.scroll_offset = (self.scroll_offset + delta * 0.35) % 100

        for coin in self.coins:
            coin["y"] += delta

        for car in self.traffic:
            car["y"] += delta * 1.05

        for hazard in self.hazards:
            hazard["y"] += delta

        for event in self.events:
            event["y"] += delta
            if event["kind"] == "moving_barrier" and self.now - event["last_shift"] >= 380:
                event["lane"] += event["direction"]
                if event["lane"] <= 0 or event["lane"] >= LANES - 1:
                    event["lane"] = max(0, min(LANES - 1, event["lane"]))
                    event["direction"] *= -1
                event["last_shift"] = self.now

        for item in self.powerups:
            item["y"] += delta

        self.coins = [coin for coin in self.coins if coin["y"] - coin["radius"] <= HEIGHT + 40]
        self.traffic = [car for car in self.traffic if car["y"] <= HEIGHT + 120]
        self.hazards = [hazard for hazard in self.hazards if hazard["y"] <= HEIGHT + 120]
        self.events = [event for event in self.events if event["y"] <= HEIGHT + 120]
        self.powerups = [
            item
            for item in self.powerups
            if item["y"] <= HEIGHT + 80 and self.now <= item["expires_at"]
        ]

    def _collision_rect(self, lane, y, kind):
        if kind == "traffic":
            return lane_rect(lane, y, TRAFFIC_WIDTH, TRAFFIC_HEIGHT)
        if kind in {"barrier", "pothole"}:
            return lane_rect(lane, y, OBSTACLE_SIZE, OBSTACLE_SIZE)
        if kind == "moving_barrier":
            return lane_rect(lane, y, 72, 42)
        if kind == "oil":
            return lane_rect(lane, y, 62, 34)
        if kind == "speed_bump":
            return lane_rect(lane, y, 70, 22)
        if kind == "boost_strip":
            return lane_rect(lane, y, 70, 26)
        if kind in {"nitro", "shield", "repair"}:
            return lane_rect(lane, y, POWERUP_SIZE, POWERUP_SIZE)
        return lane_rect(lane, y, 20, 20)

    def _handle_collections_and_collisions(self):
        for coin in self.coins[:]:
            coin_rect = self._collision_rect(coin["lane"], coin["y"], "coin")
            if self.player_rect.colliderect(coin_rect):
                self.coins_collected += coin["value"]
                self.score_bonus += coin["value"] * 12
                self.coins.remove(coin)

        for item in self.powerups[:]:
            item_rect = self._collision_rect(item["lane"], item["y"], item["kind"])
            if self.player_rect.colliderect(item_rect):
                if self.active_powerup is None:
                    self._activate_powerup(item["kind"])
                self.powerups.remove(item)

        for car in self.traffic[:]:
            rect = self._collision_rect(car["lane"], car["y"], "traffic")
            if self.player_rect.colliderect(rect):
                if self._consume_protection("traffic"):
                    self.traffic.remove(car)
                else:
                    self.finished = True
                    self.victory = False
                    return

        for hazard in self.hazards[:]:
            rect = self._collision_rect(hazard["lane"], hazard["y"], hazard["kind"])
            if self.player_rect.colliderect(rect):
                if hazard["kind"] == "oil":
                    self.slow_until = max(self.slow_until, self.now + 2200)
                    self.hazards.remove(hazard)
                elif self._consume_protection(hazard["kind"]):
                    self.hazards.remove(hazard)
                else:
                    self.finished = True
                    self.victory = False
                    return

        for event in self.events[:]:
            rect = self._collision_rect(event["lane"], event["y"], event["kind"])
            if self.player_rect.colliderect(rect):
                if event["kind"] == "speed_bump":
                    self.slow_until = max(self.slow_until, self.now + 1800)
                    self.events.remove(event)
                elif event["kind"] == "boost_strip":
                    self.event_boost_until = max(self.event_boost_until, self.now + 1800)
                    self.score_bonus += 18
                    self.events.remove(event)
                elif self._consume_protection(event["kind"]):
                    self.events.remove(event)
                else:
                    self.finished = True
                    self.victory = False
                    return

    def _build_result(self):
        return {
            "name": self.username,
            "score": int(self.score),
            "distance": int(self.distance),
            "coins": self.coins_collected,
            "difficulty": self.settings["difficulty"],
            "result": "Finished" if self.victory else "Game Over",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def update(self, dt_ms):
        if self.finished:
            return self._build_result()

        self.now += dt_ms
        if self.active_powerup == "nitro" and self.powerup_ends_at and self.now >= self.powerup_ends_at:
            self.active_powerup = None
            self.powerup_ends_at = 0

        self._update_player_rect()
        speed = self._current_speed()
        dt_seconds = dt_ms / 1000
        self.distance += speed * dt_seconds * 0.45
        self.score = self.coins_collected * 35 + self.distance + self.score_bonus

        if self.distance >= self.profile["finish_distance"]:
            self.finished = True
            self.victory = True
            return self._build_result()

        progress = self._progress_ratio()

        traffic_spawn_ms = max(380, self.profile["traffic_spawn"] - int(progress * 300))
        hazard_spawn_ms = max(520, self.profile["hazard_spawn"] - int(progress * 260))
        event_spawn_ms = max(2000, self.profile["event_spawn"] - int(progress * 400))

        if self.now - self.last_coin_spawn >= self.profile["coin_spawn"]:
            self._spawn_coin()
            self.last_coin_spawn = self.now

        if self.now - self.last_traffic_spawn >= traffic_spawn_ms:
            self._spawn_traffic()
            self.last_traffic_spawn = self.now

        if self.now - self.last_hazard_spawn >= hazard_spawn_ms:
            self._spawn_hazard()
            self.last_hazard_spawn = self.now

        if self.now - self.last_event_spawn >= event_spawn_ms:
            self._spawn_event()
            self.last_event_spawn = self.now

        if (
            self.active_powerup is None
            and not self.powerups
            and self.now - self.last_powerup_spawn >= self.profile["powerup_spawn"]
        ):
            self._spawn_powerup()
            self.last_powerup_spawn = self.now

        self._move_entities(speed, dt_seconds)
        self._handle_collections_and_collisions()

        if self.finished:
            return self._build_result()
        return None

    def _draw_road(self, surface):
        surface.fill(GREEN)
        pygame.draw.rect(surface, ROAD, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(surface, WHITE, (ROAD_X, 0, ROAD_WIDTH, HEIGHT), 4)

        for lane in range(1, LANES):
            x = ROAD_X + lane * LANE_WIDTH
            for y in range(-50 + int(self.scroll_offset), HEIGHT, 100):
                pygame.draw.line(surface, ROAD_LINE, (x, y), (x, y + 50), 5)

    def _draw_coin(self, surface, coin):
        center = (lane_center(coin["lane"]), int(coin["y"]))
        pygame.draw.circle(surface, coin["color"], center, coin["radius"])
        label = self.small_font.render(str(coin["value"]), True, BLACK)
        surface.blit(label, label.get_rect(center=center))

    def _draw_hazard(self, surface, hazard):
        rect = self._collision_rect(hazard["lane"], hazard["y"], hazard["kind"])
        if hazard["kind"] == "barrier":
            pygame.draw.rect(surface, ORANGE, rect, border_radius=8)
            pygame.draw.line(surface, WHITE, rect.topleft, rect.bottomright, 4)
            pygame.draw.line(surface, WHITE, rect.topright, rect.bottomleft, 4)
        elif hazard["kind"] == "pothole":
            pygame.draw.ellipse(surface, BLACK, rect)
            pygame.draw.ellipse(surface, GRAY, rect, 3)
        elif hazard["kind"] == "oil":
            pygame.draw.ellipse(surface, (25, 25, 25), rect)
            pygame.draw.circle(surface, (55, 55, 55), rect.center, 8)

    def _draw_event(self, surface, event):
        rect = self._collision_rect(event["lane"], event["y"], event["kind"])
        if event["kind"] == "moving_barrier":
            pygame.draw.rect(surface, RED, rect, border_radius=8)
            pygame.draw.line(surface, WHITE, rect.midleft, rect.midright, 4)
        elif event["kind"] == "speed_bump":
            pygame.draw.rect(surface, YELLOW, rect, border_radius=4)
            pygame.draw.line(surface, BLACK, rect.midleft, rect.midright, 3)
        elif event["kind"] == "boost_strip":
            pygame.draw.rect(surface, CYAN, rect, border_radius=4)
            for offset in range(0, rect.w, 10):
                pygame.draw.line(surface, WHITE, (rect.x + offset, rect.y), (rect.x + offset - 6, rect.bottom), 2)

    def _draw_powerup(self, surface, item):
        rect = self._collision_rect(item["lane"], item["y"], item["kind"])
        color_map = {"nitro": CYAN, "shield": BLUE, "repair": GREEN}
        pygame.draw.rect(surface, color_map[item["kind"]], rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=10)
        label = self.small_font.render(item["kind"][0].upper(), True, WHITE)
        surface.blit(label, label.get_rect(center=rect.center))

    def _draw_hud(self, surface):
        panel = pygame.Rect(12, 12, 270, 148)
        pygame.draw.rect(surface, WHITE, panel, border_radius=14)
        pygame.draw.rect(surface, BLACK, panel, 2, border_radius=14)

        remaining = max(0, int(self.profile["finish_distance"] - self.distance))
        power_text = "None"
        if self.active_powerup == "nitro":
            left = max(0, (self.powerup_ends_at - self.now) // 1000 + 1)
            power_text = f"Nitro ({left}s)"
        elif self.active_powerup == "shield":
            power_text = "Shield (until hit)"
        elif self.active_powerup == "repair":
            power_text = "Repair (next obstacle)"

        lines = [
            f"Driver: {self.username}",
            f"Coins: {self.coins_collected}",
            f"Score: {int(self.score)}",
            f"Distance: {int(self.distance)}",
            f"Remaining: {remaining}",
            f"Power-up: {power_text}",
            f"Difficulty: {self.settings['difficulty'].title()}",
        ]

        for index, line in enumerate(lines):
            text = self.small_font.render(line, True, BLACK)
            surface.blit(text, (24, 24 + index * 18))

    def draw(self, surface):
        self._draw_road(surface)

        for coin in self.coins:
            self._draw_coin(surface, coin)

        for hazard in self.hazards:
            self._draw_hazard(surface, hazard)

        for event in self.events:
            self._draw_event(surface, event)

        for car in self.traffic:
            rect = self._collision_rect(car["lane"], car["y"], "traffic")
            draw_car(surface, rect, car["color"], facing="down")

        for item in self.powerups:
            self._draw_powerup(surface, item)

        player_color = CAR_COLORS.get(self.settings["car_color"], BLUE)
        draw_car(surface, self.player_rect, player_color, facing="up")

        if self.now < self.hit_flash_until:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 60))
            surface.blit(flash, (0, 0))

        self._draw_hud(surface)
