import math

import pygame


class Ball:
    def __init__(self, radius, x, y, color=(254, 254, 227), number=0):
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.radius = radius
        self.vx = 0.0
        self.vy = 0.0
        self.number = number
        self.active = True

        self.friction = 0.985

    def update(self, screen_width, screen_height):
        if not self.active: return

        # Применение трения
        self.vx *= self.friction
        self.vy *= self.friction

        # Обновление позиции
        self.x += self.vx
        self.y += self.vy

        # Столкновение со стенками
        if self.x < self.radius + 150:
            self.x = self.radius + 150
            self.vx *= -0.95
        elif self.x > screen_width - self.radius - 150:
            self.x = screen_width - self.radius - 150
            self.vx *= -0.95

        if self.y < self.radius + 50:
            self.y = self.radius + 50
            self.vy *= -0.95
        elif self.y > screen_height - self.radius - 50:
            self.y = screen_height - self.radius - 50
            self.vy *= -0.95

    def draw(self, surface):
        if not self.active: return

        # Основной круг
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        # Блик
        highlight_pos = (
            self.x - self.radius * 0.3,
            self.y - self.radius * 0.3
        )
        pygame.draw.circle(surface, (255, 255, 255, 128), highlight_pos, int(self.radius * 0.4))

        # Номер
        if self.number > 0:
            font = pygame.font.SysFont('Arial', 18, bold=True)
            text = font.render(str(self.number), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x, self.y))
            surface.blit(text, text_rect)

    def is_moving(self):
        return math.hypot(self.vx, self.vy) > 0.1
