"""
Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified and updatedautomatically.
"""

import abc


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


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a phmeter.
    """

    def __init__(self):
        self._phmeter = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class ConcreteObserver(Observer):
    """
    Implement the Observer updating interface to keep its state
    consistent with the phmeter's.
    Store state that should stay consistent with the phmeter's.
    """

    def update(self, arg):
        self._observer_state = arg
        # ...


def main():
    phmeter = Phmeter()
    concrete_observer = ConcreteObserver()
    phmeter.attach(concrete_observer)
    phmeter.phmeter_state = 123


if __name__ == "__main__":
    main()