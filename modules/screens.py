import pygame
from pygame.locals import *

from buttons import Button


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
                100 + (self.window_size[1] / len(self.btns) - 50) * index
            ))



    def draw_screen(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.screen.fill(self.fill)

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

            # Отрисовка всех кнопок ПОСЛЕ обработки событий
            for button in self.btns:
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        print('Работа приложения была успешно завершена!')


if __name__ == '__main__':
    screen = pygame.display.set_mode()
    mms = MainMenuScreen(screen)
    mms.draw_screen()
