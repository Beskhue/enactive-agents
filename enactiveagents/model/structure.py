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