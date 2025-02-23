from turtle import Turtle
import random

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.x_move = 6.0  # Increased from 4.0
        self.y_move = 6.0  # Increased from 4.0
        self.move_speed = 0.03  # Decreased from 0.05

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.03  # Decreased from 0.05
        self.x_move = 6.0 * random.choice([1, -1])  # Increased from 4.0
        self.y_move = 6.0 * random.choice([1, -1])  # Increased from 4.0
