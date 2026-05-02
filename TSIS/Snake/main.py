import json
import sys
from pathlib import Path

import pygame

import db
from game import HEIGHT, SNAKE_COLORS, WIDTH, SnakeGame


SETTINGS_PATH = Path(__file__).with_name("settings.json")
DEFAULT_SETTINGS = {
    "snake_color": "green",
    "show_grid": True,
    "sound_enabled": True,
}

BACKGROUND = (233, 242, 247)
TEXT = (20, 20, 20)


class Button:
    def __init__(self, rect, label):
        self.rect = pygame.Rect(rect)
        self.label = label

    def draw(self, surface, font, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = (205, 228, 248) if hovered else (255, 255, 255)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, TEXT, self.rect, 2, border_radius=12)
        label = font.render(self.label, True, TEXT)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def load_settings():
    if not SETTINGS_PATH.exists():
        SETTINGS_PATH.write_text(json.dumps(DEFAULT_SETTINGS, indent=2), encoding="utf-8")
    data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    return {**DEFAULT_SETTINGS, **data}


def save_settings(settings):
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def draw_center(screen, text, font, y):
    surface = font.render(text, True, TEXT)
    screen.blit(surface, surface.get_rect(center=(WIDTH // 2, y)))


def draw_text_input(screen, rect, text, font):
    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=12)
    pygame.draw.rect(screen, TEXT, rect, 2, border_radius=12)
    shown = text if text else "Enter username..."
    color = TEXT if text else (130, 130, 130)
    screen.blit(font.render(shown, True, color), (rect.x + 12, rect.y + 10))


def cycle_option(options, current):
    index = options.index(current)
    return options[(index + 1) % len(options)]


def safe_init_db():
    try:
        db.init_db()
        return None
    except Exception as error:
        return str(error)


def safe_personal_best(username):
    try:
        return db.get_personal_best(username), None
    except Exception as error:
        return 0, str(error)


def safe_save_result(username, score, level):
    try:
        db.save_session(username, score, level)
        return None
    except Exception as error:
        return str(error)


def safe_top_scores():
    try:
        return db.get_top_scores(10), None
    except Exception as error:
        return [], str(error)


def draw_menu(screen, fonts, username, mouse_pos, buttons, db_error):
    screen.fill(BACKGROUND)
    draw_center(screen, "TSIS 4 Snake", fonts["title"], 80)
    

def draw_game_over(screen, fonts, result, mouse_pos, buttons, db_error):
    screen.fill(BACKGROUND)
    draw_center(screen, "Game Over", fonts["title"], 85)
    lines = [
        f"Player: {result.get('username', '-')}",
        f"Score: {result.get('score', 0)}",
        f"Level reached: {result.get('level', 1)}",
        f"Personal best: {result.get('personal_best', 0)}",
    ]
    for index, line in enumerate(lines):
        draw_center(screen, line, fonts["normal"], 170 + index * 42)
    if db_error:
        draw_center(screen, f"Database warning: {db_error}", fonts["small"], 360)
    for button in buttons.values():
        button.draw(screen, fonts["normal"], mouse_pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 4 Snake")
    clock = pygame.time.Clock()

    fonts = {
        "title": pygame.font.SysFont("Arial", 42),
        "normal": pygame.font.SysFont("Arial", 24),
        "small": pygame.font.SysFont("Arial", 18),
    }

    db_error = safe_init_db()
    settings = load_settings()
    username = ""
    state = "menu"
    game = None
    last_result = None
    leaderboard_rows = []
    leaderboard_error = None

    menu_buttons = {
        "play": Button((210, 240, 180, 46), "Play"),
        "leaderboard": Button((210, 300, 180, 46), "Leaderboard"),
        "settings": Button((210, 360, 180, 46), "Settings"),
        "quit": Button((210, 420, 180, 46), "Quit"),
    }

    settings_buttons = {
        "color": Button((320, 160, 170, 42), "Change Color"),
        "grid": Button((320, 230, 170, 42), "Toggle Grid"),
        "sound": Button((320, 300, 170, 42), "Toggle Sound"),
        "save_back": Button((210, 410, 180, 46), "Save & Back"),
    }

    leaderboard_back = Button((210, 650, 180, 42), "Back")
    game_over_buttons = {
        "retry": Button((210, 430, 180, 46), "Retry"),
        "menu": Button((210, 490, 180, 46), "Main Menu"),
    }

    running = True
    while running:
        dt_ms = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN and username.strip():
                        best, db_error = safe_personal_best(username.strip())
                        game = SnakeGame(username.strip(), settings, best)
                        state = "game"
                    elif event.unicode and event.unicode.isprintable() and len(username) < 16:
                        username += event.unicode

                if menu_buttons["play"].clicked(event) and username.strip():
                    best, db_error = safe_personal_best(username.strip())
                    game = SnakeGame(username.strip(), settings, best)
                    state = "game"
                elif menu_buttons["leaderboard"].clicked(event):
                    leaderboard_rows, leaderboard_error = safe_top_scores()
                    state = "leaderboard"
                elif menu_buttons["settings"].clicked(event):
                    state = "settings"
                elif menu_buttons["quit"].clicked(event):
                    running = False

            elif state == "settings":
                if settings_buttons["color"].clicked(event):
                    settings["snake_color"] = cycle_option(list(SNAKE_COLORS.keys()), settings["snake_color"])
                elif settings_buttons["grid"].clicked(event):
                    settings["show_grid"] = not settings["show_grid"]
                elif settings_buttons["sound"].clicked(event):
                    settings["sound_enabled"] = not settings["sound_enabled"]
                elif settings_buttons["save_back"].clicked(event):
                    save_settings(settings)
                    state = "menu"

            elif state == "leaderboard":
                if leaderboard_back.clicked(event):
                    state = "menu"

            elif state == "game":
                game.handle_event(event)

            elif state == "game_over":
                if game_over_buttons["retry"].clicked(event) and username.strip():
                    best, db_error = safe_personal_best(username.strip())
                    game = SnakeGame(username.strip(), settings, best)
                    state = "game"
                elif game_over_buttons["menu"].clicked(event):
                    state = "menu"

        if state == "menu":
            draw_menu(screen, fonts, username, mouse_pos, menu_buttons, db_error)

        elif state == "settings":
            draw_settings(screen, fonts, settings, mouse_pos, settings_buttons)

        elif state == "leaderboard":
            draw_leaderboard(screen, fonts, leaderboard_rows, mouse_pos, leaderboard_back, leaderboard_error)

        elif state == "game":
            result = game.update(dt_ms)
            game.draw(screen)
            if result is not None:
                save_error = safe_save_result(result["username"], result["score"], result["level"])
                best, best_error = safe_personal_best(result["username"])
                result["personal_best"] = max(result["personal_best"], best)
                db_error = save_error or best_error
                last_result = result
                state = "game_over"

        elif state == "game_over":
            draw_game_over(screen, fonts, last_result or {}, mouse_pos, game_over_buttons, db_error)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
    