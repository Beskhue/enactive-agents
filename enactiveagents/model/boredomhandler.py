"""
Module that holds classes that represent an agent's boredom handler.
"""

import abc
import model.interaction

class BoredomHandler(object):
    """
    Abstract boredom handler class.
    """

    @abc.abstractmethod
    def process_boredom(self, interaction_memory, interaction, unmodified_valence):
        """
        Modifies the valence of an interaction such that boredom is handled.

        :param interaction_memory: The interaction memory
        :param interaction: The interaction to process boredom for
        :param unmodified_valence: The unmodified (raw) valence of the interaction
        :return: The modified valence taking boredom into account
        """
        raise NotImplementedError("Should be implemented by child")


class PassthroughBoredomHandler(BoredomHandler):
    """
    A boredom handler not implementing any boredom measures.
    """
    def process_boredom(self, interaction_memory, interaction, unmodified_valence):
        return unmodified_valence

class WeightBoredomHandler(BoredomHandler):
    """
    A boredom handler taking into account the weight of interactions. The sum
    of the hierarchical weight of an interaction is calculated, and its
    contribution to the total weight is calculated. This is used to discount
    interactions that have a high contribution.
    """

    def interaction_total_weight(self, interaction_memory, interaction):
        """
        Get the total (hierarchical) weight of an interaction. This takes the
        sum of all weights of all interactions inside the hierarchy of this
        interaction. E.g., for a composite interaction <i1, i2> the sum is
        weight(<i1, i2>) = <i1, i2>.weight + weight(i1) + weight(i2).

        :param interaction_memory: The interaction memory
        :param interaction: The interaction to get the hierarchical weight for
        :return: The hierarchical weight of the interaction
        """
        if isinstance(interaction, model.interaction.CompositeInteraction):
            return (
                interaction_memory.get_weight(interaction) 
                + self.interaction_total_weight(interaction_memory, interaction.get_pre()) 
                + self.interaction_total_weight(interaction_memory, interaction.get_post())
            )
        else:
            return interaction_memory.get_weight(interaction)
    
    def process_boredom(self, interaction_memory, interaction, unmodified_valence):
        if unmodified_valence > 0:
            sum = interaction_memory.get_total_weight()
            weight = self.interaction_total_weight(interaction_memory, interaction)
            modifier = (1 - float(weight)/float(sum))
            return unmodified_valence * modifier
        else:
            return unmodified_valence
