"""
Module that holds classes that represent an agent's perception handler.
"""

import abc
import entity
import agent
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
            pos = entity.Position(agent_.get_position())

            pos.add(agent_.get_move_delta(delta))

            entities = world_.get_entities_at(pos)
            for entity_ in entities:
                if entity_ == agent_:
                    continue
                if isinstance(entity_, agent.Agent):
                    return "a%s" % delta
                elif isinstance(entity_, structure.Wall):
                    return "w%s" % delta
                elif isinstance(entity_, structure.Block):
                    return "b%s" % delta
                elif isinstance(entity_, structure.Food):
                    return "f%s" % delta

        return ""

class PersistentPerceptionHandler(PerceptionHandler):
    """
    A perception handler that has a persistent perception. Perceives changes
    in the line of sight: objects that appeared, got closer, further away, etc. 
    """

    def __init__(self):
        self.previous_perception = None

    def perceive(self, agent_, world_):

        perception = None

        for delta in range(0, 10):
            pos = entity.Position(agent_.get_position())

            pos.add(agent_.get_move_delta(delta))

            entities = world_.get_entities_at(pos)
            for entity_ in entities:
                if entity_ == agent_:
                    continue
                if isinstance(entity_, agent.Agent):
                    perception = ("agent", delta)
                    break
                elif isinstance(entity_, structure.Wall):
                    perception = ("wall", delta)
                    break
                elif isinstance(entity_, structure.Block):
                    perception = ("block", delta)
                    break
                elif isinstance(entity_, structure.Food):
                    perception = ("food", delta)
                    break
            
            if perception != None:
                break
          
        previous_perception = self.previous_perception
        self.previous_perception = perception

        if perception == None:
            return ""  
        elif perception[1] == 0:
            return "%s on top" % perception[0]
        elif perception[1] == 1:
            return "%s in front" % perception[0]
        elif previous_perception != None and perception[0] == previous_perception[0]:
            if perception[1] < previous_perception[1]:
                return "%s got closer" % perception[0]
            elif perception[1] == previous_perception[1]:
                return "%s unchanged" % perception[0]
            else:
                return "%s got further away" % perception[0]
        else:
            return "%s appeared" % perception[0]
