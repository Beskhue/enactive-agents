"""
Module that holds classes that represent an agent's perception handler.
"""

import abc
import world
import structure

class PerceptionHandler(object):

    @abc.abstractmethod
    def perceive(self, agent, world):
        """
        Generates a percept given an agent and a world.

        :param agent: The agent to generate the percept for.
        :param world: The world to generate the percept for.
        :return: The percept.
        """
        raise NotImplementedError("Should be implemented by child")

class EmptyPerceptionHandler(PerceptionHandler):

    def perceive(self, agent, world):
        return ""

class BasicPerceptionHandler(PerceptionHandler):

    def perceive(self, agent_, world_):
        for delta in range(1, 10):
            pos = world.Position(agent_.get_position())
            pos.add(agent_.get_move_delta(delta))

            entities = world_.get_entities_at(pos)
            if len(entities) > 0:
                if isinstance(entities[0], structure.Wall):
                    return "w%s" % delta

        return ""