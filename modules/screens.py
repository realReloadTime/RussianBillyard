import pygame
from pygame.locals import *

from navigation import Button, LabelText
from balls import Ball

from random import randint


class MainMenuScreen:
    def __init__(self, screen: pygame.display.set_mode, fill: str = '#4C956C'):
        btns = ['Новая игра', 'Продолжить', 'Настройки', 'Выход']

        self.screen = screen
        self.window_size = screen.get_size()
        self.fill = fill

        self.btns = [Button(0, 0, button)
                     for index, button in enumerate(btns)]

        for index, btn in enumerate(self.btns):
            btn.move_button_to((
                self.window_size[0] / 2 - btn.rect.width / 2,
                100 + (self.window_size[1] / len(self.btns) - 50) * index + 100
            ))
        self.btns.append(Button(self.window_size[0] - 250 * 1.1,
                                self.window_size[1] - 75 * 1.2,
                                'Автор', 250, 75))

    def get_decorative_balls(self):
        balls = list()
        for i in range(16):
            balls.append(Ball(self.screen,
                                   40,
                                   self.window_size[0] // 16 * i + 50,
                                   randint(50, self.window_size[1])))
        return balls

    def draw_screen(self):
        running = True
        clock = pygame.time.Clock()

        game_label = LabelText(self.window_size[0] // 2, 75, 'РУССКИЙ БИЛЬЯРД', 96, (235, 235, 235))
        balls = self.get_decorative_balls()
        while running:
            self.screen.fill(self.fill)

            for ball in balls:
                ball.update(2000, 2000)
            # Обработка всех событий ДО отрисовки кнопок
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                # Обновляем состояние всех кнопок
                for button in self.btns:
                    if button.update(event) and button.is_clicked_now():
                        # print(f'BTN: {button.text} {button.rect} {event.pos}')
                        if button.text == 'Выход':
                            running = False
                        if button.text == 'Автор':
                            balls = self.get_decorative_balls()

            # Отрисовка всех кнопок ПОСЛЕ обработки событий
            for button in self.btns:
                button.draw(self.screen)
            game_label.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        print('Работа приложения была успешно завершена!')


if __name__ == '__main__':
    screen = pygame.display.set_mode()
    mms = MainMenuScreen(screen)
    mms.draw_screen()
