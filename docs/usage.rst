========================
Project design and usage
========================

This section explains how EnactiveAgents can be used.
It will describe in detail how the various modules can be used and adapted to specific needs.

High-level architecture
=======================
First it is useful to know the high-level design of the project. The project is split into four main packages: :doc:`model <model>`, :doc:`view <view>`, :doc:`controller <controller>`, and :doc:`experiment <experiment>`. As their names imply, the model, view, and controller packackes are designed with a `model-view-controller <https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ (MVC) pattern. In essence this simply means that the model logic is kept separate from the means of manipulating the experiment and the means of displaying the experiment to the user.

Model
-----
The model package contains modules implementing the entities available (structures, agents), the various agent components within the enactivist cognitive architecture, and additionally implements the means for agents to interact with a world. The world model implements basic world logic, such as whether two entities are at the same location.

View
----
The view package contains modules to represent the model in various ways. For example, the main view module (view.py) is used to render the model to a graphical representation on screen.

Controller
----------
The controller package contains modules implementing the ways with which a user can interact with the experiment. Currently, it only impements keyboard controls.

Experiment
----------
The experiment package contains modules to set up various experiments using the existing model. So, the *model* package implements the agents and the basic world logic, and the *experiment* package is used to set up experiments using this model. An experiment defines a world layout, defines the agents that interact in the world, and uses the basic world logic to define the interaction logic. For example, an experiment can define a "step" and "bump" interaction, and can then define whether an agent that is attempting to step successfully steps or bumps depending on whether there is a structure in front of the agent.

Usage
=====
.. toctree::

    usage.experiments
    usage.vision
    usage.controls
    usage.programmable
