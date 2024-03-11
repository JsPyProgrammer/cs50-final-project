# import the random library
import random


class Square:
    def __init__(self, canvas, x, y):
        """This function adds the paddle to the canvas"""

        # set the width, height, x, and y
        self.width = 10
        self.height = 75
        self.x = x
        self.y = y
        # indicate the canvas that's in use
        self.canvas = canvas
        # draw and get the id of the rectangle that is drawn
        self.id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill="white"
        )

    def move(self, amount):
        # update the y the amount needed
        self.y += amount

        # update the coords of the square on the canvas
        self.canvas.coords(
            self.id, self.x, self.y, self.x + self.width, self.y + self.height
        )


class Circle:
    def __init__(self, canvas, x, y):
        """This function adds the ball to the canvas"""

        # set the radius, x, and y of the ball
        self.radius = 5
        self.x = x
        self.y = y
        # indicate the canvas that's in use
        self.canvas = canvas

        # set the speed and direction of the ball
        self.speed = 5
        self.moveX = random.choice((-1, 1))
        self.moveY = random.randint(-100, 100) / 100

        # draw and get the id of the ball
        self.id = self.canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill="green",
        )

    def move(self):
        # move the ball in the direction needed along with the speed
        x = self.moveX * self.speed
        y = self.moveY * self.speed

        # update the x and y coord
        self.x += x
        self.y += y

        # update the ball in the canvas
        self.canvas.coords(
            self.id,
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )
