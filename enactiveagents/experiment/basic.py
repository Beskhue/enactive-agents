"""
Module to build experiments (worlds, agents, etc.).
"""

import model.interaction
import model.agent
import experiment

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

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left")
        feel = model.interaction.PrimitiveInteraction("Feel")
        no_feel = model.interaction.PrimitiveInteraction("No Feel")
        bump = model.interaction.PrimitiveInteraction("Bump")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different from the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return bump

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return no_feel
            else:
                return feel

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step] = _step
        enact_logic[turn_right] = _turn_right
        enact_logic[turn_left] = _turn_left
        enact_logic[feel] = _feel

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(no_feel)
        primitives.append(bump)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 1
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[feel] = 0
        motivation[no_feel] = -1
        motivation[bump] = -10

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


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

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left")
        feel = model.interaction.PrimitiveInteraction("Feel")
        no_feel = model.interaction.PrimitiveInteraction("No Feel")
        bump = model.interaction.PrimitiveInteraction("Bump")

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
                return step
            else:
                return bump

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return no_feel
            else:
                return feel

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step] = _step
        enact_logic[turn_right] = _turn_right
        enact_logic[turn_left] = _turn_left
        enact_logic[feel] = _feel

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(no_feel)
        primitives.append(bump)

        # Set intrinsic homeostatic motivation values.
        motivation = {}
        motivation[step] = lambda agent: agent.get_homeostatic_value("energy") * 0.1
        motivation[turn_right] = lambda agent: -2
        motivation[turn_left] = lambda agent: -2
        motivation[feel] = lambda agent: 0
        motivation[no_feel] = lambda agent: -1
        motivation[bump] = lambda agent: -10

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)
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

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left")
        feel = model.interaction.PrimitiveInteraction("Feel")
        no_feel = model.interaction.PrimitiveInteraction("No Feel")
        bump = model.interaction.PrimitiveInteraction("Bump")
        cuddle = model.interaction.PrimitiveInteraction("Cuddle")
        no_cuddle = model.interaction.PrimitiveInteraction("No Cuddle")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return bump

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return no_feel
            else:
                return feel

        def _cuddle(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if entity != agent and isinstance(entity, model.agent.Agent):
                    return cuddle
            
            return no_cuddle

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step] = _step
        enact_logic[turn_right] = _turn_right
        enact_logic[turn_left] = _turn_left
        enact_logic[feel] = _feel
        enact_logic[cuddle] = _cuddle

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(no_feel)
        primitives.append(bump)
        primitives.append(cuddle)
        primitives.append(no_cuddle)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 1
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[feel] = 0
        motivation[no_feel] = -1
        motivation[bump] = -10
        motivation[cuddle] = 50
        motivation[no_cuddle] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


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

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left")
        feel = model.interaction.PrimitiveInteraction("Feel")
        no_feel = model.interaction.PrimitiveInteraction("No Feel")
        bump = model.interaction.PrimitiveInteraction("Bump")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different from the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return model.interaction.PrimitivePerceptionInteraction(step, agent.get_perception(world))
            else:
                return model.interaction.PrimitivePerceptionInteraction(bump, agent.get_perception(world))

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return model.interaction.PrimitivePerceptionInteraction(turn_right, agent.get_perception(world))
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return model.interaction.PrimitivePerceptionInteraction(turn_left, agent.get_perception(world))

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return model.interaction.PrimitivePerceptionInteraction(no_feel, agent.get_perception(world))
            else:
                return model.interaction.PrimitivePerceptionInteraction(feel, agent.get_perception(world))

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step] = _step
        enact_logic[turn_right] = _turn_right
        enact_logic[turn_left] = _turn_left
        enact_logic[feel] = _feel

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(no_feel)
        primitives.append(bump)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 25
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[feel] = 0
        motivation[no_feel] = -1
        motivation[bump] = -10

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world

class BasicVisionPushExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w..b..b.....bpw",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionPushExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left")
        feel = model.interaction.PrimitiveInteraction("Feel")
        no_feel = model.interaction.PrimitiveInteraction("No Feel")
        bump = model.interaction.PrimitiveInteraction("Bump")
        push = model.interaction.PrimitiveInteraction("Push")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different from the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return model.interaction.PrimitivePerceptionInteraction(step, agent.get_perception(world))
            else:
                return model.interaction.PrimitivePerceptionInteraction(bump, agent.get_perception(world))

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return model.interaction.PrimitivePerceptionInteraction(turn_right, agent.get_perception(world))
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return model.interaction.PrimitivePerceptionInteraction(turn_left, agent.get_perception(world))

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return model.interaction.PrimitivePerceptionInteraction(no_feel, agent.get_perception(world))
            else:
                return model.interaction.PrimitivePerceptionInteraction(feel, agent.get_perception(world))

        def _push(world, agent, interaction):
            if world.can_step(agent):
                pos = agent.get_position()
                entities = world.get_entities_at(pos)
                for entity in entities:
                    if isinstance(entity, model.structure.Block):
                        entity.position.add(agent.get_move_delta(1))
                        return model.interaction.PrimitivePerceptionInteraction(push, agent.get_perception(world))
            return model.interaction.PrimitivePerceptionInteraction(bump, agent.get_perception(world))

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step] = _step
        enact_logic[turn_right] = _turn_right
        enact_logic[turn_left] = _turn_left
        enact_logic[feel] = _feel
        enact_logic[push] = _push

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(no_feel)
        primitives.append(bump)
        primitives.append(push)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = -1
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[feel] = 0
        motivation[no_feel] = -1
        motivation[bump] = -10
        motivation[push] = 500

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world