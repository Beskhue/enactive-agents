"""
Module implementing a global application state.
"""

import logging

class AppState:
    """
    Class to hold the application state.
    """

    state = None

    running = True
    save_simulation_renders = False
    t = 0

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

    def reset(self):
        self.state = None

        self.running = True
        self.save_simulation_renders = False
        self.t = 0

        self.logger = logging.getLogger('enactive-agents')
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def enable_console_logger(self):
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def enable_file_logger(self, file_path):
        # Create file logger handler
        ch = logging.FileHandler(filename = file_path)
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

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

    def set_experiment(self, experiment):
        self.experiment = experiment

    def get_experiment(self):
        return self.experiment

    def toggle_pause(self):
        self.running = not self.running

    def toggle_saving_simulation_renders(self):
        """
        Toggle whether simulation renders should be saved on or off, depending on the
        current setting.
        """
        self.save_simulation_renders = not self.save_simulation_renders

    def is_running(self):
        return self.running

    def get_save_simulation_renders(self):
        return self.save_simulation_renders

    def increment_t(self):
        """
        Increment the simulation clock by one tick.
        """
        self.t += 1

    def set_t(self, t):
        self.t = t

    def get_t(self):
        return self.t

    def get_logger(self):
        return self.logger
