import time
import serial
import os

def startUp():
    print("*****************************************************")
    print("                   PUMP: StartUp                     ")
    print("*****************************************************\n")
    print("Please read the instructions before continuing")
    print("1. Make sure the ports are correctly input in the config file.")
    print("2. Initially, pump should be stopped (NOT TURNED OFF!). Read documentation if you do not understand")
    os.system('pause')
    print("Starting Process . . . ")
    time.sleep(1)

def connectPump(port):

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    return ser

def sendCommand(ser, command, waitForOutput=True, tries=3):
    # For debug
    # return "OK\r\n"
    # try sending the send three times.
    for _ in range(tries):
        # encode string
        commandEncoded = command.encode()
        # write
        ser.write(commandEncoded)
        # wait for the output to return
        if waitForOutput:
            time.sleep(0.1)
            output = ''
            while ser.inWaiting() > 0:
                output += ser.read(1).decode()
            if output != '':
                return output
    return None


def setFlowRate(ser, flow_rate, waitForOutput=True, tries=2):
    try_count = 0
    while try_count <= tries:
        # change . to ,
        fowRateEURO = str(round(float(flow_rate), 1)).replace('.', ',')
        while len(fowRateEURO) != 5:
            fowRateEURO = '0' + fowRateEURO
        output = sendCommand(ser, "SMM=" + fowRateEURO + "!", waitForOutput=waitForOutput)
        valid = validate_output(output)
        if valid:
            return valid
        try_count += 1

    if try_count > tries:
        return False


def togglePump(ser, waitForOutput=True, tries=2):
    try_count = 0
    while try_count <= tries:
        output = sendCommand(ser, "TA2!", waitForOutput=waitForOutput)
        valid = validate_output(output)
        if valid:
            return valid
        try_count += 1

    if try_count > tries:
        return False


def validate_output(output):
    if output is not None:
        print("Output from pump:", output.strip())
        if output == "OK\r\n":
            print("Successfully send command\n")
            return True
        else:
            print("Failed to send command\n")
            return False
    else:
        print("Error: no output from pump. possibly the rs232 got disconnected.")


def getDesiredFlowRate(elapsedTime, flowRates, timeList):
    indexTime = 0
    if elapsedTime > timeList[-1]:
        indexTime = -1
    else:
        for index, pointInTime in enumerate(timeList):

            if elapsedTime < pointInTime:
                indexTime = index - 1
                break

    return flowRates[indexTime]

def serialConsole(ser):
    #ser.open()
    print('Enter your commands below.\r\nInsert "exit" to leave the application.')
    userInput = 1
    while 1:
        # get keyboard input
        # Python 2 users
        # input = raw_input(">> ")
        # Python 3 users
        userInput = input(">> ")

        # type exit to exit console
        if userInput == 'exit':
            ser.close()
            exit()
        else:
            # send the character to the device
            # (note that I dont happend a \r\n carriage return and line feed to the characters - this is not requested by my device)

            #convert to bytes
            userInputBytes = userInput.encode()
            ser.write(userInputBytes)
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1).decode()

            if out != '':
                print(">> " + out)


if __name__ == '__main__':
    ser = connectPump('COM3')
    print(ser.port)
    # send one command
    print(sendCommand(ser, "DSP?", waitForOutput=True))
    # start console
    serialConsole(ser)
