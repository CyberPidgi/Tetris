from piece import *
from keys import Keys
from tkinter import Canvas
from random import choice


class Board:

    board_state = []
    current_board_state = []
    current_piece = None

    def __init__(self, master, height, width, colour, fps):
        self.master = master
        self.screen = Canvas(self.master, height=height, width=width, bg=colour)
        self.screen.pack()
        self.master.bind('<Key>', self.get_keypress)

        num_of_rows = height / BLOCK_WIDTH
        num_of_columns = width / BLOCK_WIDTH

        if int(num_of_rows) != num_of_rows or int(num_of_columns) != num_of_columns:
            raise Exception(f"Height or Width is not a multiple of {BLOCK_WIDTH}")

        num_of_rows, num_of_columns = map(int, (num_of_rows, num_of_columns))
        for i in range(num_of_rows):
            empty_list = []
            for j in range(num_of_columns):
                empty_list.append(EMPTY)
            Board.board_state.append(empty_list)

        Piece.display = self.screen
        Piece.num_of_columns = num_of_columns
        Piece.num_of_rows = num_of_rows
        Piece.board = Board.board_state

        Board.generate_new_piece()
        self.master.after(fps, self.update)

    @staticmethod
    def generate_new_piece():
        Board.current_piece = choice(Blocks.__subclasses__()).init()

        # Board.current_piece = Line.init()
        # Board.current_piece = L.init()
        # Board.current_piece = LongerL.init()
        # Board.current_piece = ZigZag.init()
        # Board.current_piece = T.init()

        # block = Piece(0, Piece.num_of_columns // 2)
        # Board.current_piece = Blocks((block,))
        Board.add_piece_to_board(Board.current_piece)

    def update(self):
        # if the piece has reached the last row, or if it has collided with another piece
        # there is no point in updating the piece, so we generate a new one.
        if Board.current_piece.is_stationary:
            Board.generate_new_piece()

        # auto move piece down
        Board.remove_piece_from_board(Board.current_piece)
        Board.current_piece.move(Keys.DOWN)
        Board.add_piece_to_board(Board.current_piece)

        # clear a line if there are no empty spaces
        num_of_cleared_lines = 0
        for index, row in enumerate(Board.board_state):
            if EMPTY not in row:
                if not all([block.is_stationary for block in row]):
                    continue
                [block.go_poof() for block in row]
                Board.board_state[index] = [EMPTY for _ in range(len(row))]
                num_of_cleared_lines += 1

        # move all the blocks down if lines were cleared
        if num_of_cleared_lines:
            for row in Board.board_state[::-1]:
                for block in row:
                    if block == EMPTY or not block.is_stationary:
                        continue
                    block.is_stationary = False
                    Board.remove_piece_from_board(Blocks((block,)))
                    [block.move(Keys.DOWN) for _ in range(Piece.num_of_rows)]
                    Board.add_piece_to_board(Blocks((block,)))
                    block.is_stationary = True

        # update the board for class Piece as well
        Piece.board = Board.board_state

        self.master.after(1000, self.update)

    @staticmethod
    def remove_piece_from_board(piece):
        for block in piece.blocks:
            Board.board_state[block.row][block.column] = EMPTY

    @staticmethod
    def add_piece_to_board(piece):
        for block in piece.blocks:
            Board.board_state[block.row][block.column] = block

    @staticmethod
    def get_keypress(event):
        Board.remove_piece_from_board(Board.current_piece)

        if event.keycode == 37:
            Board.current_piece.move(Keys.LEFT)

        if event.keycode == 38:
            Board.current_piece.move(Keys.UP)

        elif event.keycode == 39:
            Board.current_piece.move(Keys.RIGHT)

        elif event.keycode == 40:
            Board.current_piece.move(Keys.DOWN)

        Board.add_piece_to_board(Board.current_piece)
