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

    @abc.abstractmethod
    def reconstruct_from_hierarchy(self, sequence):
        """
        Reconstruct a sequence of enacted (primitive) interactions into the
        hierarchical structure represented by this interaction.

        See section 4.2 of: Georgeon, O. L., & Ritter, F. E. (2012). 
        An intrinsically-motivated schema mechanism to model and simulate 
        emergent cognition. Cognitive Systems Research, 15, 73-92.

        :param sequence: The sequence of primitive interactions to turn into a
                         composite/primitive interaction.
        :return: The composite/primitive interaction reconstructed from the 
                 sequence.
        """
        raise NotImplementedError("Should be implemented by child")

    def __ne__(self, other):
        return not self == other


class PrimitiveInteraction(Interaction):
    def __init__(self, name, result):
        super(PrimitiveInteraction, self).__init__(name)
        self.result = result
        self.hash = hash((hash(self.name), hash(self.result)))

    def get_result(self):
        """
        Get the result of the interaction this primitive represents.
        
        :return: The resut of the interaction this primitive represents.
        """
        return self.result

    def unwrap(self):
        """
        Get the primitive interaction as a singleton.
        
        :return: The primitive interaction as a singleton.
        """
        return [self]

    def reconstruct_from_hierarchy(self, sequence):
        return sequence.pop(0)

    def to_json(self):
        return {"name": self.name, "result": self.result}

    def __eq__(self, other):
        if isinstance(other, PrimitiveInteraction):
            return self.name == other.name and self.result == other.result
        else:
            return False

    def __hash__(self):
        return self.hash

    def __repr__(self):
        return "PrimitiveInteraction(name=%r, result=%r)" % (self.name, self.result)

    def __str__(self):
        return "(%s, %s)" % (self.name, self.result)

class PrimitivePerceptionInteraction(Interaction):
    """
    A primitive perception interaction is a construct containing both a
    primitive interaction and a perception.
    """
    def __init__(self, interaction, perception):
        """
        :param interaction: An interaction
        :param perception: A perception (can be any perception object returned
                           by an an agent).
        """
        self.interaction = interaction
        self.perception = perception
        self.hash = hash((hash(self.interaction), hash(self.perception)))

    def unwrap(self):
        """
        Get the primitive interaction and perception in the perception 
        interaction as a singleton.

        :return: The primitive interaction and perception in the perception 
                 interaction as a singleton.
        """
        return [self]

    def get_primitive_interaction(self):
        return self.interaction

    def get_name(self):
        return str(self.interaction) + ":" + str(self.perception)

    def reconstruct_from_hierarchy(self, sequence):
        return sequence.pop(0)

    def to_json(self):
        return {"interaction": self.interaction, "perception": self.perception}

    def __eq__(self, other):
        if isinstance(other, PrimitivePerceptionInteraction):
            return self.interaction == other.interaction and self.perception == other.perception
        else:
            return False

    def __repr__(self):
        return "PrimitivePerceptionInteraction(interaction=%r, perception=%r)" % (self.interaction, self.perception)

    def __str__(self):
        return "%s" % self.get_name()

    def __hash__(self):
        return self.hash

class CompositeInteraction(Interaction):
    def __init__(self, pre, post):
        """
        :param pre: The pre interaction
        :param post: The post interaction
        """
        super(CompositeInteraction, self).__init__("Composite")

        self.pre = pre
        self.post = post

        self.hash = hash((hash(self.pre), hash(self.post)))

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

    def reconstruct_from_hierarchy(self, sequence):
        pre = self.pre.reconstruct_from_hierarchy(sequence)
        if len(sequence) > 0:
            post = self.post.reconstruct_from_hierarchy(sequence)
            return CompositeInteraction(pre, post)
        else:
            return pre

    def to_json(self):
        return {"pre": self.pre, "post": self.post}

    def __eq__(self, other):
        if isinstance(other, CompositeInteraction):
            return self.pre == other.pre and self.post == other.post
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "CompositeInteraction(pre=%r,post=%r)" % (self.pre, self.post)

    def __str__(self):
        return "<%s, %s>" % (self.pre, self.post)

    def __hash__(self):
        return self.hash
