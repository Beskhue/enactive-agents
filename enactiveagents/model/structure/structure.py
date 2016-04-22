"""
Module that holds classes that represent structures.
"""

import model.world

class Structure(model.world.Entity):
    vertices = [[0,0], [0, 1], [1, 1], [1, 0]]

    def collidable(self):
        return True

class Wall(Structure):
    def __init__():
        super(Wall, self).__init__()
        self.height = 1
        self.width = 1