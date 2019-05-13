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


def serialConsole(ser):
    print('Enter your commands below.\r\nInsert "exit" to leave the application.')
    userInput = 1
    while 1:
        # get keyboard input
        # Python 2 users
        # input = raw_input(">> ")
        # Python 3 users
        userInput = input(">> ")
        if userInput == 'exit':
            ser.close()
            exit()
        else:
            # send the character to the device
            # (note that I dont happend a \r\n carriage return and line feed to the characters - this is not requested by my device)
            ser.write(userInput)
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1)

            if out != '':
                print (">> " + out)


if __name__ == '__main__':
    serialConnections = connectPump(['COM4'])
    ser = serialConnections[0]
    serialConsole(ser)
