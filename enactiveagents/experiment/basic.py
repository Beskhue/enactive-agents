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
        "w.w.w...w.ww.ww",
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
        # different form the attempted interaction).
        def _step(agent, world):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return bump

        def _turn_right(agent, world):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(agent, world):
            agent.add_rotation(90)
            return turn_left

        def _feel(agent, world):
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

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 7
        motivation[turn_right] = -1
        motivation[turn_left] = -1
        motivation[feel] = 0
        motivation[no_feel] = -1
        motivation[bump] = -10

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                entity.set_enact_logic(enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world