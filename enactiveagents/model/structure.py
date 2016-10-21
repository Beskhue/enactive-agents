"""
Module that holds classes that represent structures.
"""

import world

class Structure(world.Entity):
    """
    Class representing structures in the world (i.e., static but potentially
    interactable with by agents).
    """
    def collidable(self):
        return True

class Wall(Structure):
    """
    Class representing a wall structure.
    """
    def __init__(self):
        super(Wall, self).__init__()
        self.height = 1
        self.width = 1

class Block(Structure):
    """
    Class representing a block structure.
    """

    color = (122, 179, 62, 255)

    def collidable(self):
        return False