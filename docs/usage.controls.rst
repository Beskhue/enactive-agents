==================
Simulation control
==================
The simulation can be controlled with keyboard commands. The following commands are implemented:

======= ====================
Key     Command
======= ====================
Space   Pause the simulation
Escape  Quit the simulation
======= ====================

Experiment control
==================
To create interactive experiments, the simulation control can be extended by defining new controls in the experiment.
To do this, override the :func:`experiment.experiment.Experiment.controller` method.
For example, to make the keyboard key `f` add food at the current mouse position, write:

::

    def controller(self, event, coords):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = model.structure.Food()
                food.set_position(coords)
                self.world.add_entity(food)
