import abc
import model.agent
import appstate

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

def create_programmable_agent(program_class, world):
    a = model.agent.ProgrammableAgent()
    program = program_class(world, a)
    a.set_program(program)
    return a