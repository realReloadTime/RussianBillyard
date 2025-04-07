import pygame
from pygame.locals import *

pygame.font.init()


class Button:
    def __init__(self, x, y, text, width=400, height=100, font_size=45, blocked: bool = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)

        # Цвета
        self.normal_bg = pygame.Color('#D68C45')  # Фон кнопки
        self.blocked_bg = pygame.Color('#FFC9B9')  # Фон неактивной кнопки
        self.hover_bg = pygame.Color('#2C6E49')  # Фон при наведении
        self.border_color = pygame.Color('#2C6E49')  # Цвет обводки
        self.text_color = pygame.Color('#FFFFFF')  # Цвет текста (белый)

        # Параметры обводки
        self.border_width = 2
        self.border_padding = 5

        # Состояние
        self.is_hovered = False
        self.is_clicked = False
        self.is_blocked = blocked

    def draw(self, surface):
        # Рисуем фон кнопки
        bg_color = self.hover_bg if self.is_hovered else self.normal_bg
        if self.is_blocked:
            bg_color = self.blocked_bg
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=5)

        # Рисуем обводку
        border_rect = pygame.Rect(
            self.rect.x - self.border_padding,
            self.rect.y - self.border_padding,
            self.rect.width + self.border_padding * 2,
            self.rect.height + self.border_padding * 2
        )
        pygame.draw.rect(surface, self.border_color, border_rect, self.border_width, border_radius=7)

        # Рисуем текст
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, event):
        if self.is_blocked:
            return False

        # mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.is_hovered:
                    self.is_clicked = True
                    return True  # Кнопка была нажата

            if event.type == MOUSEBUTTONUP and event.button == 1:
                if self.is_clicked_now():
                    self.is_clicked = False
                    return True  # Кнопка была отпущена (клик завершен)
                self.is_clicked = False
        return False

    def is_clicked_now(self):
        return self.is_clicked and self.is_hovered

    def move_button_to(self, x_y: tuple, w_h: tuple = None):
        if x_y:
            self.rect.x, self.rect.y = x_y
        if w_h:
            self.rect.width, self.rect.height = w_h


class LabelText:
    def __init__(self, x, y, text, font_size=64, color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.text_color = color

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = text_surface.get_rect(center=self.rect.center)

        surface.blit(text_surface, self.rect)


