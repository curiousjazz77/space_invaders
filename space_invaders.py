import turtle
import os
from math import pow, sqrt
import random


# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

# Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("light blue")
player.shape("turtle")
player.penup()
player.speed(0) #fast as possible
player.setposition(0, -250) #down near bottom of border
player.setheading(90)

playerspeed = 15

# Choose a number of enemies
number_of_enemies = 5
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    # enemy = turtle.Turtle()
    enemy.color("orange")
    enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2



# Player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

"""
Define bullet state as either
ready (ready to fire) or fire (bullet is firing)
"""
bulletstate = "ready"

# Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    """
    Decalre bullet state as a global
    if it needs changed
    :return:
    """
    global bulletstate  # probably not a good idea for production code
    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 25
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(turtle1, turlte2):
    distance = sqrt(pow(turtle1.xcor()-turlte2.xcor(), 2) +
                    pow(turtle1.ycor() - turlte2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# Create keyboard bindings
turtle.Screen().listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(fire_bullet, "space")

# Main game loop
while True:
    # Move the enemy
    x = enemy.xcor()
    x += enemyspeed
    enemy.setx(x)

    # Move enemy back and down
    if enemy.xcor() > 280:
        y = enemy.ycor()
        y -= 50
        enemyspeed *= -1
        enemy.sety(y)

    if enemy.xcor() < -280:
        y = enemy.ycor()
        y -= 50
        enemyspeed *= -1
        enemy.sety(y)

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    # Check for a collision btwn enemy and bullet
    if isCollision(bullet, enemy):
        bullet.hideturtle()
        bulletstate = "ready"
        bullet.setposition(0, -400)
        # Reset the enemy
        enemy.setposition(-200, 250)

    # Check for a collision btwn enemy and player
    if isCollision(player, enemy):
        player.hideturtle()
        enemy.hideturtle()
        print("Game Over")
        break

wn.mainloop()
