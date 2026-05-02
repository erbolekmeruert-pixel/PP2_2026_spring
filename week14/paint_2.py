import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
GREEN = (30, 180, 30)
BLUE = (30, 80, 220)
YELLOW = (240, 220, 0)
PURPLE = (140, 60, 190)
ORANGE = (255, 140, 0)
GRAY = (230, 230, 230)
DARK_GRAY = (80, 80, 80)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

current_tool = "pen"
current_color = BLACK
brush_size = 5
eraser_size = 24
shape_width = 2

drawing = False
start_pos = None
current_pos = None
last_pos = None

color_buttons = [
    (BLACK, pygame.Rect(20, 20, 40, 40)),
    (RED, pygame.Rect(70, 20, 40, 40)),
    (GREEN, pygame.Rect(120, 20, 40, 40)),
    (BLUE, pygame.Rect(170, 20, 40, 40)),
    (YELLOW, pygame.Rect(220, 20, 40, 40)),
    (PURPLE, pygame.Rect(270, 20, 40, 40)),
    (ORANGE, pygame.Rect(320, 20, 40, 40)),
]

tool_buttons = {
    "pen": pygame.Rect(430, 10, 90, 30),
    "rect": pygame.Rect(530, 10, 90, 30),
    "circle": pygame.Rect(630, 10, 90, 30),
    "eraser": pygame.Rect(730, 10, 90, 30),

    "square": pygame.Rect(430, 50, 90, 30),
    "right_triangle": pygame.Rect(530, 50, 90, 30),
    "equilateral_triangle": pygame.Rect(630, 50, 90, 30),
    "rhombus": pygame.Rect(730, 50, 90, 30),
}

tool_labels = {
    "pen": "Pen",
    "rect": "Rect",
    "circle": "Circle",
    "eraser": "Eraser",
    "square": "Square",
    "right_triangle": "R-Tri",
    "equilateral_triangle": "E-Tri",
    "rhombus": "Rhombus",
}

clear_button = pygame.Rect(840, 10, 120, 30)


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        border_width = 4 if color == current_color else 2
        pygame.draw.rect(screen, BLACK, rect, border_width)

    for tool_name, rect in tool_buttons.items():
        button_color = (180, 220, 255) if tool_name == current_tool else WHITE
        pygame.draw.rect(screen, button_color, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        text = small_font.render(tool_labels[tool_name], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.draw.rect(screen, (255, 210, 210), clear_button, border_radius=8)
    pygame.draw.rect(screen, BLACK, clear_button, 2, border_radius=8)
    clear_text = font.render("Clear", True, BLACK)
    screen.blit(clear_text, clear_text.get_rect(center=clear_button.center))

    info_text = small_font.render(f"Color / Tool: {tool_labels[current_tool]}", True, BLACK)
    size_text = small_font.render(f"Brush: {brush_size}  Eraser: {eraser_size}", True, BLACK)
    screen.blit(info_text, (840, 50))
    screen.blit(size_text, (840, 68))


def to_canvas_pos(mouse_pos):
    x = max(0, min(WIDTH - 1, mouse_pos[0]))
    y = max(0, min(HEIGHT - TOOLBAR_HEIGHT - 1, mouse_pos[1] - TOOLBAR_HEIGHT))
    return x, y


def make_rect(start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    width = abs(start[0] - end[0])
    height = abs(start[1] - end[1])
    return pygame.Rect(x, y, width, height)


def make_square_rect(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = min(abs(dx), abs(dy))

    if dx >= 0:
        x = start[0]
    else:
        x = start[0] - side

    if dy >= 0:
        y = start[1]
    else:
        y = start[1] - side

    return pygame.Rect(x, y, side, side)


def get_right_triangle_points(start, end):
    return [start, (start[0], end[1]), end]


def get_equilateral_triangle_points(start, end):
    left = min(start[0], end[0])
    right = max(start[0], end[0])
    side = max(1, right - left)
    height = int((math.sqrt(3) / 2) * side)
    center_x = (left + right) // 2

    if end[1] >= start[1]:
        apex_y = min(start[1], end[1])
        base_y = apex_y + height
        apex = (center_x, apex_y)
    else:
        apex_y = max(start[1], end[1])
        base_y = apex_y - height
        apex = (center_x, apex_y)

    return [
        apex,
        (center_x - side // 2, base_y),
        (center_x + side // 2, base_y),
    ]


def get_rhombus_points(start, end):
    rect = make_rect(start, end)
    center_x = rect.x + rect.width // 2
    center_y = rect.y + rect.height // 2

    return [
        (center_x, rect.y),
        (rect.x + rect.width, center_y),
        (center_x, rect.y + rect.height),
        (rect.x, center_y),
    ]


def draw_shape(surface, tool_name, color, start, end):
    if tool_name == "rect":
        rect = make_rect(start, end)
        pygame.draw.rect(surface, color, rect, shape_width)

    elif tool_name == "circle":
        radius = int(math.dist(start, end))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, shape_width)

    elif tool_name == "square":
        rect = make_square_rect(start, end)
        if rect.width > 0:
            pygame.draw.rect(surface, color, rect, shape_width)

    elif tool_name == "right_triangle":
        points = get_right_triangle_points(start, end)
        pygame.draw.polygon(surface, color, points, shape_width)

    elif tool_name == "equilateral_triangle":
        points = get_equilateral_triangle_points(start, end)
        pygame.draw.polygon(surface, color, points, shape_width)

    elif tool_name == "rhombus":
        points = get_rhombus_points(start, end)
        pygame.draw.polygon(surface, color, points, shape_width)


shape_tools = {
    "rect",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
}

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_toolbar()

    if drawing and start_pos and current_pos and current_tool in shape_tools:
        preview_surface = canvas.copy()
        draw_shape(preview_surface, current_tool, current_color, start_pos, current_pos)
        screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] < TOOLBAR_HEIGHT:
                for color, rect in color_buttons:
                    if rect.collidepoint(mouse_pos):
                        current_color = color

                for tool_name, rect in tool_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        current_tool = tool_name

                if clear_button.collidepoint(mouse_pos):
                    canvas.fill(WHITE)

            else:
                drawing = True
                start_pos = to_canvas_pos(mouse_pos)
                current_pos = start_pos
                last_pos = start_pos

                if current_tool == "pen":
                    pygame.draw.circle(canvas, current_color, start_pos, brush_size // 2)
                elif current_tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, start_pos, eraser_size // 2)

        elif event.type == pygame.MOUSEMOTION and drawing:
            mouse_pos = pygame.mouse.get_pos()
            current_pos = to_canvas_pos(mouse_pos)

            if current_tool == "pen" and last_pos is not None:
                pygame.draw.line(canvas, current_color, last_pos, current_pos, brush_size)

            elif current_tool == "eraser" and last_pos is not None:
                pygame.draw.line(canvas, WHITE, last_pos, current_pos, eraser_size)

            last_pos = current_pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and start_pos is not None:
                end_pos = to_canvas_pos(pygame.mouse.get_pos())

                if current_tool in shape_tools:
                    draw_shape(canvas, current_tool, current_color, start_pos, end_pos)

            drawing = False
            start_pos = None
            current_pos = None
            last_pos = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
