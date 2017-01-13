import abc
import math

class Entity(object):
    """
    Class that represents an entity that can be placed in a world.

    The position of the entity is its top-left corner.
    """

    width = 1
    height = 1
    step_size = 1
    rect = None

    def __init__(self, position = None, rotation = 0):
        if position is None:
            self.position = Position()
        else:
            self.position = Position(position)
        self.rotation = rotation

    def get_position(self):
        return self.position

    def get_spanning_positions(self):
        """
        As an entity can be larger than 1x1, it might span multiple cells.
        This method returns a list of all cells the entity spans over.
        
        :return: A list of all positions (cells) the entity spans over.
        """

        positions = []

        for dx in range(self.width):
            for dy in range(self.height):
                pos = Position(self.position)
                pos.add((dx, dy))
                positions.append(pos)

        return positions

    def get_rotation(self):
        return self.rotation

    def get_rect(self):
        return (self.position.get_x(), self.position.get_y(), width, height)

    def set_position(self, position):
        self.position.set(position)

    def set_rotation(self, rotation):
        self.rotation = rotation % 360

    def add_position(self, positionDelta):
        self.position.add(positionDelta)

    def add_rotation(self, rotationDelta):
        self.rotation += rotationDelta
        self.rotation = self.rotation % 360

    def at(self, position):
        """
        Test if this entity is at a certain position (i.e., the position is 
        inside the entity's rectangle).
        :param position: The position to check.
        :return: True if the position is inside the entity's rectangle.
        """
        if not isinstance(position, Position):
            position = Position(position)

        return inside(
            (
                self.position.get_x(),
                self.position.get_y(),
                self.width, 
                self.height
            ),
            position
        )

    def step(self):
        """
        Move the entity one step.
        """
        self.move(1)

    def move(self, steps):
        """
        Move the entity a certain number of steps.
        :param steps: The number of steps to move the agent.
        """
        self.position.add(self.get_move_delta(steps))

    def get_move_delta(self, steps = 1):
        """
        Get the change in position if the agent were to move.
        :param steps: The number of steps the agent would move.
        """
        angle = math.radians(self.rotation)
        sine = math.sin(angle)
        cos = math.cos(angle)
        return (
            steps * self.step_size * cos, 
            -steps * self.step_size * sine
        )
        

    def collide(self, other):
        """
        Get whether this entity and the other entity or rect are intersecting.
        If other is a rect, it should be in the form of:
        [x, y, width, height]
        :param other: The entity or rect to check for collision with this entity.
        """
        if not self.collidable():
            return false

        if isinstance(other, Entity):
            return collide(
                (
                    self.position.get_x(),
                    self.position.get_y(),
                    self.width, 
                    self.height
                ),
                (
                    other.position.get_x(),
                    other.position.get_y(),
                    other.width, 
                    other.height
                )
            )
        else:
            return collide(
                (
                    self.position.get_x(),
                    self.position.get_y(),
                    self.width, 
                    self.height
                ), 
                other
            )

    def get_color(self):
        """
        Get the color of the entity.
        :return: The color of the entity.
        :rtype: (int, int, int, int)
        """
        if hasattr(self, 'color'):
            return self.color
        else:
            return (255,255,255,255)

    def set_color(self, color):
        """
        Set the color of the entity.
        :param color: The color to set the entity to.
        :type color: (int, int, int, int)
        """
        self.color = color

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    @abc.abstractmethod
    def collidable(self):
        """
        Return whether entities can collide with this object.
        :return: True if entities can collide with this object, false otherwise.
        :rtype: bool
        """
        raise NotImplementedError("Should be implemented in child")

class Position:
    
    x = 0
    y = 0
    PRECISION = 5

    def __init__(self, position=None):
        if not position is None:
            if isinstance(position, Position):
                self.x = Position.round(position.x)
                self.y = Position.round(position.y)
            else:
                self.x = Position.round(position[0])
                self.y = Position.round(position[1])

    @staticmethod
    def round(n):
        return round(n, Position.PRECISION)

    def get(self):
        return (self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set(self, position):
        if not isinstance(position, Position):
            position = Position(position)

        self.x = Position.round(position.x)
        self.y = Position.round(position.y)

    def add(self, delta):
        self.x = Position.round(self.x + delta[0])
        self.y = Position.round(self.y + delta[1])

    def manhattan_distance_to(self, other):
        """
        Get the manhattan distance between this position and a given position.

        :param other: The given position.
        """
        return (abs(self.get_x() - other.get_x()) + abs(self.get_y() - other.get_y()))

    def angle_to(self, other):
        """
        Get the angle between this position and a given position.
        """
        delta = Position(other)
        delta.add((-self.x, -self.y))

        # Angle of delta with vector (1,0)
        angle = math.degrees(math.acos(delta.get_x() / math.sqrt(delta.get_x()**2 + delta.get_y()**2)))
        if delta.get_y() > 0:
            angle = -angle
        return angle

    def __hash__(self):
        return hash((hash(self.x),  hash(self.y)))

    def __eq__(self, other):
        if not isinstance(other, Position):
            other = Position(other)

        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not self == other

def collide(r1, r2):
    """
    Test if two rectangles collide.
    :param r1: The first rectangle.
    :param r2: The second rectangle.
    """
    return not (
        r2[0] >= r1[0]+r1[2] or # Left side of r2 is to the right of right side of r1
        r2[0]+r2[2] <= r1[0] or # Right side of r2 is to the left of left side of r1
        r2[1] >= r1[1]+r1[3] or # Top of r2 is below of bottom of r1
        r2[1]+r2[3] <= r1[1] # Bottom of r2 is above top of r1
    )

def inside(r, p):
    """
    Test if a point is inside a rectangle.
    :param r: The rectangle.
    :param p: The point.
    """
    return not (
        p.get_x() < r[0] or
        p.get_y() < r[1] or
        p.get_x() >= r[0] + r[2] or
        p.get_y() >= r[1] + r[3]
    )