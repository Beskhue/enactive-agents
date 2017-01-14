.. EnactiveAgents documentation master file, created by
   sphinx-quickstart on Fri Apr 22 02:14:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. title:: EnactiveAgents, an ECA in Python
   
============================
EnactiveAgents documentation
============================

EnactiveAgents is an implementation of the Enactivist Cognitive Architecture in Python. See *Georgeon, O. L., Marshall, J. B., & Manzotti, R. (2013). ECA: An enactivist cognitive architecture based on sensorimotor modeling. Biologically Inspired Cognitive Architectures, 6, 46-57* for a thorough description of the architecture.
   
The implementation is set up to be *scriptable*, *adaptable* and *pluggable*:
   
- Scriptable: experiments can easily be set up. The architecture and specific experiment logic are decoupled.
- Adaptable: the architecture is implemented with the model-view-controller design pattern, and is highly object oriented. This makes adding or modifying functionality straightforward.
- Pluggable: the implementation makes as few assumptions as possible about data formats, e.g. different types of agents can be interchanged.

For the source code documentation head to the :doc:`source code documentation <modules>` page.

Guide
=====
.. toctree::
   :maxdepth: 1

   Home <self>
   Modules <modules>
   overview
   quickstart
   usage
   faq
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

