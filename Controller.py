"""
Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified and updatedautomatically.
"""

import abc
import ph
import pump
import json
# TODO: create a looger
import logging

####################################################
# Class Structure For subject and observer design pattern
####################################################

class Phmeter:
    """
    Know its observers (pump). Any number of Observer objects (pumps) may observe a
    phmeter value.
    Send a notification to its observers(pumps) when ph state changes.
    """

    def __init__(self):
        self._observers = set()
        self._phmeter_state = None

    def attach(self, observer):
        observer._phmeter = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._phmeter = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._phmeter_state)

    @property
    def phmeter_state(self):
        return self._phmeter_state

    @phmeter_state.setter
    def phmeter_state(self, arg):
        self._phmeter_state = arg
        self._notify()


class Pump(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a phmeter.
    """

    def __init__(self):
        self._phmeter = None
        self._pump_state = None
        self.ser = None

    @abc.abstractmethod
    def connect(self, port):
        pass

    @abc.abstractmethod
    def update(self, arg):
        pass


class ConcretePump(Pump):
    """
    Implement the Observer updating interface to keep its state
    consistent with the phmeter's.
    Store state that should stay consistent with the phmeter's.
    """

    def connect(self, port):
        self.ser = pump.connectPump(port)

        if self.ser.isOpen():
            print("{} is open".format(port))
        else:
            print("Error {} is not open".format(port))

    def update(self, arg):
        # currently arg is phValue
        phValue = arg
        self._pump_state = phValue
        # do something when you get ph value
        pump.sendCommand(self.ser, "TA2!", waitForOutput=True)


def StartProces(config):
    """
        This function starts recording ph, connects to pump and send commands to pump
    """

    # Validate pump
    pump.startUp()

    # Add Subject which is your ph meter (ph application)
    phmeter = Phmeter()
    # Observers/listeners which are your pumps
    observers = []
    ports = config["pumps"]
    phReadInterval = config["ph_read_interval"]

    # Initialize pumps observers
    print("*****************************************************")
    print("                 Pump: Connection                     ")
    print("*****************************************************\n")
    for port in ports:
        concrete_pump = ConcretePump()
        concrete_pump.connect(port)
        observers.append(concrete_pump)

    # Make pump(observer) listen to subject.
    for observer in observers:
        phmeter.attach(observer)

    # Validate if ph application is running correctly.
    ph.preStartUp()
    ph.startUp()
    phValueLocationX, phValueLocationY = ph.isParalyLogging(interval=phReadInterval)


    print("*****************************************************")
    print("             Read PH and Command ")
    print("*****************************************************\n")
    # Pumps something according to the ph value.
    while True:
        # TODO: validate if getting the same time , that means mouse has been moved.
        phValue, rowData = ph.getHP(phValueLocationX, phValueLocationY)
        phmeter.phmeter_state = phValue
        for observer in observers:
            print("Pump at port {}: {}".format(observer.ser.port, observer._pump_state))


if __name__ == "__main__":
    # read config file
    filename = "configuration.json"
    if filename:
        with open(filename, 'r') as f:
            config = json.load(f)

    # start process
    StartProces(config)
