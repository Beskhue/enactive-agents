============
Agent vision
============
To handle agents with vision, the basic setup discussed in :doc:`creating experiments <usage.experiments>` must be changed somewhat.
Firstly, an agent no longer enact only primitives, ``model.interaction.PrimitiveInteraction``, but can also enact primitive interactions combined with a percept, ``model.interaction.PrimitivePerceptionInteraction``.
These perception interactions are created dynamically during the simulation.
The main setup change takes place in the in the interaction logic.
Where before we defined the step logic as:

::

    def _step(world, agent, interaction):
        if world.can_step(agent):
            agent.step()
            return step
        else:
            return bump
                    
we now define it as:

::

    def _step(world, agent, interaction):
        if world.can_step(agent):
            agent.step()
            return model.interaction.PrimitivePerceptionInteraction(step, agent.get_perception(world))
        else:
            return model.interaction.PrimitivePerceptionInteraction(bump, agent.get_perception(world))
            
Additionally, we need to register a :doc:`perception handler <model.perceptionhandler>` to the agent:

::

    agent.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())
    
Perception handler
==================
A perception handler is an implementation (child) of the class ``PerceptionHandler``.
It has a method ``perceive`` taking as parameters the agent it is registered to and the current world state.
It should return some object (such as a string) indicating what the agent's current perception is.
For example, the following perception handler returns strings such as "w2" to indicate the agent can see a wall at a distance of 2:

::

    class BasicPerceptionHandler(PerceptionHandler):
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

            return ""
            
Note that the perception handler can return complex objects (such as instantiations of classes).
When returning complex objects, be sure that these can be compared for equality. Equal perceptions should return objects that are evaluated to be equal, e.g. by implementing the ``__eq__`` method.