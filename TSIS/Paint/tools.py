import math

import pygame


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

    x = start[0] if dx >= 0 else start[0] - side
    y = start[1] if dy >= 0 else start[1] - side
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
    else:
        apex_y = max(start[1], end[1])
        base_y = apex_y - height

    return [
        (center_x, apex_y),
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


def draw_shape(surface, tool_name, color, start, end, width):
    if tool_name == "line":
        pygame.draw.line(surface, color, start, end, width)
    elif tool_name == "rect":
        rect = make_rect(start, end)
        if rect.width > 0 and rect.height > 0:
            pygame.draw.rect(surface, color, rect, width)
    elif tool_name == "circle":
        radius = int(math.dist(start, end))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, width)
    elif tool_name == "square":
        rect = make_square_rect(start, end)
        if rect.width > 0:
            pygame.draw.rect(surface, color, rect, width)
    elif tool_name == "right_triangle":
        pygame.draw.polygon(surface, color, get_right_triangle_points(start, end), width)
    elif tool_name == "equilateral_triangle":
        pygame.draw.polygon(surface, color, get_equilateral_triangle_points(start, end), width)
    elif tool_name == "rhombus":
        pygame.draw.polygon(surface, color, get_rhombus_points(start, end), width)


def flood_fill(surface, start, fill_color):
    width, height = surface.get_size()
    target_color = surface.get_at(start)[:3]
    replacement_color = fill_color[:3]

    if target_color == replacement_color:
        return

    stack = [start]
    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y))[:3] != target_color:
            continue

        surface.set_at((x, y), replacement_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))