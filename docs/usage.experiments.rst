====================
Creating experiments
====================
One of the most common tasks when using EnactiveAgents is the creation of new experiments.
When creating a new experiment, you do not change the *model*.
You simply use the model to define a new simulation.

What do experiments consist of?
===============================
In the most basic sense, an experiment consists of a world and a number of agents. In the case of enactive agents, this amounts to four main things each experiment should do:

- define the world layout;
- define the (types of) agents that are in that world;
- define the primitive interactions agents can take, and assign these interactions to the agents;
- define the agent-world interaction logic.

Additionally, experiments can:

- define functions to mutate the world state at each tick for automated experimentation;
- define when a simulation should automatically stop;
- define a function to calculate metrics.

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
For example, the :doc:`experiment.experiment` modules defines an :class:`Experiment <experiment.experiment.Experiment>` class with a :meth:`parse_world <experiment.experiment.Experiment.parse_world>` method.
This method takes as input a list of strings, and optionally a function to map characters in the strings to entities.
To use it, we create a child of the :class:`Experiment <experiment.experiment.Experiment>` class.
With the default :meth:`mapper <experiment.experiment.Experiment.mapper>`, the above world could be automatically parsed from the textual representation:

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
    
However, enactive agents (such as the :class:`model.agent.ConstructiveAgent`) require more information to be able to interact with the world.
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
The agents can even be of different types (e.g. a mix of :class:`ConstructiveAgent <model.agent.ConstructiveAgent>` and :class:`HomeostaticConstructiveAgent <model.agent.HomeostaticConstructiveAgent>`).

Defining primitive interactions
-------------------------------
A primitive interaction is a single discrete action an agent can take.
For example, such an action could be *step* or *bump*.
To define primitives, create instantiations of the PrimitiveInteraction class in the :doc:`model.interaction`:

::
    
    step = model.interaction.PrimitiveInteraction("Step", "Succeed")
    step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")

The primitive interaction carries with it a name (here ``Step``) and a result (here ``Succeed`` and ``Fail``).
However, it does not carry any semantics indicating what the primitive represents.
We need to define the interaction logic seperately.

Defining agent-world interaction logic
--------------------------------------
To define agent-world interaction logic, the semantics of primitive interactions are registered to the world.
The world keeps track of primitive interactions and their logic.

The logic associated with a primitive interaction is a function that manipulates the world, and that returns the primitive interaction the agent actually enacted.
The functions are stored per agent in the world as a dictionary that maps primitive interactions to the interaction logic functions.
The interaction logic functions manipulate the world.
Because the functions are stored per agent, different agents can have different logic for the same primitives.

Once an agent attempts to interact a specific primitive interaction, the world evaluates the associated function.

For example:

::
    
    class Exp(experiment.Experiment):
        def __init__(self):
            # Define the world and agent(s)
            # ...
            
            # Define primitives
            step = model.interaction.PrimitiveInteraction("Step", "Succeed")
            step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
            
            # Define interaction logic for stepping
            def _step(world, agent, interaction):
                if world.can_step(agent):
                    agent.step()
                    return step
                else:
                    return step_fail
            
            # Associate the step primitive with the step logic
            enact_logic = {}
            enact_logic[step.get_name()] = _step
            
            # Associate the logic with an agent
            world.add_enact_logic(agent, enact_logic)
            
            # Set primitives known/enactable by the agents.
            primitives = []
            primitives.append(step)
            primitives.append(step_fail)
            
            # Set intrinsic motivation values.
            motivation = {}
            motivation[step] = 1
            motivation[step_fail] = -10
            
            # Add the primitives and motivation to the agent
            agent.add_primitives(primitives)
            agent.add_motivations(motivation)
            
            
        
Here, when an agent attempts to enact the action *step*, the function checks if the agent is able to take a step. If the agent can step, the agent steps and the function indicates *step* was enacted and succeeded. Otherwise, the agent does nothing and the function indicates the action failed.

Reusable agent-world interaction logic
______________________________________

Many basic primitive interactions and their logic are reusable and are pre-defined in the :class:`Elements <model.experiment.elements.Elements>` class.
The code in the section above, now including many more interactions, would become:

::

    class Exp(experiment.Experiment):
        def __init__(self):
            # Define the world and agent(s)
            # ...
            
            # Get the pre-defined enact logic mapping
            enact_logic = Elements.get_enact_logic()
            
            # Associate the logic with an agent
            world.add_enact_logic(agent, enact_logic)
            
            # Set primitives known/enactable by the agents.
            primitives = []
            primitives.append(Elements.step)
            primitives.append(Elements.step_fail)
            primitives.append(Elements.turn_right)
            primitives.append(Elements.turn_left)
            primitives.append(Elements.wait)
            primitives.append(Elements.feel)
            primitives.append(Elements.feel_fail)
            
            # Set intrinsic motivation values.
            motivation = {}
            motivation[Elements.step] = 1
            motivation[Elements.step_fail] = -10
            motivation[Elements.turn_right] = -2
            motivation[Elements.turn_left] = -2
            motivation[Elements.wait] = -1
            motivation[Elements.feel] = 0
            motivation[Elements.feel_fail] = -1
            
            # Add the primitives and motivation to the agent
            agent.add_primitives(primitives)
            agent.add_motivations(motivation)

Note that you do not need to add all interactions defined in :class:`Elements <model.experiment.elements.Elements>` to the agent.
You only need to add the desired interactions to the agent.
            
Defining complex agent-world interaction logic
----------------------------------------------
The world-agent interaction logic described above is useful for simple interactions concering a single agent.
However, sometimes more complex interactions are required.
For example, it might be necessary to base the result of an interaction on the intended interactions of multiple agents (e.g., collaborative interactions).
To do this, complex logic is registered to the world.

Complex logic is similar to regular interaction logic described above.
Complex logic is a function, and can manipulate the world.
However, the logic is not stored per agent, and instead is used for all agents.
Additionally, where interaction logic is called to process an interaction of a single agent, complex logic processes all agents at the same time.
The complex logic evaluates the world state and the intended interactions, assigns the actual enacted interactions to the agents, and returns this to the world.
Any piece of complex logic can process and assign actual enacted interaction to none, one, some, or all of the agents in the world.
In other words, a piece of complex logic does not need to process the interactions for all agents.
Any agents with interactions that are unprocessed, will first be given to additional registered complex logic if more logic is registered, and if still left unprocessed, will be handled as per usual with simple interaction logic.

An example piece of complex logic is shown below. Here, two agents can destroy a block. They must both be facing the same block, and they must both intend to enact ``collaborative_destroy``. Only if this is true, the block is destroyed, and two pieces of food are spawned.

::
    
    class Exp(experiment.Experiment):
        def __init__(self):
            # Define the world and agent(s)
            # ...
            
            # Define primitives
            collaborative_destroy = model.interaction.PrimitiveInteraction("Collaborative Destroy", "Succeed")
            collaborative_destroy_fail = model.interaction.PrimitiveInteraction("Collaborative Destroy", "Fail")
            
            # Define interaction logic for collaboratively destroying
            def _collaborative_destroy(world, agents_interactions):
                enacted = {}

                for agent_1, interaction_1 in agents_interactions.iteritems():
                    if agent_1 in enacted:
                        continue
                    else:
                        enacted[agent_1] = collaborative_destroy_fail # Set fail as default, we will now see whether it succeeded

                        entities = world.get_entities_in_front(agent_1)
                        for entity in entities:
                            if isinstance(entity, model.structure.Block):
                                # There is a block at agent 1's position, try to find a second agent attempting to destroy the same block:
                                for agent_2, interaction_2 in agents_interactions.iteritems():
                                    if agent_1 == agent_2:
                                        continue

                                    if agent_2.get_position() == agent_1.get_position():
                                        # The agents are at the same position, so the action fails
                                        continue

                                    if entity in world.get_entities_in_front(agent_2):
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
            
            # Register the basic encation logic.
            enact_logic = Elements.get_enact_logic()

            # Register the complex enaction logic just defined.
            self.world.add_complex_enact_logic(_collaborative_destroy, collaborative_destroy.get_name())

            # Set primitives known/enactable by the agents.
            primitives = []
            primitives.append(Elements.step)
            primitives.append(Elements.step_fail)
            primitives.append(Elements.turn_right)
            primitives.append(Elements.turn_left)
            primitives.append(Elements.wait)
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
            motivation[Elements.wait] = -1
            motivation[Elements.eat] = 20
            motivation[Elements.eat_fail] = -2
            motivation[collaborative_destroy] = 50
            motivation[collaborative_destroy_fail] = -1

            # Add the logic to all agents present in the world.
            for entity in self.world.get_entities():
                if isinstance(entity, model.agent.Agent):
                    self.world.add_enact_logic(entity, enact_logic)
                    entity.add_primitives(primitives)
                    entity.add_motivations(motivation)

Automated experimentation
=========================
Experiments can define functions to alter the world state.
These functions are automatically called during the simulation with the world parameter and the world time in ticks.
This functionality is meant to enable automating experiments.

For example, an experiment can be defined where food is automatically added to the world if there is no food present.
The food is only to be placed at a "free position," i.e. a position where no other entity (wall, agent) is located.

::

    import random

    class Exp(experiment.Experiment):

        def __init__(self):
            # Define the world and agent(s)
            # ...

            def add_food(world, t):
                if len(world.get_entities_of_type(model.structure.Food)) == 0:
                    # Add food
                    positions = world.get_free_positions()
                    p = random.choice(positions)

                    food = model.structure.Food()
                    food.set_position(p)
                    world.add_entity(food)

            self.world.add_mutate_callback(add_food)

Note that multiple such mutate functions can be added to a single world.
