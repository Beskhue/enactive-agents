"""
Module containing some re-usable experiment elements
"""

import model

class Elements:
    step = model.interaction.PrimitiveInteraction("Step", "Succeed")
    step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
    turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
    turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
    feel = model.interaction.PrimitiveInteraction("Feel", "Succeed")
    feel_fail = model.interaction.PrimitiveInteraction("Feel", "Fail")
    cuddle = model.interaction.PrimitiveInteraction("Cuddle", "Succeed")
    cuddle_fail = model.interaction.PrimitiveInteraction("Cuddle", "Fail")
    eat = model.interaction.PrimitiveInteraction("Eat", "Succeed")
    eat_fail = model.interaction.PrimitiveInteraction("Eat", "Fail")
    push = model.interaction.PrimitiveInteraction("Push", "Succeed")
    push_fail = model.interaction.PrimitiveInteraction("Push", "Fail")
    destroy = model.interaction.PrimitiveInteraction("Destroy", "Succeed")
    destroy_fail = model.interaction.PrimitiveInteraction("Destroy", "Fail")

    @classmethod
    def get_enact_logic(cls):
        return {
            cls.step.get_name(): cls._step,
            cls.turn_right.get_name(): cls._turn_right,
            cls.turn_left.get_name(): cls._turn_left,
            cls.feel.get_name(): cls._feel,
            cls.cuddle.get_name(): cls._cuddle,
            cls.eat.get_name(): cls._eat,
            cls.push.get_name(): cls._push,
            cls.destroy.get_name(): cls._destroy
        }


    # Define environment logic for primitives, these functions will be
    # registered to the primitive interactions and will be called once
    # the agent attempts to enact the primitive interaction. 
    # The function can manipulate the world and the agents.
    # The return value is the actual enacted interaction (i.e., can be 
    # different from the attempted interaction).

    @classmethod
    def _step(cls, world, agent, interaction):
        if world.can_step(agent):
            agent.step()
            return cls.step
        else:
            return cls.step_fail

    @classmethod
    def _turn_right(cls, world, agent, interaction):
        agent.add_rotation(-90)
        return cls.turn_right
        
    @classmethod
    def _turn_left(cls, world, agent, interaction):
        agent.add_rotation(90)
        return cls.turn_left

    @classmethod
    def _feel(cls, world, agent, interaction):
        if world.can_step(agent):
            return cls.feel_fail
        else:
            return cls.feel

    @classmethod
    def _cuddle(cls, world, agent, interaction):
        entities = world.get_entities_at(agent.get_position())
        for entity in entities:
            if entity != agent and isinstance(entity, model.agent.Agent):
                return cls.cuddle
            
        return cls.cuddle_fail

    @classmethod
    def _eat(cls, world, agent, interaction):
        entities = world.get_entities_at(agent.get_position())
        for entity in entities:
            if isinstance(entity, model.structure.Food):
                world.remove_entity(entity)
                return cls.eat
            
        return cls.eat_fail

    @classmethod
    def _push(cls, world, agent, interaction):
        if world.can_step(agent):
            pos = agent.get_position()
            entities = world.get_entities_at(pos)
            for entity in entities:
                if isinstance(entity, model.structure.Block):
                    entity.position.add(agent.get_move_delta(1))
                    return Elements.push
        return cls.push_fail

    @classmethod
    def _destroy(cls, world, agent, interaction):
        entities = world.get_entities_at(agent.get_position())
        for entity in entities:
            if isinstance(entity, model.structure.Block):
                world.remove_entity(entity)
                food = model.structure.Food()
                food.set_position(entity.get_position())
                self.world.add_entity(food)
                return cls.destroy
            
        return cls.destroy_fail

