"""
Module implementing the event manager (mediator).

See also: http://pygame.org/wiki/tut_design
"""

import pygame.event
import abc

class Event:
    """
    Class representing a game event.
    """

    def __init__(self):
        self.name = "Generic Event"

class TickEvent(Event):
    """
    Class representing a game tick event.
    
    Each tick one step of the simulation will be performed.
    """
    
    def __init__(self):
        self.name = "Tick Event"

class QuitEvent(Event):
    """
    Class representing a quit event. When this event is sent, the simulation
    should stop.
    """

    def __init__(self):
        self.name = "Quit Event"

class EventListener:
    """
    Class implementing a listener that can be notified of events.
    """
    
    @abc.abstractmethod
    def notify(self, event):
        """
        Notifies the listener of an event.
        
        :param event: The event the listener should be notified
            of.
        :type event: events.Event.
        """
        return

class EventManager:
    """
    Class implementing coordination between the model, views and 
    controllers.
    """

    def __init__(self):
        self.listeners = set()

    def register_listener(self, listener):
        """
        Register a listener with the event manager.

        :param listener: The listener to register.
        :type listener: events.Listener.
        """
        self.listeners.add(listener)

    def deregister_listener(self, listener):
        """
        Deregister a listener from the event manager.

        :param listener: The listener to deregister.
        :type listener: events.Listener.
        """
        self.listeners.remove(listener)

    def post_event(self, event):
        """
        Post an event to be sent to the listeners.

        :param event: The event to send.
        :type event: events.Event.
        """
        for listener in self.listeners:
            listener.notify(event)
