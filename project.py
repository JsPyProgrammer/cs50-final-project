# import all the libraries that I need
import random
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# my components.py library
from components import *

# global variables that are used
lvl = None
startPage = None
gamePage = None
canvas = None
window = {"width": 640, "height": 400}
player = None
computer = None
computerSpeed = 0
ball = None
keys = [False, False]
playerScore = 0
computerScore = 0
stop = False
playerScoreDisplay = None
computerScoreDisplay = None
resultText = None
playingGame = False
paused = False
gameMenu = None

# set up the window =====
root = Tk()
# make the title of window PyPong
root.title("PyPong")
# run the confirmClose function before closing
root.protocol("WM_DELETE_WINDOW", lambda: confirmClose())
# remove menu tearoffs
root.option_add("*tearOff", False)
# set the window size (640*400)
root.minsize(window["width"], window["height"])
# remove realizability
root.resizable(False, False)
# set the style to use on each platform
ttkStyle = ttk.Style()
if sys.platform == "win32":
    ttkStyle.theme_use("vista")
elif sys.platform == "darwin":
    ttkStyle.theme_use("aqua")
else:
    ttkStyle.theme_use("clam")
# =====

# .png is only supported for Tk v8.6+. Use .gif for older versions
if TkVersion < 8.6:
    logo = PhotoImage(file="logo.gif")
else:
    logo = PhotoImage(file="logo.png")

# style configurations
ttkStyle.configure("startPage.TFrame", background="black")
ttkStyle.configure(
    "option.TButton",
    background="white",
    font="TkDefaultFont 11",
    foreground="black",
    highlightthickness=0,
    borderwidth=0,
    activebackground="white",
)


def isKeyUp(sym):
    """Checks if the key symbol is 'Up'"""
    return sym == "Up"


def isKeyDown(sym):
    """Check if the key symbol is 'Down'"""
    return sym == "Down"


def isAboveScreen(square):
    """Checks if the square is going above the canvas screen"""
    return square.y < 0


def isBelowScreen(square):
    """Checks if the bottom of the square is going below the canvas screen"""
    return square.y + square.height > window["height"]


def wonGame(score):
    """Checks if reached the minimum score"""
    return score >= 5


def getComputerSpeed(level):
    """Gets the speed multiplier for the computer"""
    if level == "easy":  # level is easy, go 50% of the speed as player
        return 0.5
    elif level == "medium":  # level is medium, go 100% of the speed as player
        return 1
    elif level == "hard":  # level is hard, go 150% of the speed as player
        return 1.5
    else:  # unknown level, go 0% of the speed
        return 0


def isColliding(circle, square):
    """Checks if the circle is colliding with the square"""

    # get the top, right, bottom, and left sides of the circle
    circleRight = circle.x + circle.radius
    circleLeft = circle.x - circle.radius
    circleTop = circle.y - circle.radius
    circleBottom = circle.y + circle.radius

    # gets the right and bottom sides of the square
    squareRight = square.x + square.width
    squareBottom = square.y + square.height

    # check if any part is touching the square
    return (
        (circleLeft <= squareRight)
        and (circleRight >= square.x)
        and (circleTop <= squareBottom)
        and (circleBottom >= square.y)
    )


def getKey(event, isDown):
    """Checks the key symbol, and indicates in keys[] which key is being pressed or lifted"""

    if isKeyUp(event.keysym):  # if the key symbol is up...
        # set the first element to the value of isDown
        keys[0] = isDown

    if isKeyDown(event.keysym):  # if the key symbol is down...
        # set the second element to the value of isDown
        keys[1] = isDown


def movePlayer():
    """Moves the players square"""

    if keys[0]:  # if pressing on the up key...
        # move the player's square up by 5px
        player.move(-5)

    if keys[1]:  # if pressing on the down key...
        # move the player's square down by 5px
        player.move(5)


def moveComputer():
    """This is the computer AI"""
    global computerSpeed
    # get the middle of the computer's square
    computerMiddle = computer.y + computer.height / 2

    # here is the maximum speed of the computer
    maxMove = 5 * getComputerSpeed(lvl)

    # if the ball is moving towards the computer, follow the ball's y coords, if it's moving away from the computer, go to the middle of the field
    point = ball.y if ball.moveX < 0 else window["height"] / 2

    # the y distance between the computer's middle and the point of target
    move = abs(computerMiddle - point)

    # if the distance is greater than the maximum speed, allow only the maximum speed, otherwise move at the speed of the y distance
    move = move if move < maxMove else maxMove

    if computerMiddle > point:  # if the target point is above the computer's middle
        # move up the needed speed
        computer.move(-move)
        # indicate that the computer is going up.
        computerSpeed = -1
    elif computerMiddle < point:  # if the target point is below the computer's middle
        # move down the needed speed
        computer.move(move)
        # indicate that the computer is going up.
        computerSpeed = 1
    else:  # if exactly at the target point
        if ball.moveX < 0:  # if the ball is moving towards the computer
            # make a random 1px move, either up or down, this will help prevent ties
            goUp = random.randint(0, 1)
            if goUp:  # if should go up
                # move up 1px
                computer.move(-1)
                # indicate that the computer is going up
                computerSpeed = -1
            else:
                # move down 1px
                computer.move(1)
                # indicate that the computer is going down
                computerSpeed = 1


def drawCanvas():
    """This function updates the canvas"""
    global computerSpeed, playerScore, computerScore, stop, resultText
    # update the player's position
    movePlayer()
    # update the computer's position
    moveComputer()
    # update the ball's position
    ball.move()

    # do this for both the player's and computer's squares
    for square in (player, computer):
        if isAboveScreen(square):  # if the square is above the screen...
            # move the square down the amount it is off screen
            square.move(-square.y)
        elif isBelowScreen(square):  # if the square is below the screen...
            # move the square up the amount it is off screen
            square.move(window["height"] - square.y - square.height)

    # if the ball is colliding with the player
    if isColliding(ball, player):
        # put the ball right beside the player's paddle
        ball.x = player.x - ball.radius
        # make the ball move the other way
        ball.moveX *= -1
        # if pressing on the up key
        if keys[0]:
            # make the ball move up faster
            ball.moveY -= 0.25

        # if pressing on the down key
        if keys[1]:
            # make the ball move down faster
            ball.moveY += 0.25

    # if the ball is colliding with the computer
    if isColliding(ball, computer):
        # put the ball right beside the computer's paddle
        ball.x = computer.x + computer.width + ball.radius
        # make the ball move the other way
        ball.moveX *= -1
        # make the ball move faster toward the direction that the computer was moving at
        ball.moveY += 0.25 * computerSpeed

    # if the ball hits the top or bottom of the screen
    if (ball.y - ball.radius <= 0) or (ball.y + ball.radius >= window["height"]):
        # make the ball move the other way
        ball.moveY *= -1

    # if the ball goes past the player's paddle
    if ball.x - ball.radius > window["width"]:
        # add one point to the computer's score
        computerScore += 1
        # update the computer's score on the screen
        canvas.itemconfigure(computerScoreDisplay, text=computerScore)
        # temporarily stop the game
        stop = True
    elif ball.x + ball.radius < 0:  # if the ball goes past the computer's paddle
        # add one point to the player's score
        playerScore += 1
        # update the player's score on the screen
        canvas.itemconfigure(playerScoreDisplay, text=playerScore)
        # temporarily stop the game
        stop = True

    # if the game hasn't been temporarily stopped or been paused
    if not stop and not paused:
        # update the canvas after 17ms (canvas updates 60fps)
        canvas.after(17, drawCanvas)
    elif stop:  # if the game has been stopped
        if wonGame(playerScore) or wonGame(computerScore):  # if anyone won the game...
            # put a black rectangle on the screen to make the resulting text clear to read
            canvas.create_rectangle(
                50,
                window["height"] / 2 - 50,
                window["width"] - 50,
                window["height"] / 2 + 50,
                fill="black",
            )
            # if the computer's score is more than the player's score
            if computerScore > playerScore:
                # print "You Lose" in read in the middle of the screen
                resultText = canvas.create_text(
                    window["width"] / 2,
                    window["height"] / 2,
                    fill="red",
                    text="You Lose",
                    font="TkHeaderFont 90",
                    anchor="center",
                )
                # end the game after 5 sec.
                canvas.after(5000, endGame)
            else:  # if the player's score is more than the computer's score
                # print "You Win" in read in the middle of the screen
                resultText = canvas.create_text(
                    window["width"] / 2,
                    window["height"] / 2,
                    fill="green",
                    text="You Win",
                    font="TkHeaderFont 90",
                    anchor="center",
                )
                # end the game after 5 sec.
                canvas.after(5000, endGame)
        else:
            # no one won, restart the round
            restartRound()
            # continue play after 3 sec.
            canvas.after(3000, drawCanvas)


def restartRound():
    """This function restarts the round"""
    global stop
    # we no longer need to stop the game
    stop = False

    # the x middle and y middle of the screen
    newX = window["width"] / 2
    newY = window["height"] / 2

    # put the ball in the center of the screen
    ball.x = newX
    ball.y = newY
    # temporarily set the ball speed to 0
    s = ball.speed
    ball.speed = 0
    # draw the ball on screen
    ball.move()
    # put the ball speed back
    ball.speed = s
    # set a random direction for the ball to go
    ball.moveX = random.choice((-1, 1))
    ball.moveY = random.randint(-100, 100) / 100

    # set the computer's paddle to the middle of the y axis
    computer.y = newY - computer.height / 2
    # draw the computer's paddle
    computer.move(0)

    # set the computer's paddle to the middle of the y axis
    player.y = newY - player.height / 2
    # draw the computer's paddle
    player.move(0)


def startGame():
    """This function initiates the game"""
    global playingGame
    # indicate that the user is playing the game
    playingGame = True

    # show the game canvas
    gamePage.lift()

    # start playing the game after 3 sec.
    canvas.after(3000, drawCanvas)

    # enable the "New Game" and "Pause" options in the menu
    gameMenu.entryconfigure("New Game", state="normal")
    gameMenu.entryconfigure("Pause", state="normal")


def endGame():
    """This function ends the game"""
    global computerScore, playerScore, stop, playingGame
    # indicate that the user is no longer playing the game
    playingGame = False

    # if the "You Won" or "You Lose" text had been drawn
    if resultText != None:
        # remove the black square
        canvas.delete(resultText - 1)
        # remove the "You Won"/"You Lose" text
        canvas.delete(resultText)

    # set the scores to 0
    computerScore = 0
    playerScore = 0

    # display the scores on screen
    canvas.itemconfigure(computerScoreDisplay, text=computerScore)
    canvas.itemconfigure(playerScoreDisplay, text=playerScore)
    # reset all the components
    restartRound()

    # show the start page
    startPage.lift()

    # disable the "New Game" and "Pause" options in the menu
    gameMenu.entryconfigure("New Game", state="disabled")
    gameMenu.entryconfigure("Pause", state="disabled")


def setLvl(l):
    """Set the level to play at"""
    global lvl
    # set the lvl
    lvl = l
    # start the game
    startGame()


def confirmEndGame():
    """Confirms that the user wants to forcefully start a new game"""
    global paused
    if playingGame:  # run only if playing the game
        # pause the game
        paused = True
        # ask the user for a confirmation
        newGame = messagebox.askyesno(
            message="Are you sure you want to stop playing?",
            icon="question",
            title="New Game",
        )
        # unpause the game
        paused = False
        if newGame:  # if user confirms decision...
            # end the game
            endGame()
        else:  # if not...
            # continue game
            drawCanvas()


def pauseGame():
    """This function pauses/unpauses the game"""
    global paused
    if playingGame:  # run if playing the game
        # toggle the pause
        paused = not paused
        if not paused:  # if game isn't paused
            # continue the game
            drawCanvas()


def showHelp():
    """This function shows the help window"""
    global paused

    def closeHelp():
        """This function closes the help window"""
        global paused
        # close the help window
        helpWindow.destroy()

        # unpause the game
        paused = False

        # if user was playing the game
        if playingGame:
            # continue the game
            drawCanvas()

    def selectOption(event):
        """This function parses and displays a help file"""
        # get the option id
        selected = tableOfContents.curselection()[0]

        # enable the content area for editing
        content["state"] = "normal"

        # get the help text
        text = open(str(selected) + ".txt", "r")
        helpText = text.read()
        text.close()

        # remove everything from the content area
        content.delete("1.0", "end")

        # symbols that are open
        openSymbol = {
            "#": False,
            "|": False,
            "$": False,
            "^": False,
        }
        # the style that each symbol represents
        symbolStyle = {
            "#": "title",
            "|": "subtitle",
            "$": "keypress",
            "^": "center",
        }
        # keeps track of how many dashes have been encountered in a row
        encounteredLine = 0

        # go through each character in the help text
        for char in helpText:
            if char in symbolStyle:  # if the character is a special symbol...
                if openSymbol[char]:  # if the character has already been opened
                    # close the symbol
                    openSymbol[char] = False
                else:  # if it's closed
                    # open the symbol
                    openSymbol[char] = True
            elif char == "-":  # if the character is a dash...
                if encounteredLine < 2:  # if met less than 2 dashes in a row...
                    # add the amount encountered
                    encounteredLine += 1
                else:  # if already met 2 dashes in a row
                    # set the amount encountered to 0
                    encounteredLine = 0

                    # insert the amount of horizontal lines needed to fill the width
                    content.insert("end", "‒" * content["width"])
            else:
                # all the styles that should be applied
                styles = []

                # go through each symbol in openSymbol dict.
                for sym in openSymbol:
                    # if the symbol is open
                    if openSymbol[sym]:
                        # append the style that should be applied
                        styles.append(symbolStyle[sym])

                # print the character along with the needed styles
                content.insert("end", char, tuple(styles))

        # disable the content area from editing
        content["state"] = "disabled"

    # pause the game
    paused = True
    # make the help window
    helpWindow = Toplevel()
    # set the title
    helpWindow.title("PyPong Help")
    # disable resizing
    helpWindow.resizable(False, False)
    # make it part of the root window
    helpWindow.transient(root)

    # make the body frame with 5px padding
    body = ttk.Frame(helpWindow, padding=5)
    # place the body frame in the window
    body.grid(row=0, column=0)

    # all the help sections
    sections = (
        "Object of the Game",
        "Who am I?",
        "How to move",
        "How to score a point",
    )
    # put them into a tkinter variable
    sectionsVar = StringVar(value=sections)
    # make a listbox of the sections
    tableOfContents = Listbox(
        body, listvariable=sectionsVar, highlightthickness=0, font="TkTextFont 11"
    )
    # when something is selected, show the help page
    tableOfContents.bind("<<ListboxSelect>>", selectOption)
    # place the listbox in the window
    tableOfContents.grid(row=0, column=0, sticky=(N, E, S, W))

    # make a vertical separator
    ttk.Separator(body, orient=VERTICAL).grid(row=0, column=1, sticky=(N, S))

    # make the content area
    content = Text(
        body,
        width=40,
        height=20,
        highlightthickness=0,
        font="TkFixedFont 12",
        wrap="word",
    )
    # make the style tags for it
    content.tag_configure("center", justify="center")
    content.tag_configure("title", font="TkHeaderFont 20 bold")
    content.tag_configure("subtitle", font="TkHeaderFont 14 bold")
    content.tag_configure(
        "keypress", font="Monospace 8", background="#dddddd", foreground="#aa0000"
    )
    # place the content area in the window
    content.grid(row=0, column=2, sticky=(N, E, S, W))

    # make a small intro in the content area
    content.insert("end", "\n")
    content.insert("end", "Hi! How can I help?\n", ("center", "title"))
    content.insert(
        "end",
        "\nClick on the options on the left to get help on the topic you need",
        ("center"),
    )
    # disable the content area from editing
    content["state"] = "disabled"

    # add a scroll bar
    scroll = ttk.Scrollbar(body, orient=VERTICAL, command=content.yview)
    # set it to work with the content area
    content["yscrollcommand"] = scroll.set
    # put the scrollbar in the window
    scroll.grid(row=0, column=3, sticky=(N, S))

    # add a horizontal separator
    ttk.Separator(body, orient=HORIZONTAL).grid(
        row=1, column=0, columnspan=4, sticky=(W, E)
    )

    # make a close button
    close = ttk.Button(body, text="Close", command=closeHelp, cursor="hand2")
    # put the close button in the window
    close.grid(row=2, column=0, columnspan=4, pady=5)

    # close the window when the user presses Ctrl+W
    helpWindow.bind("<Control-KeyPress-w>", lambda e: closeHelp())


def showAbout():
    """This function shows the about window"""
    global paused

    def displayReadMe():
        """This function shows the README.md file"""
        # show the content area frame
        textContent.grid()
        # enable the content area for editing
        text["state"] = "normal"
        # remove everything from the content area
        text.delete("1.0", "end")
        # open the README.md file
        f = open("README.md", "r")
        # print out the file
        text.insert("end", f.read())
        # close the file
        f.close()
        # disable the content area from editing
        text["state"] = "disabled"

    def displayCredits():
        """This function shows the credits"""
        # show the content area frame
        textContent.grid()
        # enable the content area for editing
        text["state"] = "normal"
        # remove everything from the content area
        text.delete("1.0", "end")
        # put the credits
        text.insert(
            "end",
            "Anton Shapovalov is the creator of this game",
            ("center"),
        )
        # disable the content area from editing
        text["state"] = "disabled"

    def closeAbout():
        """Closes the about window"""
        global paused
        # close the window
        aboutWindow.destroy()
        # unpause the game
        paused = False
        # if user is playing the game
        if playingGame:
            # continue playing
            drawCanvas()

    # pause the game
    paused = True
    # create the window
    aboutWindow = Toplevel()
    # add the title
    aboutWindow.title("About PyPong")
    # disable resizing
    aboutWindow.resizable(False, False)
    # make it part of the root window
    aboutWindow.transient(root)

    # make a body frame with 5px padding
    body = ttk.Frame(aboutWindow, padding=5)
    # put the body in the window
    body.grid(row=0, column=0)

    # put the image along with the name of the game
    title = ttk.Label(
        body, image=logo, text="PyPong", compound=TOP, font="TkDefaultFont 10 bold"
    )
    # put the title in the window
    title.grid(row=0, column=0, columnspan=3)

    # put the version and release year
    ttk.Label(body, text="Version: 1.0 (Released in 2023)").grid(
        row=1, column=0, columnspan=3, pady=5
    )

    # put a extremely small description of the game
    ttk.Label(
        body,
        text="The classic game of pong. Hit the ball with your paddle until it passes the computer's paddle",
        wraplength=400,
        justify="center",
    ).grid(row=2, column=0, columnspan=3, pady=5)

    # put why this game was made
    ttk.Label(
        body, text="This game was made for the CS50 and CTEC121 final project"
    ).grid(row=3, column=0, columnspan=3, pady=5)

    # make the text content frame
    textContent = ttk.Frame(body)
    # put the text content frame in the window
    textContent.grid(row=4, column=0, columnspan=3, pady=5, sticky=(N, E, S, W))
    # hide the text content frame
    textContent.grid_remove()

    # make the text content
    text = Text(textContent, width=51, height=10, highlightthickness=0, wrap="word")
    # make some style tags
    text.tag_configure("center", justify="center")
    # place the text content into the text content frame
    text.grid(row=0, column=0, sticky=(N, E, S, W))

    # make a vertical scroll bar
    scroll = ttk.Scrollbar(textContent, orient=VERTICAL, command=text.yview)
    # place the scrollbar into the text content frame
    scroll.grid(row=0, column=1, sticky=(N, S))
    # make it work with the text content
    text["yscrollcommand"] = scroll.set

    # make the button to see the README.md file
    readMe = ttk.Button(body, text="README file", command=displayReadMe)
    # put the button in the window
    readMe.grid(row=5, column=0, pady=5)

    # make the button to see the credits
    credits = ttk.Button(body, text="Credits", command=displayCredits)
    # put the button in the window
    credits.grid(row=5, column=1, pady=5)

    # make the close button
    close = ttk.Button(body, text="Close", command=closeAbout)
    # put the button in the window
    close.grid(row=5, column=2, pady=5)

    # if the user presses Ctrl+W, close the window
    aboutWindow.bind("<Control-KeyPress-w>", lambda e: closeAbout())


def confirmClose():
    """This function confirms the closing of the whole game"""
    global paused
    # pause the game
    paused = True
    # ask for a confirmation
    shouldClose = messagebox.askyesno(
        message="Are you sure you want to quit?", title="Quit PyPong?", icon="question"
    )
    if shouldClose:  # if the user confirms
        # close the game
        root.destroy()
    else:  # if not
        # unpause the game
        paused = False
        # if user playing the game
        if playingGame:
            # continue playing
            drawCanvas()


def main():
    global startPage, gamePage, player, computer, ball, canvas, computerScoreDisplay, playerScoreDisplay, gameMenu
    # menu bar
    menubar = Menu(root)
    root["menu"] = menubar
    gameMenu = Menu(menubar)
    menubar.add_cascade(menu=gameMenu, label="Game")

    # set up game menu =====
    # add the "New Game" option
    gameMenu.add_command(
        label="New Game", accelerator="Ctrl+N", command=confirmEndGame, state="disabled"
    )
    # add the "Pause" option
    gameMenu.add_command(
        label="Pause", accelerator="Ctrl+P", command=pauseGame, state="disabled"
    )
    # add a separator
    gameMenu.add_separator()
    # add the "About" option
    gameMenu.add_command(label="About", accelerator="F2", command=showAbout)
    # add the "Help" option
    gameMenu.add_command(label="Help", accelerator="F1", command=showHelp)
    # add a separator
    gameMenu.add_separator()
    # add the "Quit" option
    gameMenu.add_command(label="Quit", accelerator="Ctrl+Q", command=confirmClose)
    # =====

    # start page
    startPage = ttk.Frame(style="startPage.TFrame", cursor="left_ptr")
    startPage.grid(row=0, column=0, sticky=(N, E, S, W))

    # add the title of the game
    ttk.Label(
        startPage,
        text="PyPong Game",
        font="TkHeaderFont 30 bold",
        foreground="white",
        background="black",
        padding=5,
    ).grid(row=0, column=0, columnspan=3)

    # tell the user to choose a level
    ttk.Label(
        startPage,
        text="Choose your level:",
        font="TkDefaultFont 16",
        background="black",
        foreground="white",
        padding=(0, 5, 0, 10),
    ).grid(row=1, column=0, columnspan=3)

    # the easy button
    easy = ttk.Button(
        startPage,
        style="option.TButton",
        text="Easy",
        cursor="hand2",
        command=lambda: setLvl("easy"),
    )
    easy.grid(row=2, column=0)

    # the medium button
    medium = ttk.Button(
        startPage,
        style="option.TButton",
        text="Medium",
        cursor="hand2",
        command=lambda: setLvl("medium"),
    )
    medium.grid(row=2, column=1)

    # the hard button
    hard = ttk.Button(
        startPage,
        style="option.TButton",
        text="Hard",
        cursor="hand2",
        command=lambda: setLvl("hard"),
    )
    hard.grid(row=2, column=2)

    # the game page
    gamePage = ttk.Frame(cursor="left_ptr")
    gamePage.grid(row=0, column=0, sticky=(N, E, S, W))
    # hide the game below the start page
    gamePage.lower()

    # the game canvas
    canvas = Canvas(
        gamePage,
        background="black",
        width=window["width"],
        height=window["height"],
        highlightthickness=0,
    )

    # add the dashes in the middle
    canvas.create_line(
        window["width"] / 2,
        0,
        window["width"] / 2,
        window["height"],
        fill="dodgerblue",
        width=5,
        dash=(40, 20),
    )

    # show the computer's side of the field
    canvas.create_text(
        window["width"] / 4,
        5,
        text="Computer",
        anchor="n",
        font="TkDefaultFont 11",
        fill="white",
    )
    # show the player's side of the field
    canvas.create_text(
        window["width"] / 4 * 3,
        5,
        text="You",
        anchor="n",
        font="TkDefaultFont 11",
        fill="white",
    )

    # show the computer's score
    computerScoreDisplay = canvas.create_text(
        window["width"] / 4,
        window["height"] / 2,
        text=computerScore,
        anchor="center",
        font="TkDefaultFont 70",
        fill="white",
    )
    # show the player's score
    playerScoreDisplay = canvas.create_text(
        window["width"] / 4 * 3,
        window["height"] / 2,
        text=playerScore,
        anchor="center",
        font="TkDefaultFont 70",
        fill="white",
    )
    # put the canvas in the game frame
    canvas.grid(row=0, column=0)

    # add the computer's and player's square, along with the ball
    computer = Square(canvas, 5, window["height"] / 2 - 75 / 2)
    player = Square(canvas, window["width"] - 15, window["height"] / 2 - 75 / 2)
    ball = Circle(canvas, window["width"] / 2, window["height"] / 2)

    # allow the start pages columns to resize
    for i in range(3):
        startPage.columnconfigure(i, weight=1)

    # allow the first column and row to resize
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # record what key is being pressed
    root.bind("<KeyPress>", lambda e: getKey(e, True))
    # record what key has been release
    root.bind("<KeyRelease>", lambda e: getKey(e, False))

    # keyboard shortcuts for the menu
    root.bind("<Control-KeyPress-n>", lambda e: confirmEndGame())
    root.bind("<Control-KeyPress-p>", lambda e: pauseGame())
    root.bind("<Control-KeyPress-q>", lambda e: confirmClose())
    root.bind("<KeyPress-F1>", lambda e: showHelp())
    root.bind("<KeyPress-F2>", lambda e: showAbout())

    # show the window
    root.mainloop()


# run main() if running the project
if __name__ == "__main__":
    try:
        # run main()
        main()
    except:
        # Error! Show a message to the user.
        messagebox.showerror(message="Sorry. The program doesn't work on your device.")
