"""
Module Supervisor
"""
import threading
from sender import SenderThread


class SupervisorThread(threading.Thread):
    """
    SupervisorThread class
    This supervises any changes for all the gpios and send them in case of changes
    """
    gpios = []
    deleted_gpios = []

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.__event = event
        self.__nonStop = True

    @staticmethod
    def get_changed_ports():
        """
        Get a list of ports whose port status has changed
        """
        changed_gpios = []
        for gpio in SupervisorThread.gpios:
            if gpio.has_changed():
                changed_gpios.append(gpio)
                gpio.changes_send()
        return changed_gpios

    def run(self):
        while self.__nonStop:
            try:
                ports_to_send = SupervisorThread.get_changed_ports()
                if len(ports_to_send) > 0:
                    print('GPIOs changed detected')
                    deleted_gpios = SupervisorThread.deleted_gpios
                    msg = SenderThread.get_gpios_json(ports_to_send, deleted_gpios)
                    print('MSG to return: ' + msg)
                    SenderThread.msg = msg
                    SupervisorThread.deleted_gpios = []
                    self.__event.set()
                    self.__event.clear()
            except Exception as e:
                print(e)
                break
        print('Supervisor finished')

    def stop(self):
        self.__nonStop = False