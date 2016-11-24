import abc

class AgentProgram(object):

    @abc.abstractmethod
    def get_interaction(self, world, agent, percept):
        """
        Get the interaction to enact.

        :return: The primitive interaction that the enact should enact.
        """
        raise NotImplementedError("Should be implemented by child.")

class TrivialAgentProgram(AgentProgram):

    def get_interaction(self, world, agent, percept):
        interaction_memory = agent.interaction_memory
        return interaction_memory.get_primitive_interactions()[0]
