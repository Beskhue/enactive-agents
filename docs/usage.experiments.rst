====================
Creating experiments
====================
One of the most common tasks when using EnactiveAgents is the creation of new experiments.
When creating a new experiment, you do not change the *model*.
You simply use the model to define a new simulation.

What do experiments consist of?
===============================
Most basically, an experiment consists of a world and a number of agents. In the case of enactive agents, this amounts to four main things each experiment should do:

- define the world layout;
- define the (types of) agents that are in that world;
- define the primitive interactions agents can take, and assign these interactions to the agents;
- define the agent-world interaction logic.


Defining the world
==================
To define a world, first instantiate the ``World`` class:

::
    
    world = model.world.World()
    
In the default model supplied in EnactiveAgents, worlds are rectangular. Set a width and height:

::

    world.set_width(5)
    world.set_height(6)
    
Of course, the world only becomes interesting once we add entities (e.g., structures, agents) to the world. For example, to add a wall at the top-left corner we can do the following:

::

    wall = model.structure.Wall()
    wall.set_position((0,0))
    world.add_entity(wall)
    
Adding an agent is straightforward as well:

::

    agent = model.agent.ConstructiveAgent()
    agent.set_position((2,3))
    world.add(agent)

Automatic world generation
--------------------------
Instead of defining worlds by hand, we can automate the process.
For example, the :doc:`experiment.experiment` modules defines an ``Experiment`` class with a ``parse_world`` method.
This method takes as input a list of strings, and optionally a function to map characters in the strings to objects.
To use it, we create a child of the ``Experiment`` class.
With the default mapper, the above world could be automatically parsed from the semi-graphic representation:

::

    class Exp1(experiment.Experiment):
        world_representation = [
            "w....",
            ".....",
            ".....",
            "..a..",
            ".....",
            ".....",
            ]
        
        def __init__(self):
            super(Exp1, self).__init__()
            world = self.parse_world(world_representation)
    
Or a more complex world with multiple agents:

::

    class Exp2(experiment.Experiment):

        world_representation = [
            "wwwwwwwwwwwwwww",
            "w.....a.......w",
            "w.wwwwwww.....w",
            "w.......wwwww.w",
            "w.wwwww.......w",
            "w.w....a..w...w",
            "w.w.wwwww.w...w",
            "w.w.w...w.ww..w",
            "w.www.....w...w",
            "w.....wwwww.a.w",
            "wwwwwwwwwwwwwww"
            ]
    
        def __init__(self):
            super(Exp2, self).__init__()
            world = self.parse_world(world_representation)
            
Defining agents
---------------
As we saw before, defining an agent is as simple as making a new instatiation of an agent class and adding the agent to the world:

::

    agent = model.agent.ConstructiveAgent()
    agent.set_position((2,3))
    world.add(agent)
    
However, enactive agents (such as the ``ConstructiveAgent``) require more information to be able to interact with the world.
In the enactive architecture, agents interact with the world by attempting to perform specific actions and perceive the world through those same interactions.
For example, an agent might attempt to *step*, but there is a wall in front of the agent. Instead, the agent will *bump*. As such, it attempted to interact *step*, but perceived it actually *bumped*.
The agents require a list of interactions they can interact, and a list of intrinsic motivations (e.g. agents like stepping and hate bumping).
How the interactions are set up is discussed later; we now assume these lists already exist.

We extend the code above to:

::

    agent = model.agent.ConstructiveAgent()
    agent.set_position((2,3))
    agent.set_primitives(primitives)
    agent.set_motivation(motivation)
    world.add(agent)
    
Different agents in the same world can have different possible interactions and motivations.
The agents can even be of different types (e.g. a mix of ``ConstructiveAgent`` and ``HomeostaticAgent``).

Defining primitive interactions
-------------------------------
A primitive interaction is a single discrete action an agent can take.
For example, such an action could be *step* or *bump*.
To define primitives, create instantiations of the PrimitiveInteraction class in the :doc:`model.interaction`:

::
    
    step = model.interaction.PrimitiveInteraction("Step")
    bump = model.interaction.PrimitiveInteraction("Bump")

The primitive interaction carries with it a name (here ``Step`` and ``Bump``).
However, it does not carry any semantics indicating what the primitive represents.
We need to define the interaction logic seperately.

Defining agent-world interaction logic
--------------------------------------
To define agent-world interaction logic, the semantics of primitive interactions are registered to the world.
The world keeps track of primitive interactions and their logic.

The logic associated with a primitive interaction is a function that manipulates the world, and that returns the primitive interaction the agent actually enacted.
The functions are stored in the world per agent, as a dictionary mapping primitive interactions to the interaction logic functions.
Different agents can have different logic for the same primitives.

Once an agent attempts to interact a specific primitive interaction, the world evaluates the associated function.

For example:

::
    
    class Exp(experiment.Experiment):
        def __init__(self):
            # define the world and agent(s)...
        
            # Define primitives
            step = model.interaction.PrimitiveInteraction("Step")
            bump = model.interaction.PrimitiveInteraction("Bump")
            
            # Define interaction logic for stepping
            def _step(world, agent, interaction):
                if world.can_step(agent):
                    agent.step()
                    return step
                else:
                    return bump
            
            # Associate the step primitive with the step logic
            enact_logic = {}
            enact_logic[step] = _step
            
            # Associate the logic with an agent
            world.add_enact_logic(agent, enact_logic)
        
Here, when an agent attempt to enact *step*, the function checks if the agent is able to take a step. If the agent can step, the agent steps and the function indicates *step* was enacted. Otherwise, the agent does nothing and the function indicates the agent enacted *bump*.

Defining complex agent-world interaction logic
----------------------------------------------
The world-agent interaction logic described above is useful for simple interactions concering a single agent.
However, sometimes more complex interactions are required.
To do this, complex logic is registered to the world.

Complex logic is similar to regular interaction logic described above.
Complex logic is a function, and can manipulate the world.
However, the logic is not stored per agent, and instead is used for all agents.
Additionally, where interaction logic is called to process an interaction of a single agent, complex logic processes all agents at the same time.
The complex logic evaluates the world state and the intended interactions, assigns the actual enacted interactions to the agents, and returns this to the world.
Any piece of complex logic can process and assign actual enacted interaction to none, one, some, or all of the agents in the world.
In other words, a piece of complex logic does not need to process the interactions for all agents.
Any agents with interactions that are unprocessed, will first be given to additional registered complex logic if more logic is registered, and if still left unprocessed, will be handled as per usual with simple interaction logic.
