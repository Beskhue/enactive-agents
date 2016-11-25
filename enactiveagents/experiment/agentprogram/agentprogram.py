import abc
import model.agent
import appstate
from utilities.pathfinding import Pathfinding

class AgentProgram(object):

    def __init__(self, world = None, agent = None):
        self.world = world
        self.agent = agent

    def get_nearest(self, cls):
        """
        Get the entity of a certain class that is nearest to the agent.

        :param cls: The class the entity should be of

        NOTE: Uses heuristic (Manhattan) distance.
        """
        entity_of_cls = []
        for entity in self.world.get_entities():
            if isinstance(entity, cls):
                entity_of_cls.append((self.agent.get_position().manhattan_distance_to(entity.get_position()), entity))

        entity_of_cls.sort(key = lambda tuple: tuple[0])
        if len(entity_of_cls) > 0:
            return entity_of_cls[0][1]
        else:
            return None

    def get_nearest_food(self):
        return self.get_nearest(model.structure.Food)

    def get_nearest_block(self):
        return self.get_nearest(model.structure.Block)

    def get_direction_to_position(self, position):
        """
        Get the direction (left, right, backward, straight ahead) of a position
        relative to this agent.
        
        :param position: The position to get the direction for.
        :return: "a" for ahead, "l" for left, "r" for right, "b" for behind
        """
        pos_angle = self.agent.get_position().angle_to(position)
        angle_to = round((pos_angle - self.agent.get_rotation()) % 360)

        if angle_to < 50 or angle_to > 310:
            return "a"
        elif angle_to < 140:
            return "l"
        elif angle_to < 220:
            return "b"
        else:
            return "r"

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

        # Eat if there is food in front 
        for entity in self.world.get_entities_in_front(self.agent):
            if isinstance(entity, model.structure.Food):
                return self.agent.interaction_memory.find_interaction_by_name_and_result("Eat")

        # If there is food, go to the nearest food
        to_entity = self.get_nearest_food()
        if to_entity == None:
            # Destroy a block if there is a block in front
            for entity in self.world.get_entities_in_front(self.agent):
                if isinstance(entity, model.structure.Block):
                    interaction = self.agent.interaction_memory.find_interaction_by_name_and_result("Destroy")
                    if interaction == None:
                        interaction = self.agent.interaction_memory.find_interaction_by_name_and_result("Collaborative Destroy")
                    return interaction

            # If there is a block, go to the nearest block
            to_entity = self.get_nearest_block()

        if to_entity != None:
            # Get the path to the goal entity
            path = Pathfinding.find_path(self.world, self.agent.get_position(), to_entity.get_position(), tolerance = 1)
            path = path[0]

            if len(path) == 0:
                # We do not need to step, but we need to turn
                direction = self.get_direction_to_position(to_entity.get_position())
            else:
                # We need to take a step (and potentially turn)
                step = path[0]
                direction = self.get_direction_to_position(step)

            if direction ==  "a":
                return self.agent.interaction_memory.find_interaction_by_name_and_result("Step")
            elif direction == "l":
                return self.agent.interaction_memory.find_interaction_by_name_and_result("Turn Left")
            elif direction == "r":
                return self.agent.interaction_memory.find_interaction_by_name_and_result("Turn Right")
            elif direction == "b":
                return self.agent.interaction_memory.find_interaction_by_name_and_result("Turn Left")

        # We can't do anything of use
        return self.agent.interaction_memory.find_interaction_by_name_and_result("Wait")


def create_programmable_agent(program_class, world):
    a = model.agent.ProgrammableAgent()
    program = program_class(world, a)
    a.set_program(program)
    return a
