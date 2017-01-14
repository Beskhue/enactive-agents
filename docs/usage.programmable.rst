===================
Programmable agents
===================
To facilitate experimentation, EnactiveAgents features programmable agents (:class:`model.agent.ProgrammableAgent`).
These agents are supplied with an :class:`AgentProgram <experiment.agentprogram.agentprogram.AgentProgram>` to tell the agent what to do at each tick.
The programmable agents are treated in exactly the same way as regular agents.
This means that their interaction logic is evaluated in exactly the same way as regular agents.
For example, their interactions can fail.

In the simplest terms, an agent program is an object of type :class:`AgentProgram <experiment.agentprogram.agentprogram.AgentProgram>` that has a method :meth:`get_interaction <experiment.agentprogram.agentprogram.AgentProgram.get_interaction>` which returns the primitive interaction the agent wants to enact.
Below is a trivial agent program that simply enacts the first interaction known by the agent.

::

    class TrivialAgentProgram(AgentProgram):
        """
        A trivial agent program that simply attempts to perform the first primitive
        known by the agent.
        """
        def get_interaction(self, percept):
            interaction_memory = self.agent.interaction_memory
            return interaction_memory.get_primitive_interactions()[0]
            
We can add a programmable agent with this agent program to a world:

::

    class Exp(experiment.Experiment):
        # ...
        
        def __init__(self):
            # ...
            # Add programmed agent
            a = agentprogram.agentprogram.create_programmable_agent(agentprogram.agentprogram.TrivialAgentProgram, self.world)
            a.set_position((1,2))
            self.world.add_entity(a)
            # ...

The agent program object has access to the agent and world through ``self.agent`` and ``self.world`` respectively.
These objects should only be used for perceiving the agent and world states, and not for direct manipulation.
The abstract class :class:`AgentProgram <experiment.agentprogram.agentprogram.AgentProgram>` contains methods to facilitate the creation of agent programs, such as :meth:`get_nearest_food <experiment.agentprogram.agentprogram.AgentProgram.get_nearest_food>`.
