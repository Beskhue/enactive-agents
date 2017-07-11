===================
Running simulations
===================
Experiments are run through the :doc:`enactiveagents`.
To change which experiment are to be run, change the :func:`enactiveagents.main` method.

For example, to run :class:`experiment.basic.BasicHomeostaticExperiment`, and subsequently :class:`experiment.basic.BasicVisionExperiment`, one can write this:

::

    def main():
        """
        Main function of the application.
        """

        experiments = []
        experiments.append(experiment.basic.BasicHomeostaticExperiment())
        experiments.append(experiment.basic.BasicVisionExperiment())

        for experiment_ in experiments:
            run_experiment(experiment_, render = True, interactive = True, console_output = True, save_logs = True)

When running an experiment, output can be controlled. For example, rendering and interactive control can be disabled. See :func:`enactiveagents.run_experiment` for more information.