# PyPong Game
## Video Demo: https://youtu.be/GJxG1UYJ85Y
## Description:

### **About the Game:**
This is the classical game of pong. Pong was first developed by Atari in 1972. Since then, there have been many different versions of it, including 3D versions like Cube Slam (now defunct). My version is a simple one, without any crazy bells or whistles.

### **What the game includes:**
This game comes with three different levels:
* Easy
* Medium
* Hard

The only difference between each level is the speed at which the computer's paddle moves. The easy computer's paddle moves fifty percent of the speed of the user's paddle. The medium computer's paddle moves the same speed as the user's paddle. The hard computer's paddle moves one-hundred and fifty percent of the speed of the user's paddle.

This game also features:
* Playing a new game
* Pausing
* An about page
* A help page
* Keyboard shortcuts

Playing a new game means that if the user is currently playing the game, but wants to play a different level, they can exit out of the game without closing the program. To do this, either press on `Game`>`New Game` or press on `Ctrl+N`/`⌘+N`.

If the user wants to keep playing the level that their on, but currently are unable to, they can pause the game. To do this, they can either press on `Game`>`Pause` or press on `Ctrl+P`/`⌘+P`.

To see the game's about page. Go to `Game`>`About` or press on `F2`. The about page contains this `README.md` file and shows some credits.

To see the game's help page. Go to `Game`>`Help` or press on `F1`. The help page contains a lot of useful information for how to play the game.

### **Design of the code:**
I chose a mix of functional programming and OOP. I chose this kind of design mainly because it's the one I use the most when I make games. When I make games, all of the components that are on the canvas are classes. This makes my code more readable to me. It's also a lot easier for me to move specific components around the canvas because most of the work of actually moving the component is done inside the class structure. I made a separate file called `components.py` that contained all of my classes. This just helps me organize my code. I like to keep classes in one file, and my main functions in a different file. I tried to separate my functions that involved with the game play. This makes the function that runs the game more readable. It also helps remove the risk of breaking something in another part of the code because they are somewhat separate of each other. I did rely heavily on global variables in this project because I found it easier to make my game with them.

### **An in-depth look at the about page:**
You might be wondering why I added an about page. I did this for two reasons. The first reason is that I saw that many games and apps have an about page, so I thought that it would look more professional if I added an about page. The second reason is that I felt like adding something more to the game and the only thing that made sense to add was an about page.

The about page has three main things on it:
* Miscellaneous info
* The README file
* Credits

The **Miscellaneous Info** is just the title of the game, along with a logo, a version number along with the release year, a two sentence description of the game, and the reason why the game was made.

The **README file** is a button that, when clicked on, shows the contents of this `README.md` file. I noticed how some apps have this and so I decided to do the same.

The **Credits** is a button that, when clicked on, shows who made the game. In other words, it tells everybody that I made the game.

### **An in-depth look at the help page:**
There are four sections in the help contents:
* Object of the Game
* Who am I?
* How to move
* How to score a point

The **Object of the Game** section gives a short, three sentence long, of what goal is. It then tells the user that the goal might be simple, but that it's not easy to attain.

The **Who am I?** section tells the user how to know which paddle is theirs and which is the computers.

The **How to move** section tells the user how to move their paddle. It also tells the user how they can change the speed of the ball while they move their paddle.

The **How to score a point** section tells the user how to score points in the game. It also tells the user how many points are needed to win the game.

All of the help texts are stored in 4 different `.txt` files (`[0-4].txt`). To make styling and writing the help files easier, I developed my MarkDown-type language. I've used something similar in different projects and have found it useful. So I decided to do the same for this project as well. This language allows five different styles:
* Title
* Subtitle
* Centering text
* Making the text "code like"
* Making a horizontal line

 The first four styles in the list follow this type of syntax: `[symbol][text][symbol]`. Here's a list of the symbols, what they do, and an example of how to use them:
 * \#, Makes a title, #Hello World#
 * |, Makes a Subtitle, |Hello World|
 * ^, Centers the text, ^Hello World^
 * \`, Makes the text "code like", \`asdf\`

 To make a horizontal line, you put three dashes, like so: `---`

 ### **An in-depth look into the computer AI:**
 For beginners, making a computer play against a human can seem like a daunting task. This is what I use to think. But as I gained experience in programming, I realized that making a computer AI for certain games can be very simple. This is one of those games. The algorithm is pretty simple. If the ball is moving towards the computer's paddle, then the computer follows the direction the ball is going. If the ball is going up, the computer goes up. If the ball is going down, the computer goes down. If the ball is neither going up nor down, then the computer stays still. If the computer is staying still, then this can cause a problem. The computer will just bounce the ball back to the player without try to change the ball's direction. If the player does the same thing, then a sort of "draw" is made. To prevent this, I made the computer make a random move either up or down right before it hits the ball so that it can prevent such draws. If, however, the ball is going away from the computer, then the computer goes to the middle of the screen. This makes it seem more human-like because it looks like it knows that, if it goes to the middle, then it can reach the place that the ball will travel towards once it's hit by the player.

 That's all there is to the algorithm. Yes, it's true that the computer isn't *very* smart and that there are way better algorithms for this game, but it can take some time to beat it and I feel that it's good enough.

 To make the easy, medium, and hard version of the computer, I just changed the speed of the computer's paddle. This in fact does make it look like the computer is playing smarter when the level gets harder. I was initially surprised at the outcome. I thought it would be a little obvious why the computer gets harder, but after some playing the game several times, I find that it's pretty hard to detect by the casual player.

 ### **Why Pong?**
 This is already the third Pong game I've made. I made two other Pong games using a different language, but this is the first one that I made with Python. So why did I make a third Pong game? Two reasons. First, I knew what to expect. I knew what algorithm to use for the computer, and I had a pretty good mental picture of what it would look like. Second, it's a fun game to make. One of the great things about Pong is that it looks pretty advanced, in some ways it is, but the best thing about it is that you can make a computer AI without to much trouble and still impress people with it.

 ### **Ways to make the game better:**
 There is no such thing as a "finished" program. There is always something you can improve in any program. This game is no exception. One of the biggest ways I can improve this game is to make the computer AI smarter. Instead of having the computer follow the ball, I can have the AI figure out where the ball is going to land once it reaches the computer's side of the screen. Another thing I can do is to allow two users play on the same computer against each other. In fact, you can also say I might as well try to make it so that two users can play against each other from two different computers on a network. There are so many different ways I can improve this game that it would take another `README.md` file to write it all out. If whoever is reading this feels that they can improve this game, I encourage you to go ahead and do it. You can send me your code to me on GitHub at https://github.com/JsPyProgrammer