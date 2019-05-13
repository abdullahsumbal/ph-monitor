"""
Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified and updatedautomatically.
"""

import abc
import ph


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

    @abc.abstractmethod
    def update(self, arg):
        pass


class ConcretePump(Pump):
    """
    Implement the Observer updating interface to keep its state
    consistent with the phmeter's.
    Store state that should stay consistent with the phmeter's.
    """

    def update(self, arg):
        self._pump_state = arg
        # ...


def startup():
    # subject
    phmeter = Phmeter()
    # listeners
    concrete_pump_1 = ConcretePump()
    concrete_pump_2 = ConcretePump()
    phmeter.attach(concrete_pump_1)
    phmeter.attach(concrete_pump_2)

    # Validate if ph application is running
    ph.preStartUp()
    ph.startUp()
    x, y = ph.isParalyLogging()

    # get ph values
    while(True):
        # TODO: validate if getting the same time , that means mouse has been moved.

        ph_value = ph.getHP(x, y)
        phmeter.phmeter_state = ph_value
        print("pump 1:", concrete_pump_1._pump_state)
        print("pump 2:", concrete_pump_2._pump_state)


def main():
    phmeter = Phmeter()
    concrete_pump = ConcretePump()
    phmeter.attach(concrete_pump)
    for i in range(10):
        phmeter.phmeter_state = i
        print(concrete_pump._pump_state)


if __name__ == "__main__":
    startup()
