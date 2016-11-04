"""
Module implementing a global application state.
"""

class AppState:
    """
    Class to hold the application state.
    """

    state = None

    running = True

    @staticmethod
    def get_state():
        """
        Static method to get an application state object. The first time this
        method is called, an application state object is created. Afterwards, 
        on subsequent calls that same object will be returned.

        :returns: AppState -- the application state object.
        """
        if AppState.state == None:
            AppState.state = AppState()

        return AppState.state

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager

    def get_event_manager(self):
        return self.event_manager

    def set_clock(self, clock):
        self.clock = clock

    def get_clock(self):
        return self.clock

    def set_world(self, world):
        self.world = world

    def get_world(self):
        return self.world

    def toggle_pause(self):
        self.running = not self.running

    def is_running(self):
        return self.running
