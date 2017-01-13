============
Agent vision
============
To handle agents with vision, the basic setup discussed in :doc:`creating experiments <usage.experiments>` must be changed somewhat.
Firstly, an agent no longer only enacts simple primitives (:class:`model.interaction.PrimitiveInteraction`), but can now also enact primitive interactions combined with a percept, (:class:`model.interaction.PrimitivePerceptionInteraction`).
These perception-interactions are created dynamically during the simulation.
The main code change takes place in the interaction logic.
For example, where before we defined the step logic as:

::

    def _step(world, agent, interaction):
        if world.can_step(agent):
            agent.step()
            return step
        else:
            return bump
                    
we now define it to return a perception-interaction with the agent's current perception:

::

    def _step(world, agent, interaction):
        if world.can_step(agent):
            agent.step()
            return model.interaction.PrimitivePerceptionInteraction(step, agent.get_perception(world))
        else:
            return model.interaction.PrimitivePerceptionInteraction(bump, agent.get_perception(world))
            
For :code:`agent.get_perception(world)` to be meaningful, the agent needs to have a :doc:`perception handler <model.perceptionhandler>`. As such, we need to register a perception handler to the agent:

::

    agent.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())
    
Perception handler
==================
A perception handler is an implementation (child) of the class :class:`model.perceptionhandler.PerceptionHandler`.
It has a method :meth:`perceive <model.perceptionhandler.PerceptionHandler.perceive>` taking as parameters the agent it is registered to and the current world state.
It should return some object (such as a string) indicating what the agent's current perception is.
For example, the following perception handler returns strings like "w2" to indicate the agent sees a wall at a distance of 2:

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