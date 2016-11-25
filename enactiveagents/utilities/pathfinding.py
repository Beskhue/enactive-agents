"""
Module containing pathfinding utilities.
"""

import model
import Queue

class Pathfinding(object):

    @staticmethod
    def get_neighbours(world, position):
        """
        Get all neighbours of a given position (cell).

        :param world: The world
        :param position: The given position (cell)
        """ 
        neighbours = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                if (position.get_x() + dx < 0 
                    or position.get_y() + dy < 0 
                    or position.get_x() + dx >= world.get_width() 
                    or position.get_y() + dy >= world.get_height()):
                    continue

                new_position = model.world.Position(position)
                new_position.add((dx, dy))

                add = True
                entities = world.get_entities_at(new_position)
                for entity in entities:
                    if entity.collidable():
                        add = False
                        break

                if add:
                    neighbours.append(new_position)

        return neighbours

    @staticmethod
    def heuristic(start, goal):
        """ 
        Calculate the heuristic cost to get from start to the goal.

        :param start: The starting position
        :param goal: The goal position
        """
        return abs(start.get_x() - goal.get_x()) + abs(start.get_y() - goal.get_y())

    @staticmethod
    def reconstruct_path(backtrack, goal):
        path = []

        current = goal
        while backtrack[current] != None:
            path.append(current)
            current = backtrack[current]

        return path

    @staticmethod
    def find_path(world, start, goal, tolerance = 0):
        """
        Implements the A* algorithm to find a path from the start to the goal.

        :param world: The world
        :param start: The starting position
        :param goal: The goal position
        :param tolerance: The heuristic tolerance distance (e.g., at a tolerance
                          of 0 the path should go to the exact goal. At a tolerance
                          of 1 the path should end within 1 cell distance to
                          the goal)
        """
        priority_queue = Queue.PriorityQueue()
        priority_queue.put(start, 0)

        backtrack = {}
        cost_to = {}

        backtrack[start] = None
        cost_to[start] = 0

        while not priority_queue.empty():
            current = priority_queue.get()

            if current == goal or Pathfinding.heuristic(current, goal) <= tolerance:
                # The goal has been found (or we're within tolerance distance),
                # so stop searching
                goal = current
                break

            for neighbour in Pathfinding.get_neighbours(world, current):
                cost_to_neighbour = cost_to[current] + 1

                if neighbour not in cost_to or cost_to_neighbour < cost_to[neighbour]:
                    cost_to[neighbour] = cost_to_neighbour
                    backtrack[neighbour] = current
                    priority = cost_to_neighbour + Pathfinding.heuristic(neighbour, goal)
                    priority_queue.put(neighbour, priority)

        return (Pathfinding.reconstruct_path(backtrack, goal), cost_to[goal])