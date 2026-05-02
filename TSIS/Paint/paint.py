from datetime import datetime

import pygame

from tools import draw_shape, flood_fill


pygame.init()

WIDTH, HEIGHT = 1000, 720
TOOLBAR_HEIGHT = 110
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 14)
text_font = pygame.font.SysFont("Arial", 30)

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
LIGHT_BLUE = (180, 220, 255)
LIGHT_RED = (255, 210, 210)

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

current_tool = "pencil"
current_color = BLACK
stroke_size = 5

drawing = False
start_pos = None
current_pos = None
last_pos = None

text_active = False
text_position = None
text_buffer = ""

status_message = ""
status_until = 0

color_buttons = [
    (BLACK, pygame.Rect(20, 15, 40, 40)),
    (RED, pygame.Rect(70, 15, 40, 40)),
    (GREEN, pygame.Rect(120, 15, 40, 40)),
    (BLUE, pygame.Rect(170, 15, 40, 40)),
    (YELLOW, pygame.Rect(220, 15, 40, 40)),
    (PURPLE, pygame.Rect(270, 15, 40, 40)),
    (ORANGE, pygame.Rect(320, 15, 40, 40)),
]

tool_order = [
    "pencil",
    "line",
    "rect",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
    "fill",
    "text",
]

tool_labels = {
    "pencil": "Pencil",
    "line": "Line",
    "rect": "Rect",
    "circle": "Circle",
    "square": "Square",
    "right_triangle": "R-Tri",
    "equilateral_triangle": "E-Tri",
    "rhombus": "Rhomb",
    "fill": "Fill",
    "text": "Text",
}

tool_buttons = {}
button_x = 380
button_y = 12
button_w = 70
button_h = 30
button_gap = 6

for index, tool_name in enumerate(tool_order):
    row = index // 5
    col = index % 5
    x = button_x + col * (button_w + button_gap)
    