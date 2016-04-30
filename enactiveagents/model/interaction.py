"""
Module to hold interaction classes.
"""

import abc

class Interaction(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        """
        Get the name of this interaction.
        :return: The name of this interaction.
        :rtype: basestring
        """
        return self.name

    @abc.abstractmethod
    def unwrap(self):
        """
        Get the sequence of interactions represented by this interaction.
        :return: The sequence of interactions represented by this itneraction.
        """
        raise NotImplementedError("Should be implemented by child")

class PrimitiveInteraction(Interaction):
    def __init__(self, name):
        super(PrimitiveInteraction, self).__init__(name)

    def unwrap(self):
        """
        Get the primitive interaction as a singleton.
        :return: The primitive interaction as a singleton.
        """
        return [self]

    def __repr__(self):
        return "PrimitiveInteraction(name=%r)" % self.name

class CompositeInteraction(Interaction):
    def __init__(self, pre, post):
        """
        :param pre: The pre interaction
        :param post: The post interaction
        """
        super(CompositeInteraction, self).__init__("Composite")

        self.pre = pre
        self.post = post

    def get_pre(self):
        return self.pre

    def get_post(self):
        return self.post

    def unwrap(self):
        """
        Unwrap the composite interaction.
        :return: A list of primitive interactions.
        """
        return self.pre.unwrap() + self.post.unwrap()

    def __eq__(self, other):
        self.unwrap() == other.unwrap()

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "CompositeInteraction(pre=%r,post=%r)" % (self.pre, self.post)
