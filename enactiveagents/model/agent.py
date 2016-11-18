"""
Module that holds classes that represent agents.
"""

import sys
import string
import abc
import random
import pygame
from world import Entity
import interaction
import interactionmemory
import events
from appstate import AppState
import settings

class Agent(Entity):
    """
    Class that represents an agent.
    """

    color = (3, 124, 146, 255)

    def __init__(self):
        super(Agent, self).__init__()
        self.setup_interaction_memory()
        self.name = 'Agent ' + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))

    @abc.abstractmethod
    def prepare_interaction(self):
        """
        Prepare an interaction to enact. 
        
        Interaction enaction is split into two parts to better handle multiple
        agents. First, all agents prepare the interaction to enact without
        manipulating the world state, and afterwards all these interactions
        are enacted (in randomized order). The world notifies the agent
        of which interaction was actually enacted.
        
        This ensures that an agent does not have access to world state 
        information it should not yet know at any point in time (especially 
        when it becomes more complex with e.g. a visual subsystem). If 
        preparation was immediately followed by enaction, an agent could
        potentially respond to the interaction of another agent made "earlier"
        at the same discrete point in time!

        :return: The primitive interaction that is to be enacted and optionally
                 something that will be passed to enacted_interaction of this 
                 agent.
        """
        raise NotImplementedError("Should be implemented by child.")

    @abc.abstractmethod
    def enacted_interaction(self, interaction, data):
        """
        Tell the agent which primitive interaction was actually enacted. 

        :param interaction: The primitive interaction that was actually
                            enacted.
        :param data: The data that was (optionally) returned by 
                     prepare_interaction this step.
        """ 
        raise NotImplementedError("Should be implemented by child.")

    @abc.abstractmethod
    def setup_interaction_memory(self):
        """
        Setup the interaction memory of this agent.
        """
        raise NotImplementedError("Should be implemented by child.")

    def get_perception(self, world):
        if self.has_perception_handler():
            return self.perception_handler.perceive(self, world)
        else:
            raise Exception("No perception handler has been set")

    def set_perception_handler(self, perception_handler):
        self.perception_handler = perception_handler

    def has_perception_handler(self):
        return hasattr(self, "perception_handler")

    def set_primitives(self, primitives):
        for primitive in primitives:
            self.interaction_memory.add_interaction(primitive)

    def set_motivation(self, motivation):
        for primitive, valence in motivation.iteritems():
            self.interaction_memory.set_valence(primitive, valence)

    def collidable(self):
        return False

class SimpleAgent(Agent):
    """
    An agent with a simple existence.
    """
    enacted = None

    def anticipate(self):
        """
        Anticipate the possible interactions based on the current context.
        :return: A list of possible (primitive) interactions.
        """
        interactions = []
        for composite_interaction in self.interaction_memory.get_composite_interactions():
            if composite_interaction.get_pre() == self.enacted:
                interactions.append(composite_interaction.get_post())

        return interactions

    def select_experiment(self, anticipations):
        """
        Select the best interaction from a list of anticipated interactions.

        If the list of anticipated interactions is empty or if the best 
        interaction has negative valence, return a random primitive interaction.

        :param anticipations: The list of interactions to choose an experiment
                              from.

        :return: A chosen primitive interaction.
        """
        anticipations.sort(
            key = lambda x: self.interaction_memory.get_valence(x),
            reverse = True
        )
        if len(anticipations) > 0 and self.interaction_memory.get_valence(anticipations[0]) > 0:
            return anticipations[0]
        else:
            return random.choice(self.interaction_memory.get_primitive_interactions())

    def learn_composite_interaction(self, context, enacted):
        """
        Learn a composite interaction or reinforce it if it is already known.

        :param context: The context (pre-interaction).
        :param enacted: The newly enecated interaction (post-interaction).
        """
        composite = interaction.CompositeInteraction(context, enacted)
        if composite not in self.interaction_memory.get_composite_interactions():
            self.interaction_memory.add_interaction(composite)
        else:
            self.interaction_memory.increment_weight(composite)

    def prepare_interaction(self):
        anticipations = self.anticipate()
        experiment = self.select_experiment(anticipations)

        # Post interaction preparation event
        AppState.state.get_event_manager().post_event(events.AgentPreparationEvent(
            self, 
            experiment, 
            self.interaction_memory.get_valence(experiment)))
        return experiment

    def enacted_interaction(self, interaction, data):
        # Learn interaction if it is not yet known
        if interaction not in self.interaction_memory.get_primitive_interactions():
            self.interaction_memory.add_interaction(interaction)

        # Post enacted interaction event
        AppState.state.get_event_manager().post_event(events.AgentEnactionEvent(
            self, 
            interaction, 
            self.interaction_memory.get_valence(interaction)))

        if not self.enacted == None:
            self.learn_composite_interaction(self.enacted, interaction)
        self.enacted = interaction

    def setup_interaction_memory(self):
        self.interaction_memory = interactionmemory.InteractionMemory()

class ConstructiveAgent(Agent):
    """
    An agent with a fully recursive existence. It considers all experiment as 
    abstract and processes all experiments in the same way.
    """

    def __init__(self):
        super(ConstructiveAgent, self).__init__()
        self.enacting_interaction = False
        self.enacting_interaction_step = 0
        self.enacting_interaction_sequence = []
        self.enacted_sequence = []
        self.context = []
        self.history = []

    def activate_interactions(self):
        """
        Step 1 of the sequential system.

        Known composite interactions whose pre-interaction belongs to the 
        context are activated.
        """
        activated = []
        for composite_interaction in self.interaction_memory.get_composite_interactions():
            if composite_interaction.get_pre() in self.context:
                activated.append(composite_interaction)

        return activated

    def propose_interactions(self):
        """
        Step 2 of the sequential system.

        Post-interactions of activated interactions are proposed together with
        the weight of the activation interaction (as a tuple).
        """
        activated = self.activate_interactions()

        proposed = map(lambda interaction: 
            (
                interaction.get_post(), 
                self.interaction_memory.get_weight(interaction)
            ), activated)

        return proposed

    def select_intended_interaction(self):
        """
        Step 3 of the sequential system.

        The decisional mechanism; choose an interaction to enact (primitive
        or composite).

        The intended interaction is selected from the proposed interactions
        based on the weight of the activated interactions and the values of the
        proposed post interactions.
        """
        proposed = self.propose_interactions()
        proposed.sort(
            key = lambda x: x[1] * self.interaction_memory.get_valence(x[0]), 
            reverse = True
        )
        proposed = map(lambda x: x[0], proposed)
        if len(proposed) > 0 and self.interaction_memory.get_proclivity(proposed[0]) > 0:
            return proposed[0]
        else:
            # TODO: in Katja's implementation the activated interactions contain
            # some set of default interactions. The paper itself does not seem 
            # to mention how to deal with an empty activated set.
            return random.choice(self.interaction_memory.get_primitive_interactions())

    def update_context(self, enacted_interaction, learned_or_reinforced):
        """
        Step 6 of the sequential system.

        Add all learned / reinforced interactions to the context.

        :param enacted_interaction: The interaction that was enacted (can be
                                    different from the intended interaction)
        :param learned_or_reinforced: A list of interactions that were just
                                      learned or reinforced.
        """
        self.context = []

        """
        According to paper: 

        Update the context of the agent. The new context includes the enacted
        interaction (e_d), the post-interaction of e_d if it exists, and the
        interactions that were just learned or reinforced and that pass a 
        certain weight ("stabilized" interactions).
        """
        
        for interaction_ in learned_or_reinforced:
            if self.interaction_memory.get_weight(interaction_) > 3:
                self.context.append(interaction_)

        if isinstance(enacted_interaction, interaction.CompositeInteraction):
            self.context.append(enacted_interaction.get_post())

        self.context.append(enacted_interaction)
        
        """
        Alternative context method:
        """
        """
        self.context.append(enacted_interaction)
        for interaction in learned_or_reinforced:
            self.context.append(interaction.get_pre())
        """
        

    def prepare_interaction(self):
        if not self.enacting_interaction:
            # Decisional mechanism.
            # We are not currently enacting the primitives in a sequence of
            # interactions. Choose a new interaction to enact (steps 1-3).
            self.enacting_interaction = True
            self.enacting_interaction_step = 0
            self.enacted_sequence = []

            print "%s - -----------------" % (self.name)
            # Exploration
            if random.random() <= 0.1:
                # Choose a random primitive interaction (not a primitive perception interaction)
                self.intended_interaction = random.choice(filter(lambda x: isinstance(x, interaction.PrimitiveInteraction), self.interaction_memory.get_primitive_interactions()))
                print "%s - EXPLORING" % (self.name)
            else:
                self.intended_interaction = self.select_intended_interaction()

            self.enacting_interaction_sequence = self.intended_interaction.unwrap()
            print "%s - Intending: %s" % (self.name, self.intended_interaction)

        # Enact a primitive interaction from the sequence we are currently
        # enacting.
        intended_interaction = self.enacting_interaction_sequence[self.enacting_interaction_step]
        print "%s - > %s" % (self.name, intended_interaction)

        # Step 4 of the sequential system, enact the interaction:
        # Post interaction preparation event
        AppState.state.get_event_manager().post_event(events.AgentPreparationEvent(
            self, 
            intended_interaction, 
            self.interaction_memory.get_valence(intended_interaction)))
        return (intended_interaction, intended_interaction)

    def enacted_interaction(self, interaction_, data):
        self.enacting_interaction_step += 1
        intended_primitive_interaction = data

        self.enacted_sequence.append(interaction_)

        # Learn interaction if it is not yet known
        if interaction_ not in self.interaction_memory.get_primitive_interactions():
            self.interaction_memory.add_interaction(interaction_)

        # Post enacted interaction event
        AppState.state.get_event_manager().post_event(events.AgentEnactionEvent(
            self, 
            interaction_, 
            self.interaction_memory.get_valence(interaction_)))

        if (
            not interaction_ == intended_primitive_interaction
            or
            self.enacting_interaction_step >= len(self.enacting_interaction_sequence)
            ):
            # Failed or done enacting
            self.enacting_interaction = False

            # Reconstruct enacted interaction from hierarchy of intended
            # interaction
            enacted = self.intended_interaction.reconstruct_from_hierarchy(self.enacted_sequence)
            print "%s - Enacted: %s" % (self.name, enacted)
            # Step 5: add new or reinforce existing composite interactions
            learned_or_reinforced = []
            if isinstance(enacted, interaction.CompositeInteraction):
                learned_or_reinforced.append(enacted)

            if len(self.history) >= 1:
                previous = self.history[-1]
                # <interaction at t-1, enacted interaction>
                t1enacted = interaction.CompositeInteraction(previous, enacted)
                learned_or_reinforced.append(t1enacted)

                if len(self.history) >= 2:
                    penultimate = self.history[-2]
                    # <interaction at t-2, interaction at t-1>
                    t2t1 = interaction.CompositeInteraction(penultimate, previous)

                    # <<interaction at t-2, interaction at t-1>, enacted interaction>
                    t2t1_enacted = interaction.CompositeInteraction(t2t1, enacted)
                    learned_or_reinforced.append(t2t1_enacted)

                    # <interaction at t-2, <interaction at t-1, enacted interaction>>
                    t2_t1enacted = interaction.CompositeInteraction(penultimate, t1enacted)
                    learned_or_reinforced.append(t2_t1enacted)
            for composite in learned_or_reinforced:
                if composite not in self.interaction_memory.get_composite_interactions():
                    self.interaction_memory.add_interaction(composite)
                else:
                    self.interaction_memory.increment_weight(composite)
                    
            # Keep history of last 100 actions performed
            if len(self.history) > 100:
                self.history.pop(0)
            self.history.append(enacted)

            """
            According to the paper:

            for pre_interaction in self.context:
                composite = interaction.CompositeInteraction(pre_interaction, enacted)
                learned_or_reinforced.append(composite)
                if composite not in self.interaction_memory.get_composite_interactions():
                    self.interaction_memory.add_interaction(composite)
                else:
                    self.interaction_memory.increment_weight(composite)
            """

            # Step 6: update context
            self.update_context(enacted, learned_or_reinforced)
        else: 
            # Not done
            pass

    def setup_interaction_memory(self):
        self.interaction_memory = interactionmemory.InteractionMemory()

class HomeostaticConstructiveAgent(ConstructiveAgent):
    """
    A homeostatic agent is a constructive agent where valences of interactions
    are a function of internal energy levels of the agent (these homeostatic
    values are not directly observable by the agent).
    """
    def __init__(self):
        super(HomeostaticConstructiveAgent, self).__init__()
        self.homeostasis = {}

    def set_homeostatic_value(self, homeostatic_property, value):
        self.homeostasis[homeostatic_property] = value

    def get_homeostatic_value(self, homeostatic_property):
        return self.homeostasis[homeostatic_property]

    def add_to_homeostatic_value(self, homeostatic_property, delta_value):
        self.homeostasis[homeostatic_property] += delta_value

    def setup_interaction_memory(self):
        self.interaction_memory = interactionmemory.HomeostaticInteractionMemory(self)

class HumanAgent(Agent):
    """
    An agent that is controlled by the user.
    """
    color = (146, 124, 3, 255)

    def prepare_interaction(self):
        chosen = None
        self.color_old = self.color # Temporarily change color to indicate this agent has to be controlled
        self.color = (255,255,0,255)

        # Secondary pygame loop to process events until the user made a decision
        while chosen == None:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                # If left control is pressed, use the regular controller(s)
                AppState.get_state().get_event_manager().post_event(events.ControlEvent())
            else:
                # If left control is not pressed, use this agent's controller
                interaction = self.get_interaction_from_input()
                if not interaction == None:
                    self.color = self.color_old
                    chosen = interaction

            # Draw views
            AppState.get_state().get_event_manager().post_event(events.DrawEvent())
            # Pygame tick control
            AppState.get_state().get_clock().tick(settings.MAX_FPS)

        # Post interaction preparation event
        AppState.state.get_event_manager().post_event(events.AgentPreparationEvent(
            self, 
            chosen, 
            -1))

        return chosen

    def enacted_interaction(self, interaction, data):
        # Post enacted interaction event
        AppState.state.get_event_manager().post_event(events.AgentEnactionEvent(
            self, 
            interaction, 
            -1))

    def setup_interaction_memory(self):
        self.interaction_memory = interactionmemory.InteractionMemory()

    def get_interaction_from_input(self):
        """
        Get the interaction the agent should enact from user input
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                quitEvent = events.QuitEvent()
                AppState.get_state().get_event_manager().post_event(quitEvent)
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return self.find_interaction_by_name_and_result("Step")
                elif event.key == pygame.K_LEFT:
                    return self.find_interaction_by_name_and_result("Turn Left")
                elif event.key == pygame.K_RIGHT:
                    return self.find_interaction_by_name_and_result("Turn Right")
                elif event.key == pygame.K_SLASH:
                    return self.choose_from_list()

    def find_interaction_by_name_and_result(self, name, result = "Succeed"):
        interactions = self.interaction_memory.get_primitive_interactions()

        for interaction in interactions:
            if interaction.get_name() == name and interaction.get_result() == result:
                return interaction

        return None

    def choose_from_list(self):
        """
        Method to choose interaction from a list of all interactions known by 
        this agent.
        """
        interactions = self.interaction_memory.get_primitive_interactions()

        print "Choose an interaction from the following list:"
        n = 1
        for interaction in interactions:
            print "%s. %s" % (n, interaction)
            n += 1
        
        choice = None

        keydict = {
            pygame.K_0: '0', 
            pygame.K_1: '1', 
            pygame.K_2: '2', 
            pygame.K_3: '3', 
            pygame.K_4: '4', 
            pygame.K_5: '5', 
            pygame.K_6: '6', 
            pygame.K_7: '7', 
            pygame.K_8: '8', 
            pygame.K_9: '9'
        }

        # Get user input until we have a valid choice
        while not isinstance(choice, int) or choice < 1 or choice > len(interactions):
            print "Please choose the number of an interaction and press [enter]: ",
            inputstring = ""
            while True:
                # Process pygame key events to get user input
                event = pygame.event.poll()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Stop and process the input retrieved so far
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove one character
                        if len(inputstring) > 0:
                            inputstring = inputstring[:-1] # Delete one character from the input string
                            sys.stdout.write('\b \b') # Delete one character from the console output
                    elif event.key == pygame.K_ESCAPE:
                        # Stop
                        print ""
                        return None
                    try:
                        key = keydict[event.key]
                    except:
                        key = ""
                    inputstring += key
                    sys.stdout.write(key)

            try:
                choice = int(inputstring)
            except ValueError:
                choice = None
            print ""

        return interactions[choice - 1]
        