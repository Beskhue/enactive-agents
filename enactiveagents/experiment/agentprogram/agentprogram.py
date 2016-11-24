import abc
import model.agent
import appstate
from utilities.pathfinding import Pathfinding

class AgentProgram(object):

    def __init__(self, world = None, agent = None):
        self.world = world
        self.agent = agent

    def get_nearest_food(self, agent):
        food = []
        for entity in self.world.get_entities():
            if isinstance(entity, model.structure.Food):
                food.append((self.agent.get_position().manhattan_distance_to(entity.get_position()), entity))

        food.sort(reverse = True, key = lambda tuple: tuple[0])
        if len(food) > 0:
            return food[0]
        else:
            return None

    def get_direction_to_position(self, position):
        """
        Get the direction (left, right, backward, straight ahead) of a position
        for this agent.
        
        :param position: The position to get the direction for.
        :return: "a" for ahead, "l" for left, "r" for right, "b" for behind
        """
        pos_angle = self.agent.get_position().angle_to(position)
        angle_to = abs(pos_angle - self.agent.get_rotation())

        if angle_to <= 45 or angle_to >= 315:
            return "a"
        elif angle_to <= 135:
            return "l"
        elif angle_to <= 225:
            return "r"
        else:
            return "b"

    @abc.abstractmethod
    def get_interaction(self, percept):
        """
        Get the interaction to enact.

        :return: The primitive interaction that the enact should enact.
        """
        raise NotImplementedError("Should be implemented by child.")

    def set_world(self, world):
        self.world = world

    def set_agent(self, agent):
        self.agent = agent

class TrivialAgentProgram(AgentProgram):
    """
    A trivial agent program that simply attempts to perform the first primitive
    known by the agent.
    """
    def get_interaction(self, percept):
        interaction_memory = self.agent.interaction_memory
        return interaction_memory.get_primitive_interactions()[0]

class SimpleEatingAndDestroyingAgent(AgentProgram):
    """
    An agent that wants to eat if there is food and attempts to break a block
    if there is a block.
    """
    def get_interaction(self, percept):
        food = self.get_nearest_food()
        if food != None:
            path = Pathfinding.find_path(self.world, self.agent.get_position(), food.get_position())

        return None


def create_programmable_agent(program_class, world):
    a = model.agent.ProgrammableAgent()
    program = program_class(world, a)
    a.set_program(program)
    return a
