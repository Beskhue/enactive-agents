"""
Module to build experiments (worlds, agents, etc.).
"""

import model.interaction
import model.agent
import experiment
from elements import Elements
import pygame

class BasicExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w.............w",
        "w.wwwwwww.....w",
        "w.......wwwww.w",
        "w.wwwww.......w",
        "w.w.......w...w",
        "w.w.wwwww.w...w",
        "w.w.w...w.ww..w",
        "w.www.....w...w",
        "w.....wwwww.a.w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Rgister enact logic
        enact_logic = Elements.get_enact_logic()

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.feel)
        primitives.append(Elements.feel_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[Elements.step] = 1
        motivation[Elements.step_fail] = -10
        motivation[Elements.turn_right] = -2
        motivation[Elements.turn_left] = -2
        motivation[Elements.feel] = 0
        motivation[Elements.feel_fail] = -1
        
        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)


    def get_world(self):
        return self.world

class BasicHomeostaticExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w.............w",
        "w.wwwwwww.....w",
        "w.......wwwww.w",
        "w.wwwww.......w",
        "w.w.......w...w",
        "w.w.wwwww.w...w",
        "w.w.w...w.ww.ww",
        "w.www.....w...w",
        "w.....wwwww.h.w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicHomeostaticExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                agent.add_to_homeostatic_value("energy", -0.1)
                return Elements.step
            else:
                return Elements.step_fail

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[Elements.step.get_name()] = _step
        enact_logic[Elements.turn_right.get_name()] = Elements._turn_right
        enact_logic[Elements.turn_left.get_name()] = Elements._turn_left
        enact_logic[Elements.feel.get_name()] = Elements._feel

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.feel)
        primitives.append(Elements.feel_fail)

        # Set intrinsic homeostatic motivation values.
        motivation = {}
        motivation[Elements.step] = lambda agent: agent.get_homeostatic_value("energy") * 0.1
        motivation[Elements.step_fail] = lambda agent: -10
        motivation[Elements.turn_right] = lambda agent: -2
        motivation[Elements.turn_left] = lambda agent: -2
        motivation[Elements.feel] = lambda agent: 0
        motivation[Elements.feel_fail] = lambda agent: -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)
                if isinstance(entity, model.agent.HomeostaticConstructiveAgent):
                    entity.set_homeostatic_value("energy", 100)


    def get_world(self):
        return self.world

class BasicCoexsistenceExperiment(experiment.Experiment):
    world_representation = [
        "wwwww",
        "w..aw",
        "w.w.w",
        "w.w.w",
        "wa..w",
        "wwwww"
        ]

    def __init__(self):
        super(BasicCoexsistenceExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Register the previously defined functions.
        enact_logic = Elements.get_enact_logic()

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.feel)
        primitives.append(Elements.feel_fail)
        primitives.append(Elements.cuddle)
        primitives.append(Elements.cuddle_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[Elements.step] = 1
        motivation[Elements.step_fail] = -10
        motivation[Elements.turn_right] = -2
        motivation[Elements.turn_left] = -2
        motivation[Elements.feel] = 0
        motivation[Elements.feel_fail] = -1
        motivation[Elements.cuddle] = 50
        motivation[Elements.cuddle_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)


    def get_world(self):
        return self.world

class BasicVisionExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w....p........w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Register the previously defined functions.
        enact_logic = Elements.get_enact_logic()

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[Elements.step] = 25
        motivation[Elements.step_fail] = -10
        motivation[Elements.turn_right] = -2
        motivation[Elements.turn_left] = -2

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)


    def get_world(self):
        return self.world

class BasicVisionExperimentLoad(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w.............w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionExperimentLoad, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Load the agent. (Note: the file must exist. Create it by running 
        # the BasicVisionExperiment for some time, and then saving the agent.)
        a = self.load_agent("20161118T041955 - Agent 3T7U8G.p")
        self.world.add_entity(a)

        # Register the previously defined functions.
        enact_logic = Elements.get_enact_logic()

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)

    def get_world(self):
        return self.world

class BasicHomeostaticVisionExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwww",
        "w......w",
        "w...w..w",
        "w...w..w",
        "w...w..w",
        "w...w..w",
        "w..ww..w",
        "w..w...w",
        "w.....hw",
        "wwwwwwww",
        ]

    def __init__(self):
        super(BasicHomeostaticVisionExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                agent.add_to_homeostatic_value("energy", -0.1)
                return Elements.step
            else:
                return Elements.step_fail

        def _eat(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if isinstance(entity, model.structure.Food):
                    world.remove_entity(entity)
                    agent.add_to_homeostatic_value("energy", 10)
                    return Elements.eat
            
            return Elements.eat_fail

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[Elements.step.get_name()] = _step
        enact_logic[Elements.turn_right.get_name()] = Elements._turn_right
        enact_logic[Elements.turn_left.get_name()] = Elements._turn_left
        enact_logic[Elements.eat.get_name()] = _eat
        enact_logic[Elements.destroy.get_name()] = Elements._destroy

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.eat)
        primitives.append(Elements.eat_fail)
        primitives.append(Elements.destroy)
        primitives.append(Elements.destroy_fail)

        # Set intrinsic homeostatic motivation values.
        motivation = {}
        motivation[Elements.step] = lambda agent: agent.get_homeostatic_value("energy") * 0.1
        motivation[Elements.step_fail] = lambda agent: -10
        motivation[Elements.turn_right] = lambda agent: -2
        motivation[Elements.turn_left] = lambda agent: -2
        motivation[Elements.eat] = lambda agent: 10 - agent.get_homeostatic_value("energy") * 0.1
        motivation[Elements.eat_fail] = lambda agent: -20
        motivation[Elements.destroy] = lambda agent: 30
        motivation[Elements.destroy_fail] = lambda agent: -2

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)
                if isinstance(entity, model.agent.HomeostaticConstructiveAgent):
                    entity.set_homeostatic_value("energy", 100)
                    entity.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())


    def get_world(self):
        return self.world

    def controller(self, event, coords):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = model.structure.Food()
                food.set_position(coords)
                self.world.add_entity(food)
            elif event.key == pygame.K_b:
                block = model.structure.Block()
                block.set_position(coords)
                self.world.add_entity(block)

class BasicVisionPushExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w............pw",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionPushExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Register the previously defined functions.
        enact_logic = Elements.get_enact_logic()

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.push)
        primitives.append(Elements.push_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[Elements.step] = -1
        motivation[Elements.step_fail] = -10
        motivation[Elements.turn_right] = -2
        motivation[Elements.turn_left] = -2
        motivation[Elements.push] = 500
        motivation[Elements.push_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)


    def get_world(self):
        return self.world


class BasicVisionCoexsistenceExperiment(experiment.Experiment):
    world_representation = [
        "wwwww",
        "w..pw",
        "w.w.w",
        "w.w.w",
        "wp..w",
        "wwwww"
        ]

    def __init__(self):
        super(BasicVisionCoexsistenceExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Register the previously defined functions.
        enact_logic = Elements.get_enact_logic()

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.cuddle)
        primitives.append(Elements.cuddle_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[Elements.step] = -1
        motivation[Elements.step_fail] = -10
        motivation[Elements.turn_right] = -2
        motivation[Elements.turn_left] = -2
        motivation[Elements.cuddle] = 50
        motivation[Elements.cuddle_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)


    def get_world(self):
        return self.world

class BasicVisionCoexsistenceDestroyExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwww",
        "wp.........w",
        "wp.........w",
        "wwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionCoexsistenceDestroyExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        collaborative_destroy = model.interaction.PrimitiveInteraction("Collaborative Destroy", "Succeed")
        collaborative_destroy_fail = model.interaction.PrimitiveInteraction("Collaborative Destroy", "Fail")

        def _collaborative_destroy(world, agents_interactions):
            enacted = {}

            for agent_1, interaction_1 in agents_interactions.iteritems():
                if agent_1 in enacted:
                    continue
                else:
                    enacted[agent_1] = collaborative_destroy_fail # Set fail as default, we will now see whether it succeeded

                    entities = world.get_entities_at(agent_1.get_position())
                    for entity in entities:
                        if isinstance(entity, model.structure.Block):
                            # There is a block at agent 1's position, try to find a second agent attempting to destroy the same block:
                            for agent_2, interaction_2 in agents_interactions.iteritems():
                                if agent_1 == agent_2:
                                    continue

                                if agent_2.get_position() == agent_1.get_position():
                                    # The agents are at the same position, so the action fails
                                    continue

                                if entity in world.get_entities_at(agent_2.get_position()):
                                    # Agent 2 is enacting on the same block as agent 1, so the action succeeded
                                    world.remove_entity(entity)
                                    pos = entity.get_position()
                                    pos_2 = (pos.get_x(), pos.get_y() + 1)

                                    food_1 = model.structure.Food()
                                    food_2 = model.structure.Food()
                                    food_1.set_position(pos)
                                    food_2.set_position(pos_2)

                                    self.world.add_entity(food_1)
                                    self.world.add_entity(food_2)
                                        
                                    enacted[agent_1] = collaborative_destroy
                                    enacted[agent_2] = collaborative_destroy
            return enacted

        # Register the previously defined functions.
        enact_logic = Elements.get_enact_logic()

        self.world.add_complex_enact_logic(_collaborative_destroy, collaborative_destroy.get_name())

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(Elements.step)
        primitives.append(Elements.step_fail)
        primitives.append(Elements.turn_right)
        primitives.append(Elements.turn_left)
        primitives.append(Elements.eat)
        primitives.append(Elements.eat_fail)
        primitives.append(collaborative_destroy)
        primitives.append(collaborative_destroy_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[Elements.step] = -1
        motivation[Elements.step_fail] = -10
        motivation[Elements.turn_right] = -2
        motivation[Elements.turn_left] = -2
        motivation[Elements.eat] = 20
        motivation[Elements.eat_fail] = -2
        motivation[collaborative_destroy] = 50
        motivation[collaborative_destroy_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.add_primitives(primitives)
                entity.add_motivations(motivation)


    def get_world(self):
        return self.world

    def controller(self, event, coords):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = model.structure.Food()
                food.set_position(coords)
                self.world.add_entity(food)
            elif event.key == pygame.K_b:
                block = model.structure.Block()
                block.set_position(coords)
                block.height = 2
                self.world.add_entity(block)
