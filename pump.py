import time
import serial


def connectPump(ports):

    serialConnections = []

    for port in ports:

        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        ser.isOpen()
        serialConnections.append(ser)

    return serialConnections


def sendCommand(ser, command, waitForOutput=True):
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
    serialConnections = connectPump(['COM3'])
    ser = serialConnections[0]
    # send one command
    print(sendCommand(ser, "DSP?", waitForOutput=True))
    # start console
    serialConsole(ser)
