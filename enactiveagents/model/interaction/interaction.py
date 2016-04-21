"""
Model to hold interaction classes.
"""

class Interaction:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        """
        Get the name of this interaction.
        :return: The name of this interaction.
        """
        return self.name

    def unwrap(self):
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

class CompositeInteraction(Interaction):
    def __init__(self, name, pre, post):
        """
        :param pre: The pre interaction
        :param post: The post interaction
        """
        super(CompositeInteraction, self).__init__(name)

        self.pre = pre
        self.post = post

    def unwrap(self):
        """
        Unwrap the composite interaction.
        :return: A list of primitive interactions.
        """
        return self.pre.unwrap() + self.post.unwrap()
