"""
Prints a history of agent events to file.
"""

import events
import json

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
            if str(event.agent) not in self.preparation_history:
                self.preparation_history[str(event.agent)] = []

            self.preparation_history[str(event.agent)].append(str(event.action))

            if len(self.preparation_history) > 20:
                self.preparation_history.pop(0)
        elif isinstance(event, events.AgentEnactionEvent):
            if str(event.agent) not in self.enaction_history:
                self.enaction_history[str(event.agent)] = []

            self.enaction_history[str(event.agent)].append(str(event.action))

            if len(self.enaction_history) > 20:
                self.enaction_history.pop(0)
        elif isinstance(event, events.TickEvent):
            self.write_to_file()

    def write_to_file(self):
        """
        Write the history to the traces file.
        """

        d = dict()
        d["preparation_history"] = self.preparation_history
        d["enaction_history"] = self.enaction_history
        with open(self.file_path,'w+') as f:
            json.dump(d, f)