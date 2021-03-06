# Python 3.6
# Sound for Mac/Linux OS

import turtle
import os
from math import pow, sqrt
import random


# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")

# register the shapes
wn.register_shape("invader.gif")
wn.register_shape("player.gif")


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

# Set score to 0
score = 0

# Draw the score to 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("light blue")
player.shape("player.gif")
player.penup()
player.speed(0) #fast as possible
player.setposition(0, -250) #down near bottom of border
player.setheading(90)

playerspeed = 15

# Choose a number of enemies
number_of_enemies = 6
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

x = -150
for enemy in enemies:
    # enemy = turtle.Turtle()
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, 100)
    x += 50

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

bulletspeed = 55

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
        os.system("afplay laser.wav&")
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
    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move enemy back and down
        if enemy.xcor() > 280:
            #  Moves all the the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 50
                #enemyspeed *= -1  ONLY need to change once, since all have same speed
                e.sety(y)
            #Change direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 50
                # enemyspeed *= -1
                e.sety(y)
            # Change direction
            enemyspeed *= 1

        # Check for a collision btwn enemy and bullet
        if isCollision(bullet, enemy):
            os.system("afplay explosion.wav&")
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            # Update score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))


        # Check for a collision btwn enemy and player
        if isCollision(player, enemy):
            os.system("afplay lose.wav&")
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    if score == 50:
        os.system("afplay winner.wav&")
        break

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"




wn.mainloop()
