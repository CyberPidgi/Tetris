from keys import Keys

BLOCK_WIDTH = 20
EMPTY = 0


class Block:

    display = None
    board = None
    colour = 'red'
    outline = 'black'
    _type = None
    num_of_rows = 0
    num_of_columns = 0

    # rotation is done in anticlockwise direction
    _ROTATION_TUPLE = ([1, -1], [1, 1], [-1, 1], [-1, -1])

    def __init__(self, row, column, num_of_rotations=(1, 1), start_rotation_at=0, colour=None, outline=None):
        self.colour = colour or Block.colour
        self.outline = outline or Block.outline
        self._type = Block._type
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
        self._name = Block.display.create_rectangle(x1, y1, x2, y2, fill=self.colour, outline=self.outline)

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

        elif Block.board[new_row_index][self.column] != EMPTY:
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
        elif Block.board[self.row][new_column_index] != EMPTY:
            return

        self.has_collided = False
        self._column = new_column_index

    def rotate(self):
        if self.num_of_rotations == (0, 0):
            return

        row, column = Block._ROTATION_TUPLE[self.rotation_index]
        row *= self.num_of_rotations[0]
        column *= self.num_of_rotations[1]

        self.row += row
        self.column += column

        self.rotation_index += 1

        if self.rotation_index >= len(Block._ROTATION_TUPLE):
            self.rotation_index = 0

        # this is implemented for the function to work with pieces like LongerL and ZigZag and the like
        # it doesn't work for them as their rotational points change at each rotation
        self.num_of_rotations = self.num_of_rotations[::-1]

    def hard_drop(self):
        pass

    def move_n_times(self, key, n):
        for _ in range(n):
            self.move(key)

    def move(self, key):

        if key == Keys.LEFT:
            self.column -= 1
        elif key == Keys.RIGHT:
            self.column += 1

        elif key == Keys.UP:
            self.rotate()
        elif key == Keys.DOWN:
            self.row += 1

        elif key == Keys.SPACE_BAR:
            self.hard_drop()

        self.create()

    def go_poof(self):
        Block.display.delete(self._name)

    def __str__(self):
        return f'Block(row={self.row} column={self.column} has_collided={self.has_collided}' \
            f' is_stationary={self.is_stationary} colour={self.colour} class={self._type})'
