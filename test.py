import pygame
import math
import sys
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы
WIDTH, HEIGHT = 1200, 800
FPS = 60
BALL_RADIUS = 20
FRICTION = 0.985
MAX_FORCE = 15
COLORS = {
    'background': '#2C6E49',
    'button_bg': '#D68C45',
    'button_hover': '#2C6E49',
    'border': '#2C6E49',
    'text': '#FFFFFF'
}


class Button:
    def __init__(self, x, y, text, width=300, height=80, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.colors = {
            'normal': pygame.Color(COLORS['button_bg']),
            'hover': pygame.Color(COLORS['button_hover']),
            'border': pygame.Color(COLORS['border']),
            'text': pygame.Color(COLORS['text'])
        }
        self.is_hovered = False

    def draw(self, surface):
        bg_color = self.colors['hover'] if self.is_hovered else self.colors['normal']
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, self.colors['border'], self.rect.inflate(10, 10), 5, border_radius=12)
        text = self.font.render(self.text, True, self.colors['text'])
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def update(self, event):
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if event.type == MOUSEBUTTONDOWN and self.is_hovered:
            return True
        return False


class Ball:
    def __init__(self, x, y, color, number=0):
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.radius = BALL_RADIUS
        self.vx = 0.0
        self.vy = 0.0
        self.number = number
        self.active = True

    def update(self):
        if not self.active: return

        # Применение трения
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Обновление позиции
        self.x += self.vx
        self.y += self.vy

        # Столкновение со стенками
        if self.x < BALL_RADIUS + 150:
            self.x = BALL_RADIUS + 150
            self.vx *= -0.95
        elif self.x > WIDTH - BALL_RADIUS - 150:
            self.x = WIDTH - BALL_RADIUS - 150
            self.vx *= -0.95

        if self.y < BALL_RADIUS + 50:
            self.y = BALL_RADIUS + 50
            self.vy *= -0.95
        elif self.y > HEIGHT - BALL_RADIUS - 50:
            self.y = HEIGHT - BALL_RADIUS - 50
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


def resolve_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.hypot(dx, dy)

    if distance == 0: return
    min_distance = ball1.radius + ball2.radius

    if distance < min_distance:
        # Корректировка позиций
        overlap = (min_distance - distance) / 2
        angle = math.atan2(dy, dx)

        ball1.x -= overlap * math.cos(angle)
        ball1.y -= overlap * math.sin(angle)
        ball2.x += overlap * math.cos(angle)
        ball2.y += overlap * math.sin(angle)

        # Расчет импульса
        nx = dx / distance
        ny = dy / distance
        p = 2 * (ball1.vx * nx + ball1.vy * ny - ball2.vx * nx - ball2.vy * ny) / (1 + 1)

        ball1.vx -= p * nx
        ball1.vy -= p * ny
        ball2.vx += p * nx
        ball2.vy += p * ny


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.balls = [
            Ball(WIDTH // 2 - 200, HEIGHT // 2, '#FFFFFF'),
            Ball(WIDTH // 2 + 200, HEIGHT // 2, '#FF0000', 1)
        ]
        self.cue_ball = self.balls[0]
        self.aiming = False
        self.last_mouse_pos = (0, 0)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(pygame.Color(COLORS['background']))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == MOUSEBUTTONDOWN:
                    if not any(b.is_moving() for b in self.balls):
                        self.aiming = True
                        self.last_mouse_pos = pygame.mouse.get_pos()

                if event.type == MOUSEBUTTONUP and self.aiming:
                    self.aiming = False
                    mouse_pos = pygame.mouse.get_pos()
                    dx = self.cue_ball.x - mouse_pos[0]
                    dy = self.cue_ball.y - mouse_pos[1]
                    force = math.hypot(dx, dy) * 0.15
                    angle = math.atan2(dy, dx)

                    self.cue_ball.vx = min(force, MAX_FORCE) * math.cos(angle)
                    self.cue_ball.vy = min(force, MAX_FORCE) * math.sin(angle)

            # Отрисовка линии прицела
            if self.aiming:
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.line(self.screen, (255, 255, 255),
                                 (self.cue_ball.x, self.cue_ball.y), mouse_pos, 3)

            # Обновление шаров
            for ball in self.balls:
                ball.update()
                ball.draw(self.screen)

            # Проверка столкновений
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    resolve_collision(self.balls[i], self.balls[j])

            pygame.display.flip()
            clock.tick(FPS)


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button(WIDTH // 2 - 150, 300, "Новая игра"),
            Button(WIDTH // 2 - 150, 400, "Выход")
        ]

    def draw(self):
        self.screen.fill(pygame.Color('#4C956C'))
        title_font = pygame.font.SysFont('Arial', 72, bold=True)
        title = title_font.render("Русский Бильярд", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for btn in self.buttons:
            btn.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn.update(event):
                        if btn.text == "Новая игра":
                            return "game"
                        if btn.text == "Выход":
                            pygame.quit()
                            sys.exit()
        return "menu"


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Русский Бильярд")

    current_screen = "menu"
    menu = MainMenu(screen)
    game = None

    while True:
        if current_screen == "menu":
            menu.draw()
            result = menu.handle_events()
            if result == "game":
                game = Game(screen)
                current_screen = "game"
        elif current_screen == "game":
            game.run()
            current_screen = "menu"


if __name__ == "__main__":
    main()