import pygame
import math


class Ball:
    def __init__(self, screen, radius, x, y, speed_x=0, speed_y=0, number=None):
        self.screen = screen
        self.radius = radius
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.number = number
        self.color = (255, 255, 255)  # белый цвет

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        if self.number is not None:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.number), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x, self.y))
            self.screen.blit(text, text_rect)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def check_borders(self, width, height):
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.speed_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > height:
            self.speed_y *= -1

    def update(self, width, height):
        self.move()
        self.check_borders(width, height)
        self.draw()
