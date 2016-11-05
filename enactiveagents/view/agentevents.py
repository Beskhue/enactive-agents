"""
Prints a history of agent events to file.
"""

import events
import json

class AgentEvents(events.EventListener):
    """
    View class
    """

    def __init__(self):
        self.history = {}

    def create_if_not_exists(self, agent):
        if str(agent) not in self.history:
            self.history[str(agent)] = {"preparation": [], "enaction": []}

    def notify(self, event):
        if isinstance(event, events.AgentPreparationEvent):
            self.create_if_not_exists(event.agent)

            self.history[str(event.agent)]["preparation"].append((str(event.action), event.valence))

            if len(self.history[str(event.agent)]["preparation"]) > 20:
                self.history[str(event.agent)]["preparation"].pop(0)
        elif isinstance(event, events.AgentEnactionEvent):
            self.create_if_not_exists(event.agent)

            self.history[str(event.agent)]["enaction"].append((str(event.action), event.valence))

            if len(self.history[str(event.agent)]["enaction"]) > 20:
                self.history[str(event.agent)]["enaction"].pop(0)

    def write(self, fp):
        """
        Writes the view as json to a stream.
        :param fp: a write()-supporting file-like object
        """
        return json.dump(self.history, fp)
