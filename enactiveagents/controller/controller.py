"""
Main world controller.
"""

from appstate import AppState
import pygame
import events

class Controller(events.EventListener):
    """
    Controller class.
    """

    experiment_controller = None

    def __init__(self):
        pass

    def quit(self):
        """ 
        Gracefully quit the simulator.
        """

        quitEvent = events.QuitEvent()
        AppState.get_state().get_event_manager().post_event(quitEvent)

    def set_experiment_controller(self, experiment_controller):
        self.experiment_controller = experiment_controller

    def process_input(self):
        """
        Process user input.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    return
                elif event.key == pygame.K_SPACE:
                    AppState.get_state().toggle_pause()
                    return
            
            if self.experiment_controller:     
                if pygame.mouse.get_focused():
                    self.experiment_controller(event, pygame.mouse.get_pos())
                else:
                    self.experiment_controller(event, None)

    def notify(self, event):
        if isinstance(event, events.ControlEvent):
            self.process_input()
