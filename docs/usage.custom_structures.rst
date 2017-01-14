=================
Custom structures
=================
The simulated agents interact with simulated structures (:class:`model.structure.Structure`).
In the simulation, structures, just like primitive interactions, do not in themselves have a semantic meaning.
The semantics of a structure come from the interaction logic manipulating that structure.

It is possible to create custom structures, and to manipulate existing structures. 
For example, food can be created as such:

::

    class Food(Structure):
        """
        Class representing food.
        """

        color = (62, 179, 122, 255) # RGBA

        def collidable(self):
            return False

Note, again, that this structure does not in itself carry any semantics as to what "food" means.
It simply defines the structure to have a certain color, and defines the structure to be non-collidable (i.e., agents can pass through it).

By default, a structure is collidable, and has a width and a height of 1.
The collidability of a structure can be overriden as above, by implementing the :meth:`collidable <model.structure.Structure.collidable>` method.
The width and height can be set within the class definition through ``self.width`` and ``self.height``, or (even after instantiating the structure) through the :meth:`set_width <model.entity.Entity.set_width>` and :meth:`set_height <model.entity.Entity.set_height>` methods respectively.
For example:

::

    class Exp(experiment.Experiment):
        # ...
        
        def __init__(self):
            # ...
            block = model.structure.Block()
            block.set_position((1,2))
            block.set_height(2)
            # ...
