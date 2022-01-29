from typing import Union, List, Tuple
from abc import abstractmethod
from block import Block
from keys import Keys


class Blocks:
    """
    Used to emulate multiple blocks as a single entity
    """

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

    def rotate_at_edge(self):
        # picky boi wanted it to spin even when it was in the edge
        if all([block.column > Block.num_of_columns - 3 for block in self.blocks]):
            self.move_all_blocks(Keys.LEFT)

        elif all([block.column < 2 for block in self.blocks]):
            self.move_all_blocks(Keys.RIGHT)

        self.move_all_blocks(Keys.UP)

    def move(self, key):
        old_positions = self.all_blocks_coordinates
        old_rotational_indexes = self.all_blocks_rotational_indexes

        for block in self.blocks:

            # not sure why moving the block first fixes everything
            # but it does, so keep it here buddy
            block.move(key)

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
                if key == Keys.UP:
                    self.rotate_at_edge()
                    return
                return

    def move_all_blocks(self, key):
        for block in self.blocks:
            block.move(key)

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

    @staticmethod
    @abstractmethod
    def init():
        pass
