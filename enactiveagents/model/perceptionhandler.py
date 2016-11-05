"""
Module that holds classes that represent an agent's perception handler.
"""

import abc
import world
import structure

class PerceptionHandler(object):
    """
    Abstract perception handler class.
    """

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
    """
    A trivial perception handler that never perceives anything.
    """

    def perceive(self, agent, world):
        return ""

class BasicPerceptionHandler(PerceptionHandler):
    """
    A perception handler that perceives walls and blocks up to a given distance.
    The perception indicates the type of structure that is seen, as well as its
    distance.
    """

    def perceive(self, agent_, world_):
        for delta in range(0, 10):
            pos = world.Position(agent_.get_position())

            pos.add(agent_.get_move_delta(delta))

            entities = world_.get_entities_at(pos)
            for entity in entities:
                if entity == agent_:
                    continue
                if isinstance(entity, structure.Wall):
                    return "w%s" % delta
                elif isinstance(entity, structure.Block):
                    return "b%s" % delta
                elif isinstance(entity, structure.Food):
                    return "f%s" % delta

        return ""