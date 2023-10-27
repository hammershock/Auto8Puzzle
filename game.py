import threading
from enum import Enum

import pygame
import sys
from pygame.locals import *
from board import Board, Direction
from dijkstra import dijkstra, path_to_actions


class GameState(Enum):
    START = 1
    RUNNING = 2
    OVER = 3


class Game:
    def __init__(self):
        # 颜色定义
        self.thread = None
        self.color1 = (192, 192, 192)
        self.color2 = (192, 192, 192)
        self.border_color = (139, 139, 139)
        self.text_color = (218, 74, 65)
        self.digit_color = (0, 0, 244)

        # 尺寸定义
        self.BLOCK_SIZE = 100
        self.BOARD_SIZE = 3
        self.SCREEN_SIZE = self.BOARD_SIZE * self.BLOCK_SIZE

        # 数字板
        self.board = Board()

        # 加载方块图像
        self.block_image = pygame.image.load("resources/block.png")
        self.block_image = pygame.transform.scale(self.block_image, (self.BLOCK_SIZE, self.BLOCK_SIZE))

        # 初始化
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        pygame.display.set_caption("8 Puzzle")
        self.drag_sound = pygame.mixer.Sound("resources/drag.ogg")  # 加载拖动音效
        self.win_sound = pygame.mixer.Sound("resources/win.ogg")
        self.state = GameState.START

        # 演示模式
        self.auto_move = False
        self.moves = []

    def play_drag_sound(self):
        self.drag_sound.play()  # 播放拖动音效

    def show_message(self, message):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, self.text_color)
        text_rect = text.get_rect(center=(self.SCREEN_SIZE // 2, self.SCREEN_SIZE // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def restart_game(self):
        self.board.shuffle()  # 重新开始，打乱棋盘
        pygame.event.clear()  # 清除之前的事件，避免重复响应
        self.show_board()  # 重新绘制棋盘

    def show_board(self):
        self.screen.fill(self.color2)
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                number = self.board.get_number(row, col)
                if number:  # 如果不是0，则画出数字和边框
                    rect = pygame.Rect(col * self.BLOCK_SIZE, row * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                    pygame.draw.rect(self.screen, self.border_color, rect, 1)
                    pygame.draw.rect(self.screen, self.color1, rect.inflate(-2, -2))
                    self.screen.blit(self.block_image, rect)
                    font = pygame.font.Font(None, 80)
                    text = font.render(str(number), True, self.digit_color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.state == GameState.START:
                        self.state = GameState.RUNNING
                        self.show_board()
                    elif self.state == GameState.OVER:
                        self.restart_game()
                        self.state = GameState.RUNNING
                    continue

                if self.state != GameState.RUNNING:
                    continue

                # 按s键开启或关闭自动解决状态
                if event.key == K_s:
                    if self.auto_move:
                        self.auto_move = False
                        self.moves = []
                    else:
                        start = self.board.tuple()
                        goal = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
                        self.thread = threading.Thread(target=self.solve_puzzle, args=(start, goal))
                        self.thread.start()

                if not self.auto_move:
                    moves = {K_UP: Direction.UP, K_DOWN: Direction.DOWN, K_LEFT: Direction.LEFT,
                             K_RIGHT: Direction.RIGHT}
                    if event.key in moves and self.board.move(moves[event.key]):
                        self.play_drag_sound()
                        self.show_board()

    def solve_puzzle(self, start, goal):
        path, cost = dijkstra(start, goal)
        self.moves = path_to_actions(path)
        self.auto_move = True

    def run(self):
        while True:
            self.handle_events()

            if self.auto_move:
                moves = {(1, 0): Direction.DOWN, (-1, 0): Direction.UP, (0, 1): Direction.RIGHT,
                         (0, -1): Direction.LEFT}
                if self.moves:
                    move = self.moves.pop(0)
                    move = moves[move]
                    if self.board.move(move):
                        self.play_drag_sound()
                        self.show_board()
                    pygame.time.wait(100)
                else:
                    self.auto_move = False

            if self.state == GameState.START:
                self.show_message("Press ENTER to start.")
            elif self.state == GameState.RUNNING and self.board.is_solved():
                self.state = GameState.OVER
                self.win_sound.play()
                self.show_message("Press ENTER to restart.")
            elif self.state == GameState.OVER:
                self.show_message("Press ENTER to restart.")
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
