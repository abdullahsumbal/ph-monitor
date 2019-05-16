"""
Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified and updatedautomatically.
"""

import abc
import ph
import pump
import json
import sys
import time
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
            observer.phDependentUpdate(self._phmeter_state)

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

    def __init__(self, pumpData):
        self._phmeter = None
        self.isOn = False
        self.ser = None
        self.port = pumpData["PORT"]
        self.targetPh = pumpData["TARGET_PH"]
        self.acidic = pumpData["ACIDIC"]
        self.margin = pumpData["MARGIN"]

    def connect(self):
        self.ser = pump.connectPump(self.port)

        if self.ser.isOpen():
            print("{} is open".format(self.port))
            # TODO: Initialize the pump state
        else:
            print("Error {} is not open".format(self.port))
            sys.exit()

    @abc.abstractmethod
    def phDependentUpdate(self, arg):
        pass


class PhDependentPump(Pump):
    """
    Implement the Observer updating interface to keep its state
    consistent with the phmeter's.
    Store state that should stay consistent with the phmeter's.
    """

    def phDependentUpdate(self, arg):
        # currently arg is phValue
        output = ""
        commandWasSend = False
        phMeterValue = float(arg)
        waitForOutput = True # Maybe: this could be added in config
        if self.acidic: # pump has acidic solution
            if self.targetPh < phMeterValue: # ph read is more than target
                if not self.isOn: # ph is not acidic enough, so start pumping
                    output = pump.sendCommand(self.ser, "TA2!", waitForOutput=waitForOutput)
                    commandWasSend = True
            else: # ph read is less than target
                if self.isOn: # ph is already acidic enough, so stop pumping
                    output = pump.sendCommand(self.ser, "TA2!", waitForOutput=waitForOutput)
                    commandWasSend = True
        else: # pump has base solution
            if self.targetPh < phMeterValue: # ph read is more than target
                if self.isOn:  # ph is already basic enough, so stop pumping
                    output = pump.sendCommand(self.ser, "TA2!", waitForOutput=waitForOutput)
                    commandWasSend = True
            else: # ph read is less than target
                if not self.isOn: # ph is not basic enough, so start pumping
                    output = pump.sendCommand(self.ser, "TA2!", waitForOutput=waitForOutput)
                    commandWasSend = True

        print("{} | Target ph: {} | Ph Value: {} | isAcidic: {} | Pump state: {} | Command send: {}".format(self.port,
                                                                                                       self.targetPh,
                                                                                                       phMeterValue,
                                                                                                       self.acidic,
                                                                                                       self.isOn, commandWasSend))
        if waitForOutput and output != "":
            print("Output from pump:", output.strip())
            if output == "OK\r\n":
                print("Successfully send command\n")
                self.isOn = not self.isOn
            else:
                print("Failed to send command\n")

class TimeDependentPump(Pump):
    """
        This pump does not depend on ph and it depends on time.
    """
    def __init__(self, pumpData):
        self.isOn = False
        self.port = pumpData["PORT"]
        self.timeList = pumpData["TIME"]
        self.flowRates = pumpData["FLOW_RATES"]

    def phDependentUpdate(self, arg):
        pass

    def validateConfig(self):
        return len(self.timeList) != len(self.flowRates)

    def timeDependentUpdate(self, elapsedTime):

        indexTime = 0
        commandWasSend = False
        output = ''
        waitForOutput = True  # Maybe: this could be added in config
        if elapsedTime > self.timeList[-1]:
            indexTime = -1
        else:
            for index, pointInTime in enumerate(self.timeList):

                if elapsedTime < pointInTime:
                    indexTime = index - 1
                    break

        desiredFlowRate = self.flowRates[indexTime]

        if desiredFlowRate == 0:
            if self.isOn: # turn off pump is flow rate is 0
                output = pump.sendCommand(self.ser, "TA2!", waitForOutput=waitForOutput)
                commandWasSend = True
                self.isOn = not self.isOn
        else:
            temp = str(round(float(desiredFlowRate),1)).replace('.',',')
            while(len(temp) != 5):
                temp = '0' + temp
            print(temp)
            if not self.isOn:
                output = pump.sendCommand(self.ser, "TA2!", waitForOutput=waitForOutput)
                self.isOn = not self.isOn
            output = pump.sendCommand(self.ser, "SMM="+temp+"!", waitForOutput=waitForOutput)
            commandWasSend = True

        print("{} | Flow Rate: {} | Elapsed Time: {} | Pump state: {} | Command send: {}".format(self.port, desiredFlowRate, elapsedTime, self.isOn, commandWasSend))
        if waitForOutput and output != "":
            print("Output from pump:", output.strip())
            if output == "OK\r\n":
                print("Successfully send command\n")
            else:
                print("Failed to send command\n")


def StartProces(config):
    """
    This function starts recording ph, connects to pump and send commands to pump
    """

    # ph data from configuration file
    phData = config["PH_METERS"]
    phReadInterval = phData["PH_LOG_INTERVAL"]


    # pump data from configuration file
    pumpsData = config["PUMPS"]
    phDependentPumpsIgnore = pumpsData["PH_DEPENDENT_IGNORE"]
    timeDependentPumpsIgnore = pumpsData["TIME_DEPENDENT_IGNORE"]
    phDependentPumpsData = pumpsData['PH_DEPENDENT']
    timeDependentPumpsData = pumpsData['TIME_DEPENDENT']

    # Validate pump
    pump.startUp()

    # Initialize ph dependent pumps observers
    print("*****************************************************")
    print("                 Pump: Connection                     ")
    print("*****************************************************\n")
    if not phDependentPumpsIgnore:
        # Add Subject which is your ph meter (ph application)
        phmeter = Phmeter()
        # ph Observers/listeners which are your ph dependent pumps
        ph_observers = []

        for pumpData in phDependentPumpsData:
            concrete_pump = PhDependentPump(pumpData)
            concrete_pump.connect()
            ph_observers.append(concrete_pump)

        # Make pump(observer) listen to subject (ph meter).
        for observer in ph_observers:
            phmeter.attach(observer)

    if not timeDependentPumpsIgnore:
        time_observers = []
        for pumpData in timeDependentPumpsData:
            # TODO: validate config
            concrete_pump = TimeDependentPump(pumpData)
            if concrete_pump.validateConfig():
                print("Error: Configuration Incorrect. Length of flow rate and time does not match")
                sys.exit()
            concrete_pump.connect()
            time_observers.append(concrete_pump)

    # Validate if ph application is running correctly.
    if not phDependentPumpsIgnore:
        ph.preStartUp()
        ph.startUp()
        phValueLocationX, phValueLocationY = ph.isParalyLogging(interval=phReadInterval)
    print("*****************************************************")
    print("             Read PH and Command ")
    print("*****************************************************\n")
    # Pumps something according to the ph value.
    start_time = time.time() # experiment start time
    while True:
        # TODO: validate if getting the same time , that means mouse has been moved.
        if not phDependentPumpsIgnore:
            phMeterValue, rowData = ph.getHP(phValueLocationX, phValueLocationY)
            phmeter.phmeter_state = phMeterValue # updating this value notifies the observer
        if not timeDependentPumpsIgnore:
            time.sleep(3)
            elapsed_time = time.time() - start_time
            for time_observer in time_observers:
                time_observer.timeDependentUpdate(elapsed_time)


if __name__ == "__main__":
    # Read config file
    filename = "configuration.json"
    if filename:
        with open(filename, 'r') as f:
            config = json.load(f)

    # Start process
    StartProces(config)
