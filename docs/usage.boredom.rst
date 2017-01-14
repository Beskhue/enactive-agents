=============
Agent boredom
=============
Agents repeatedly performing the same interaction might become bored.
This can be modeled through using a boredom handler (:class:`model.boredomhandler.BoredomHandler`).
A boredom handler is an object of type :class:`BoredomHandler <model.boredomhandler.BoredomHandler>`, implementing the :meth:`process_boredom <model.boredomhandler.BoredomHandler.process_boredom>` method.

The boredom handler is attached to the interaction memory of an agent (:class:`model.interactionmemory.InteractionMemory`) and the :meth:`process_boredom <model.boredomhandler.BoredomHandler.process_boredom>` method receives as input the interaction memory, the (potentially composite) interaction that is to be evaluated, and the valence (pre-boredom) of the interaction.
The result of the :meth:`process_boredom <model.boredomhandler.BoredomHandler.process_boredom>` method should be the valence taking boredom into account.

A trivial boredom handler not taking any form of boredom into account is:

::

    class PassthroughBoredomHandler(BoredomHandler):
        """
        A boredom handler not implementing any boredom measures.
        """
        def process_boredom(self, interaction_memory, interaction, unmodified_valence):
            return unmodified_valence
            
This handler can be attached to an agent by writing:

::
    
    class Exp(experiment.Experiment):
        # ...
        
        def __init__(self):
            # ...
            agent = # ... (initialize agent)
            agent.set_interaction_memory(interactionmemory.InteractionMemory(
                boredom_handler = model.boredomhandler.PassthroughBoredomHandler
            ))
            # ... add interactions to the agent
            self.world.add_entity(agent)
            # ...
            
The default boredom handler is set in the initialization method of :class:`model.interactionmemory.InteractionMemory`.
