from tkinter import Tk, mainloop
from board import Board
from threading import Thread
from playsound import playsound


def play_theme():
    while True:
        playsound('mystery.mp3')
    

root = Tk()
root.title('Tetris')
HEIGHT, WIDTH = 500, 400
Thread(target=play_theme).start()
Board(root, HEIGHT, WIDTH, 'light blue', 1000)
mainloop()
