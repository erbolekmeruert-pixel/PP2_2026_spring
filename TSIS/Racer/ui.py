import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON = (245, 245, 245)
BUTTON_HOVER = (214, 234, 255)
BUTTON_ACTIVE = (186, 220, 255)


class Button:
    def __init__(self, rect, label):
        self.rect = pygame.Rect(rect)
        self.label = label

    def draw(self, surface, font, mouse_pos, active=False):
        color = BUTTON_ACTIVE if active else BUTTON
        if self.rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER if not active else BUTTON_ACTIVE
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=12)
        label = font.render(self.label, True, BLACK)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(surface, text, font, color, center):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, text_surface.get_rect(center=center))


def draw_text_input(surface, rect, text, font, active):
    border_color = (0, 120, 240) if active else BLACK
    fill_color = (255, 255, 255)
    pygame.draw.rect(surface, fill_color, rect, border_radius=10)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)
    display_text = text if text else "Enter username..."
    color = BLACK if text else (130, 130, 130)
    text_surface = font.render(display_text, True, color)
    surface.blit(text_surface, (rect.x + 14, rect.y + 10))
    