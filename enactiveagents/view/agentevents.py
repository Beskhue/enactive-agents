"""
Prints a history of agent events to file.
"""

import events

class AgentEvents(events.EventListener):
    """
    View class
    """

    def __init__(self, file_path):
        """
        :param file_path: The path of the file to output the history to.
        """
        self.file_path = file_path
        self.preparation_history = dict()
        self.enaction_history = dict()

    def notify(self, event):
        if isinstance(event, events.AgentPreparationEvent):
            if event.agent not in self.preparation_history:
                self.preparation_history[event.agent] = []

            self.preparation_history[event.agent].append(event.action)
        elif isinstance(event, events.AgentEnactionEvent):
            if event.agent not in self.enaction_history:
                self.enaction_history[event.agent] = []

            self.enaction_history[event.agent].append(event.action)
        elif isinstance(event, events.TickEvent):
            pass