#Day 22
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)  # Add this line for consistent speed
    ball.move()

    # Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Prevent paddles from going off screen
    if r_paddle.ycor() > 250:
        r_paddle.goto(350, 250)
    if r_paddle.ycor() < -250:
        r_paddle.goto(350, -250)
    if l_paddle.ycor() > 250:
        l_paddle.goto(-350, 250)
    if l_paddle.ycor() < -250:
        l_paddle.goto(-350, -250)

    # Improved paddle collision detection
    if (ball.distance(r_paddle) < 50 and 320 < ball.xcor() < 350) or \
       (ball.distance(l_paddle) < 50 and -350 < ball.xcor() < -320):
        ball.bounce_x()

    # Detect R paddle misses
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # Detect L paddle misses:
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()