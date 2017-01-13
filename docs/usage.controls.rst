==================
Simulation control
==================
The simulation can be controlled with keyboard commands. The following commands are implemented:

================ ======================================================
Key              Command
================ ======================================================
:code:`h`        Show control help information
:code:`r`        Toggle saving the simulation frame renders to the disk
:code:`Space`    Pause the simulation
:code:`Escape`   Quit the simulation
:code:`Ctrl + s` Save the agents to file
:code:`Ctrl + w` Save the world to file
:code:`Ctrl + e` Save the experiment to file
================ ======================================================

Note: the agent :class:`model.agent.HumanAgent` takes direct user input, masking the simulation controls. To use the simulation controls in this case, hold :code:`Alt` while inputting the control command.

Experiment control
==================
To create interactive experiments, the simulation control can be extended by defining new controls in the experiment.
To do this, override the :func:`experiment.experiment.Experiment.controller` method.
For example, to make the keyboard key :code:`f` add food at the current mouse position, write:

::

    def controller(self, event, coords):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = model.structure.Food()
                food.set_position(coords)
                self.world.add_entity(food)
