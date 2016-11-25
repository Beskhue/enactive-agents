"""
Module that holds classes that represent an agent's memory of interactions.
"""

import interaction
import model.boredomhandler

class InteractionMemory(object):
    """
    Class to represent the interaction memory of an agent.
    """
    def __init__(self, boredom_handler = model.boredomhandler.WeightBoredomHandler):
        self.primitive_interactions = []
        self.composite_interactions = []
        self.valences = {}
        self.weights = {}
        self.alternative_interactions = {}
        self.weight_sum = 0
        self.boredom_handler = boredom_handler()

    def add_interaction(self, interaction_, weight=1, valence=0):
        """
        Add an interaction to the interaction memory.

        :param interaction_: The interaction to add.
        :param weight: The weight of the interaction.
        :param valence: The valence of the interaction, only used for primitive
                        interactions.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction) or isinstance(interaction_, interaction.PrimitivePerceptionInteraction):
            self.primitive_interactions.append(interaction_)
            self.valences[interaction_] = valence
        elif isinstance(interaction_, interaction.CompositeInteraction):
            self.composite_interactions.append(interaction_)
        else:
            raise TypeError("Expected interaction_ to be either primitive, primitive perception, or composite.")

        self.weights[interaction_] = weight
        self.weight_sum += weight

    def add_alternative_interaction(self, interaction_, alternative_interaction):
        """
        Add an alternative interaction to an interaction in the interaction memory.

        :param interaction_: The interaction to add an alternative to.
        :param alternative_interaction: The alternative interaction to add to the interaction.
        :return: True if the alternative was added, false if it was already registered to the interaction
        """

        # Create alternative interaction list for this interaction if it does not yet exist
        if interaction_ not in self.alternative_interactions:
            self.alternative_interactions[interaction_] = []

        # Add the alternative interaction to the list of alternatives for this interaction
        # if it is not yet in the list of alternatives for this interaction
        if alternative_interaction not in self.alternative_interactions[interaction_]:
            self.alternative_interactions[interaction_].append(alternative_interaction)
            return True
        else:
            return False

    def get_alternative_interactions(self, interaction_):
        """
        Get the alternative interactions for an interaction.

        :param interaction_: The interaction to get the alternatives for.
        :return: A list of alternative interactions registered to an interaction.
        """
        if interaction_ not in self.alternative_interactions:
            return []
        else:
            return self.alternative_interactions[interaction_]

    def increment_weight(self, interaction):
        """
        Increment the weight of an interaction.

        :param interaction: The interaction to increment the weight of.
        """
        self.weights[interaction] += 1
        self.weight_sum += 1

    def set_weight(self, interaction, weight):
        """
        Set the weight of an interaction to a specific value.

        :param interaction: The interaction to set the weight of.
        :param weight: The value to set the interaction's weight to.
        """
        self.weight_sum = self.weight_sum - self.weights[interaction] + weight
        self.weights[interaction] = weight

    def get_weight(self, interaction):
        """
        Get the weight of an interaction.

        :param interaction: The interaction to get the weight of.
        """
        if interaction in self.weights:
            return self.weights[interaction]
        else:
            return 0

    def get_total_weight(self):
        """
        Get the sum of weights of all known interactions.

        :return: The sum of weights of all known interactions.
        """
        return self.weight_sum

    def set_valence(self, interaction_, valence):
        """
        Set the valence of an interaction to a specific value.

        :param interaction_: The interaction to set the valence of.
        :param valence: The value to set the interaction's valence to.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            self.valences[interaction_] = valence
        else:
            raise TypeError("Expected interaction to be primitive.")

    def get_valence(self, interaction_, process_boredom = True):
        """
        Get the valence of an interaction. If the interaction is a primative,
        get its valence. If the interaction is composite, sum the valences
        of its primitives.

        :param interaction_: The interaction to get the valence of.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            valence = self.valences[interaction_]
        elif isinstance(interaction_, interaction.PrimitivePerceptionInteraction):
            valence =  self.valences[interaction_.get_primitive_interaction()]
        elif isinstance(interaction_, interaction.CompositeInteraction):
            primitives = interaction_.unwrap()
            valence = reduce(lambda x, y: x + self.get_valence(y, process_boredom = False), primitives, 0)
        else:
            raise TypeError("Expected interaction_ to be either primitive or composite.")

        if process_boredom:
            return self.boredom_handler.process_boredom(self, interaction_, valence)
        else:
            return valence

    def get_proclivity(self, interaction):
        """
        Get the proclivity of an interaction. Proclivity is defined as the 
        valence multiplied by the weight.

        :param interaction: The interaction to get the proclivity of.
        """
        return self.get_weight(interaction) * self.get_valence(interaction)

    def get_primitive_interactions(self):
        return self.primitive_interactions

    def get_composite_interactions(self):
        return self.composite_interactions

    def get_all_interactions(self):
        return self.primitive_interactions + self.composite_interactions

    def find_interaction_by_name_and_result(self, name, result = "Succeed"):
        interactions = self.get_primitive_interactions()

        for interaction_ in interactions:
            if interaction_.get_name() == name and interaction_.get_result() == result:
                return interaction_

        return None

class HomeostaticInteractionMemory(InteractionMemory):
    """
    A homeostatic interaction's valence is a function of the agent's internal
    energy level. Thus, this interaction memory keeps track of the agent to be
    able to compute the valence.
    """
    def __init__(self, agent):
        super(HomeostaticInteractionMemory, self).__init__()
        self.agent = agent

    def get_valence(self, interaction_):
        """
        Get the valence of an interaction. If the interaction is a primative,
        get its valence. If the interaction is composite, sum the valences
        of its primitives. 

        The valences are functions of the agent's internal energy levels.

        :param interaction_: The interaction to get the valence of.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            return self.valences[interaction_](self.agent)
        elif isinstance(interaction_, interaction.PrimitivePerceptionInteraction):
            return self.valences[interaction_.get_primitive_interaction()](self.agent)
        elif isinstance(interaction_, interaction.CompositeInteraction):
            primitives = interaction_.unwrap()
            valence = reduce(lambda x, y: x + self.get_valence(y), primitives, 0)
            return valence
        else:
            raise TypeError("Expected interaction_ to be either primitive or composite.")