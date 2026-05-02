import sys

import pygame

from persistence import add_leaderboard_entry, load_leaderboard, load_settings, save_settings
from racer import CAR_COLORS, HEIGHT, WIDTH, RacerGame
from ui import Button, draw_center_text, draw_text_input


BACKGROUND = (235, 244, 252)
TEXT = (20, 20, 20)


def cycle_option(options, current, direction=1):
    index = options.index(current)
    return options[(index + direction) % len(options)]


def draw_menu(screen, fonts, username, input_active, mouse_pos, buttons):
    screen.fill(BACKGROUND)
    draw_center_text(screen, "TSIS 3 Racer", fonts["title"], TEXT, (WIDTH // 2, 90))
    draw_center_text(screen, "Enter your name before starting", fonts["small"], TEXT, (WIDTH // 2, 130))
    draw_text_input(screen, pygame.Rect(140, 160, 280, 46), username, fonts["normal"], input_active)

    for button in buttons.values():
        button.draw(screen, fonts["normal"], mouse_pos)


def draw_settings(screen, fonts, settings, mouse_pos, buttons):
    screen.fill(BACKGROUND)
    draw_center_text(screen, "Settings", fonts["title"], TEXT, (WIDTH // 2, 80))

    lines = [
        f"Sound: {'On' if settings['sound_enabled'] else 'Off'}",
        f"Car color: {settings['car_color'].title()}",
        f"Difficulty: {settings['difficulty'].title()}",
    ]

    for index, line in enumerate(lines):
        text = fonts["normal"].render(line, True, TEXT)
        screen.blit(text, (140, 170 + index * 70))

    for button in buttons.values():
        button.draw(screen, fonts["normal"], mouse_pos)


def draw_leaderboard(screen, fonts, entries, mouse_pos, back_button):
    screen.fill(BACKGROUND)
    draw_center_text(screen, "Leaderboard", fonts["title"], TEXT, (WIDTH // 2, 70))

    if not entries:
        draw_center_text(screen, "No saved scores yet", fonts["normal"], TEXT, (WIDTH // 2, 160))
    else:
        headers = ["#", "Name", "Score", "Distance", "Result"]
        x_positions = [70, 120, 270, 360, 460]
        for header, x in zip(headers, x_positions):
            screen.blit(fonts["small"].render(header, True, TEXT), (x, 120))

        for index, entry in enumerate(entries[:10], start=1):
            y = 150 + (index - 1) * 40
            values = [
                str(index),
                entry.get("name", "-"),
                str(entry.get("score", 0)),
                str(entry.get("distance", 0)),
                entry.get("result", "-"),
            ]
            for value, x in zip(values, x_positions):
                screen.blit(fonts["small"].render(value, True, TEXT), (x, y))

    back_button.draw(screen, fonts["normal"], mouse_pos)


def draw_game_over(screen, fonts, result, mouse_pos, buttons):
    screen.fill(BACKGROUND)
    title = "Race Finished" if result.get("result") == "Finished" else "Game Over"
    draw_center_text(screen, title, fonts["title"], TEXT, (WIDTH // 2, 90))

    lines = [
        f"Driver: {result.get('name', '-')}",
        f"Score: {result.get('score', 0)}",
        f"Distance: {result.get('distance', 0)}",
        f"Coins: {result.get('coins', 0)}",
        f"Difficulty: {result.get('difficulty', '-')}",
    ]
    for index, line in enumerate(lines):
        draw_center_text(screen, line, fonts["normal"], TEXT, (WIDTH // 2, 170 + index * 40))

    for button in buttons.values():
        button.draw(screen, fonts["normal"], mouse_pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 3 Racer")
    clock = pygame.time.Clock()

    fonts = {
        "title": pygame.font.SysFont("Arial", 42),
                "normal": pygame.font.SysFont("Arial", 24),
        "small": pygame.font.SysFont("Arial", 18),
    }

    settings = load_settings()
    username = ""
    input_active = True
    state = "menu"
    game = None
    last_result = None

    menu_buttons = {
        "play": Button((195, 240, 170, 46), "Play"),
        "leaderboard": Button((195, 300, 170, 46), "Leaderboard"),
        "settings": Button((195, 360, 170, 46), "Settings"),
        "quit": Button((195, 420, 170, 46), "Quit"),
    }

    settings_buttons = {
        "sound": Button((330, 160, 150, 40), "Toggle Sound"),
        "color": Button((330, 230, 150, 40), "Change Color"),
        "difficulty": Button((330, 300, 150, 40), "Change Difficulty"),
        "save_back": Button((205, 410, 150, 46), "Save & Back"),
    }

    leaderboard_back = Button((205, 660, 150, 40), "Back")
    game_over_buttons = {
        "retry": Button((195, 430, 170, 46), "Retry"),
        "menu": Button((195, 490, 170, 46), "Main Menu"),
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
                        game = RacerGame(settings, username.strip())
                        state = "game"
                    elif event.unicode and event.unicode.isprintable() and len(username) < 16:
                        username += event.unicode

                if menu_buttons["play"].clicked(event) and username.strip():
                    game = RacerGame(settings, username.strip())
                    state = "game"
                elif menu_buttons["leaderboard"].clicked(event):
                    state = "leaderboard"
                elif menu_buttons["settings"].clicked(event):
                    state = "settings"
                elif menu_buttons["quit"].clicked(event):
                    running = False

            elif state == "settings":
                if settings_buttons["sound"].clicked(event):
                    settings["sound_enabled"] = not settings["sound_enabled"]
                elif settings_buttons["color"].clicked(event):
                    settings["car_color"] = cycle_option(list(CAR_COLORS.keys()), settings["car_color"])
                elif settings_buttons["difficulty"].clicked(event):
                    settings["difficulty"] = cycle_option(["easy", "normal", "hard"], settings["difficulty"])
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
                    game = RacerGame(settings, username.strip())
                    state = "game"
                elif game_over_buttons["menu"].clicked(event):
                    state = "menu"

        if state == "menu":
            draw_menu(screen, fonts, username, input_active, mouse_pos, menu_buttons)

        elif state == "settings":
            draw_settings(screen, fonts, settings, mouse_pos, settings_buttons)

        elif state == "leaderboard":
            draw_leaderboard(screen, fonts, load_leaderboard(), mouse_pos, leaderboard_back)

        elif state == "game":
            result = game.update(dt_ms)
            game.draw(screen)
            if result is not None:
                last_result = result
                add_leaderboard_entry(result)
                state = "game_over"

        elif state == "game_over":
            draw_game_over(screen, fonts, last_result or {}, mouse_pos, game_over_buttons)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()