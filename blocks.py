from random import randrange
from typing import Union, List, Tuple
from keys import Keys

BLOCK_WIDTH = 20
EMPTY = 0


class Piece:

    display = None
    board = None
    colour = 'red'
    outline = 'black'
    _type = None
    num_of_rows = 0
    num_of_columns = 0
    _ROTATION_TUPLE = ([1, -1],
                       [1, 1],
                       [-1, 1],
                       [-1, -1])

    def __init__(self, row, column, num_of_rotations=(1, 1), start_rotation_at=0, colour=None, outline=None):
        self.colour = colour or Piece.colour
        self.outline = outline or Piece.outline
        self._type = Piece._type
        self._row = row
        self._column = column
        self.num_of_rotations = num_of_rotations
        self.rotation_index = start_rotation_at

        self._name = None
        self.is_stationary = False
        self.has_collided = False
        self.create()

    def create(self):
        if self._name is not None:
            self.display.delete(self._name)
        x1, y1 = self.column * BLOCK_WIDTH, self.row * BLOCK_WIDTH
        x2, y2 = x1 + BLOCK_WIDTH, y1 + BLOCK_WIDTH
        self._name = Piece.display.create_rectangle(x1, y1, x2, y2, fill=self.colour, outline=self.outline)

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, new_row_index):

        if new_row_index < 0:
            self._row = 0
            return

        elif new_row_index > self.num_of_rows - 1:
            self._row = self.num_of_rows - 1
            self.is_stationary = True
            return

        elif Piece.board[new_row_index][self.column] != EMPTY:
            self.is_stationary = True
            self.has_collided = True
            return

        self._row = new_row_index

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, new_column_index):
        self.has_collided = True

        if new_column_index < 0:
            self._column = 0
            return
        elif new_column_index > self.num_of_columns - 1:
            self._column = self.num_of_columns - 1
            return
        elif Piece.board[self.row][new_column_index] != EMPTY:
            return

        self.has_collided = False
        self._column = new_column_index

    def rotate(self):
        if self.num_of_rotations == (0, 0):
            return

        row, column = Piece._ROTATION_TUPLE[self.rotation_index]
        row *= self.num_of_rotations[0]
        column *= self.num_of_rotations[1]

        new_row = self.row + row
        new_column = self.column + column

        self.row = new_row
        self.column = new_column

        self.rotation_index += 1

        if self.rotation_index >= len(Piece._ROTATION_TUPLE):
            self.rotation_index = 0

        # this is implemented for the function to work with pieces like LongerL and ZigZag and the like
        # it doesn't work for them as their rotational points change at each rotation
        self.num_of_rotations = self.num_of_rotations[::-1]

    def hard_drop(self):
        # TODO implement this function
        pass

    def move(self, direction):

        if direction == Keys.LEFT:
            self.column -= 1
        elif direction == Keys.RIGHT:
            self.column += 1

        elif direction == Keys.UP:
            self.rotate()
        elif direction == Keys.DOWN:
            self.row += 1

        elif direction == Keys.SPACE_BAR:
            self.hard_drop()

        self.create()

    def go_poof(self):
        Piece.display.delete(self._name)

    def __str__(self):
        return f'Piece(row={self.row} column={self.column} has_collided={self.has_collided}' \
            f' is_stationary={self.is_stationary} colour={self.colour} class={self._type})'


class Blocks:

    def __init__(self, blocks: Union[List, Tuple]):
        self.blocks = blocks

    def reset(self, old_positions, old_rotational_indexes):
        for block, position, rotation_idx in zip(self.blocks, old_positions, old_rotational_indexes):
            block.row, block.column = position
            block.rotation_index = rotation_idx
            block.create()

    @property
    def all_blocks_coordinates(self):
        return [(block.row, block.column) for block in self.blocks]

    @property
    def all_blocks_rotational_indexes(self):
        return [block.rotation_index for block in self.blocks]

    def picky_bois_function(self):
        # picky boi wanted it to spin even when it was in the edge
        if all([block.column > Piece.num_of_columns - 3 for block in self.blocks]):
            [block.move(Keys.LEFT) for block in self.blocks]

        elif all([block.column < 2 for block in self.blocks]):
            [block.move(Keys.RIGHT) for block in self.blocks]

        for block in self.blocks:
            block.move(Keys.UP)

    def move(self, direction):
        old_positions = self.all_blocks_coordinates
        old_rotational_indexes = self.all_blocks_rotational_indexes

        for block in self.blocks:

            # not sure why moving the block first fixes everything
            # but it does, so keep it here buddy
            block.move(direction)

            if self.is_stationary:
                current_positions = self.all_blocks_coordinates
                if current_positions != old_positions:
                    self.reset(old_positions, old_rotational_indexes)

                for block_ in self.blocks:
                    block_.is_stationary = True
                return

            if block.has_collided:
                # if any of the blocks were unable to move cause of any piece blocking it
                # reset all the blocks positions (all, as the stopped block would have the same position)
                self.reset(old_positions, old_rotational_indexes)
                if direction == Keys.UP:
                    self.picky_bois_function()
                    return
                return

    @property
    def is_stationary(self):
        for block in self.blocks:
            if block.is_stationary:
                return True
        return False

    @property
    def has_collided(self):
        for block in self.blocks:
            if block.has_collided:
                return True
        return False


class Line(Blocks):
    colour = 'orange'

    @staticmethod
    def init():
        Piece.colour = Line.colour
        Piece._type = 'Line'
        column = randrange(1, Piece.num_of_columns)
        block1 = Piece(0, column, num_of_rotations=(1, 1), start_rotation_at=0)
        block2 = Piece(block1.row + 1, block1.column, num_of_rotations=(0, 0))
        block3 = Piece(block1.row + 2, block1.column, num_of_rotations=(1, 1), start_rotation_at=2)

        return Blocks((block1, block2, block3))


class L(Blocks):
    colour = 'yellow'

    @staticmethod
    def init():
        Piece.colour = L.colour
        Piece._type = 'L'
        column = randrange(1, Piece.num_of_columns - 1)
        block1 = Piece(0, column, num_of_rotations=(1, 1))
        block2 = Piece(block1.row + 1, block1.column, num_of_rotations=(0, 0))
        block3 = Piece(block2.row, block2.column + 1, num_of_rotations=(1, 1), start_rotation_at=3)

        return Blocks((block1, block2, block3))


class LongerL(Blocks):
    colour = 'purple'

    @staticmethod
    def init():
        Piece.colour = LongerL.colour
        Piece._type = 'LongerL'
        column = randrange(1, Piece.num_of_columns)
        block1 = Piece(0, column, num_of_rotations=(1, 1), start_rotation_at=0)
        block2 = Piece(block1.row + 1, block1.column, num_of_rotations=(0, 0))
        block3 = Piece(block1.row + 2, block1.column, num_of_rotations=(1, 1), start_rotation_at=2)
        block4 = Piece(block1.row, block1.column - 1, num_of_rotations=(2, 0), start_rotation_at=0)

        return Blocks((block1, block2, block3, block4))


class ReversedLongerL:
    pass


class Square:
    pass


class T(Blocks):
    colour = 'green'

    @staticmethod
    def init():
        Piece.colour = T.colour
        Piece._type = 'T'
        column = randrange(1, Piece.num_of_columns - 1)
        block1 = Piece(0, column, num_of_rotations=(1, 1))
        block2 = Piece(block1.row + 1, block1.column, num_of_rotations=(0, 0))  # the centre block
        block3 = Piece(block2.row, block2.column - 1, start_rotation_at=1)
        block4 = Piece(block2.row, block2.column + 1, start_rotation_at=3)

        return Blocks((block1, block2, block3, block4))


class ZigZag(Blocks):
    colour = 'red'

    @staticmethod
    def init():
        Piece.colour = ZigZag.colour
        Piece._type = 'ZigZag'
        column = randrange(1, Piece.num_of_columns - 1)
        block1 = Piece(0, column, num_of_rotations=(1, 1), start_rotation_at=0)
        block2 = Piece(block1.row + 1, block1.column, num_of_rotations=(0, 0))
        block3 = Piece(block2.row, block2.column + 1, start_rotation_at=3)
        block4 = Piece(block3.row + 1, block3.column, start_rotation_at=3, num_of_rotations=(2, 0))

        return Blocks((block1, block2, block3, block4))


class ReversedZigZag:
    pass
