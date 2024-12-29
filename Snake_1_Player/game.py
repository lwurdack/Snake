import random

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
MOVES = [UP, DOWN, LEFT, RIGHT]

EMPTY = 0
FOOD = 99

class SnakeGame:
    def __init__(self, size):
        self.size = size
        initial_length = 3  # Die Anfangslänge der Schlange
        self.snake = [(size // 2, size // 2 - i) for i in range(initial_length)]
        self.food = (random.randint(0, size - 1), random.randint(0, size - 1))
        self.direction = RIGHT
        self.done = False
        self.score = 0
        self.steps_without_food = 0

    def move(self, direction):
        if self.done:
            return

        # Kopf bewegen
        head_x, head_y = self.snake[-1]
        new_head = (head_x + direction[0], head_y + direction[1])

        if (new_head[0] < 0 or new_head[1] < 0 or 
            new_head[0] >= self.size or new_head[1] >= self.size or 
            new_head in self.snake):
            self.done = True  # Spiel beendet
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.food = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            self.steps_without_food = 0
        else:
            self.snake.pop(0)  # Letztes Segment entfernen
            self.steps_without_food += 1


    def get_state(self):
        head_x, head_y = self.snake[-1]
        return {
            "head": (head_x, head_y),
            "food": self.food,
            "distance_to_wall": {
                "UP": head_x,
                "DOWN": self.size - head_x - 1,
                "LEFT": head_y,
                "RIGHT": self.size - head_y - 1
            },
            "food_relative": {
                "UP": self.food[0] < head_x,
                "DOWN": self.food[0] > head_x,
                "LEFT": self.food[1] < head_y,
                "RIGHT": self.food[1] > head_y
            }
        }
