"""
Main world controller.
"""

import os
from time import strftime
import cPickle
from appstate import AppState
import pygame
import events
import settings

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
                elif event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    self.save_agent()
                    return
                elif event.key == pygame.K_w and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    self.save_world()
                    return
                elif event.key == pygame.K_e and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    self.save_experiment()
                    return
                elif event.key == pygame.K_h:
                    self.help()
                    return
                elif event.key == pygame.K_r:
                    AppState.get_state().toggle_saving_simulation_renders()
                    if AppState.get_state().get_save_simulation_renders():
                        print "Now saving simulation renders to file."
                    else:
                        print "No longer saving simulation renders to file."
                    return
            
            if self.experiment_controller:
                if pygame.mouse.get_focused():
                    self.experiment_controller(event, pygame.mouse.get_pos())
                else:
                    self.experiment_controller(event, None)

    def save_world(self):
        """
        Save the world to file.
        """

        print "---"
        print "Press [enter] to write the world to file, or [escape] to cancel."

        while True:
             event = pygame.event.wait()
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE:
                     print "Saving cancelled."
                     print "---"
                     return
                 elif event.key == pygame.K_RETURN:
                     break
        
        try:
            import dill
        except ImportError:
            print "ERROR: Module 'dill' is required to save worlds."
        else:       
            print "Saving the world to file..."

            # Create output directory if it does not exist
            if not os.path.exists(settings.WORLD_DIR):
                os.makedirs(settings.WORLD_DIR)

            # Pickle and save agents to file
            file_name = "%s.p" % strftime("%Y%m%dT%H%M%S")
            file_path = os.path.join(settings.WORLD_DIR, file_name)

            print " - Saving world to %s" % file_path
            dill.dump(AppState.get_state().get_world(), open(file_path, "wb"))

            print "World saved."

        print "---"

    def save_experiment(self):
        """
        Save the experiment to file.
        """

        print "---"
        print "Press [enter] to write the experiment to file, or [escape] to cancel."

        while True:
             event = pygame.event.wait()
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE:
                     print "Saving cancelled."
                     print "---"
                     return
                 elif event.key == pygame.K_RETURN:
                     break
        
        try:
            import dill
        except ImportError:
            print "ERROR: Module 'dill' is required to save experiments."
        else:       
            print "Saving the experiment to file..."

            # Create output directory if it does not exist
            if not os.path.exists(settings.EXPERIMENT_DIR):
                os.makedirs(settings.EXPERIMENT_DIR)

            # Pickle and save agents to file
            file_name = "%s.p" % strftime("%Y%m%dT%H%M%S")
            file_path = os.path.join(settings.EXPERIMENT_DIR, file_name)

            print " - Saving experiment to %s" % file_path
            dill.dump(AppState.get_state().get_experiment(), open(file_path, "wb"))

            print "Experiment saved."

        print "---"

    def save_agent(self):
        """
        Save all agents to files.
        """
        print "---"
        print "Press [enter] to write all agents to file, or [escape] to cancel."

        while True:
             event = pygame.event.wait()
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE:
                     print "Saving cancelled."
                     print "---"
                     return
                 elif event.key == pygame.K_RETURN:
                     break
             
        print "Saving agents to file..."

        # Create output directory if it does not exist
        if not os.path.exists(settings.AGENT_DIR):
            os.makedirs(settings.AGENT_DIR)

        # Pickle and save agents to file
        agents = AppState.get_state().get_world().get_agents()
        for agent in agents:
            file_name = "%s - %s.p" % (strftime("%Y%m%dT%H%M%S"), agent.get_name())
            file_path = os.path.join(settings.AGENT_DIR, file_name)

            print " - Saving %s to %s" % (agent.get_name(), file_path)
            cPickle.dump(agent, open(file_path, "wb"))

        print "Agents saved."

        print "---"

    def help(self):
        """
        Show controller help information.
        """
        print "---"
        print "Controls:"
        print " - [escape]      - quit the simulation"
        print " - [space]       - pause the simulation"
        print " - [control] + s - save the agents to file"
        print " - h             - show this help information"
        print " - r             - toggle saving simulation renders to disk"
        print ""
        print "Press any key to continue."
        while True:
             event = pygame.event.wait()
             if event.type == pygame.KEYDOWN:
                 break
        print "---"

    def notify(self, event):
        if isinstance(event, events.ControlEvent):
            self.process_input()
