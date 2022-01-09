from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from random import randint

import pygame


class Direction(Enum):
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    CENTER = 0

    def reverse(self):
        return Direction(self.value * -1)


class color(Enum):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)


@dataclass
class Snake:
    head: pygame.Vector2
    body: deque = deque()
    direction: Direction = Direction.CENTER

    def __iter__(self):
        yield self.head
        yield from self.body

    def __contains__(self, pos):
        for node in self:
            if node == pos:
                return True
        return False

    def move(self):
        self.body.appendleft(deepcopy(self.head))
        if self.direction == Direction.UP:
            self.head.y -= 1
        elif self.direction == Direction.DOWN:
            self.head.y += 1
        elif self.direction == Direction.LEFT:
            self.head.x -= 1
        elif self.direction == Direction.RIGHT:
            self.head.x += 1

    def reach_the_border(self, border: pygame.Vector2) -> bool:
        return self.head.x in {border.x, -1} or self.head.y in {border.y, -1}

    def clash_into_self(self) -> bool:
        return self.head in self.body

    def eatten_food(self, food_pos: pygame.Vector2) -> bool:
        return self.head == food_pos


@dataclass
class Board:
    SNAKE_SIZE: int = 15
    BOX_PER_ROW: int = 50
    BOX_PER_COL: int = 50
    FPS: int = 144

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Snake Game")
        self.WIDTH = self.SNAKE_SIZE * self.BOX_PER_ROW
        self.HEIGHT = self.SNAKE_SIZE * self.BOX_PER_COL
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.snake = Snake(pygame.Vector2((self.BOX_PER_ROW - 1) // 2, (self.BOX_PER_COL - 1) // 2))
        self.food_pos = self.new_food_pos()
        self.score = 0

    def new_food_pos(self) -> pygame.Vector2:
        new_pos = pygame.Vector2(randint(0, self.BOX_PER_ROW - 1), randint(0, self.BOX_PER_COL - 1))
        if (new_pos not in self.snake):
            return new_pos
        return self.new_food_pos()

    def get_color(self, x: int, y: int) -> color:
        pos = pygame.Vector2(x // self.SNAKE_SIZE, y // self.SNAKE_SIZE)
        if pos == self.snake.head:
            return color.RED
        if pos in self.snake.body:
            return color.GREEN
        if pos == self.food_pos:
            return color.BLUE
        return color.WHITE

    def draw_board(self):
        for x in range(0, self.WIDTH, self.SNAKE_SIZE):
            for y in range(0, self.HEIGHT, self.SNAKE_SIZE):
                color = self.get_color(x, y).value
                pygame.draw.rect(self.WINDOW, color, (x, y, self.SNAKE_SIZE, self.SNAKE_SIZE), 0)
        pygame.display.update()

    @staticmethod
    def direction_of(key_pressed):
        if key_pressed[pygame.K_UP]:
            return Direction.UP
        if key_pressed[pygame.K_DOWN]:
            return Direction.DOWN
        if key_pressed[pygame.K_LEFT]:
            return Direction.LEFT
        if key_pressed[pygame.K_RIGHT]:
            return Direction.RIGHT

    def get_direction(self):
        key_pressed = pygame.key.get_pressed()
        input_direction = self.direction_of(key_pressed)
        if input_direction and input_direction != self.snake.direction.reverse():
            self.snake.direction = input_direction

    def show_gameover(self):
        center_x = lambda msg: self.WIDTH // 2 - msg.get_rect().width // 2
        font = pygame.font.SysFont("Arial", 30)
        gameover_msg = font.render("Game Over!", True, color.RED.value)
        score_msg = font.render("Score: " + str(self.score), True, color.RED.value)
        self.WINDOW.fill(color.BLACK.value)
        self.WINDOW.blit(gameover_msg, (center_x(gameover_msg), 0))
        self.WINDOW.blit(score_msg, (center_x(score_msg), gameover_msg.get_rect().height))
        for counter in range(10, 0, -1):
            pygame.event.get()
            counter_msg = font.render("Exiting in " + str(counter), True, color.RED.value)
            self.WINDOW.blit(counter_msg, (center_x(counter_msg), gameover_msg.get_rect().height + counter_msg.get_rect().height))
            pygame.display.update()
            pygame.time.wait(1000)
            self.WINDOW.fill(color.BLACK.value,
                             (center_x(counter_msg), gameover_msg.get_rect().height + counter_msg.get_rect().height,
                              center_x(counter_msg) + counter_msg.get_rect().width, self.HEIGHT))

    def run(self):
        clock = pygame.time.Clock()
        run = True
        update_timer = 80
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.get_direction()
            self.snake.move()

            if self.snake.eatten_food(self.food_pos):
                self.score += 1
                self.food_pos = self.new_food_pos()
                if update_timer >= 0:
                    update_timer -= 5
            else:
                self.snake.body.pop()

            border = pygame.Vector2(self.BOX_PER_ROW, self.BOX_PER_COL)
            if (self.snake.reach_the_border(border) or self.snake.clash_into_self()):
                run = False

            self.draw_board()

            pygame.time.wait(update_timer)

        self.show_gameover()
        pygame.quit()


def main():
    board = Board()
    board.run()


if __name__ == "__main__":
    main()
