"""
Module that holds classes that represent structures.
"""

import entity

class Structure(entity.Entity):
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
    pass

class Block(Structure):
    """
    Class representing a block structure.
    """

    color = (179, 62, 179, 255)

    def collidable(self):
        return False

class Food(Structure):
    """
    Class representing food.
    """

    color = (62, 179, 122, 255)

    def collidable(self):
        return False
