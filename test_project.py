from project import *


def test_isKeyUp():
    # test different key symbols
    assert isKeyUp(-8) == False
    assert isKeyUp("Down") == False
    assert isKeyUp("Up") == True
    assert isKeyUp("Enter") == False


def test_isKeyDown():
    # test different key symbols
    assert isKeyDown("Space") == False
    assert isKeyDown("Down") == True
    assert isKeyDown("Up") == False
    assert isKeyDown(5) == False


def test_wonGame():
    # test different scores and see if won game
    assert wonGame(2) == False
    assert wonGame("Hello") == False
    assert wonGame(5) == True
    assert wonGame(8) == True


def test_getComputerSpeed():
    # test different level inputs and see what speed is returned
    assert getComputerSpeed("easy") == 0.5
    assert getComputerSpeed("medium") == 1
    assert getComputerSpeed("hard") == 1.5
    assert getComputerSpeed(2) == 0
    assert getComputerSpeed("foo") == 0
    assert getComputerSpeed(12.0) == 0
