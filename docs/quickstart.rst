==========
Quickstart
==========

This page provides a quick introduction to EnactiveAgents.
For instructions on installing EnactiveAgents, head to the :ref:`installation` page.

Running EnactiveAgents
======================

To run EnactiveAgents, do:

.. code-block:: bash

    python enactiveagents/enactiveagents.py

This starts the simulation. The simulation can be :doc:`controlled <usage.controls>`. The simulation is divided into discrete *ticks*. Each tick, the following two steps are performed sequentially:

#. Let all agents *prepare* their next primitive interaction with the current state of the world.
#. One by one, in randomized order, let the agents attempt to *enact* the prepared primitive interaction.

This subdivision of preparation and enaction is present to ensure all agents have the same information available within a single tick. Note that an interaction of an agent might change the world state, which might have ramifications for the interactions of the subsequent agents within that tick.

To change the simulation, open :code:`enactiveagents.py` and modify the following line:

.. code-block:: python

    experiment_ = experiment.basic.BasicVisionExperiment()
    
The :code:`experiment_` variable should be an object of type :class:`experiment.experiment.Experiment`. Built-in experiments can be found in :code:`experiment/basic.py` (:doc:`experiment.basic`).

An experiment can have various controls assigned to it (:meth:`experiment.experiment.Experiment.controller`). For example, an experiment might allow you to place an object for the agents to interact with.