"""
Module that holds classes that represent an agent's boredom handler.
"""

import abc

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
