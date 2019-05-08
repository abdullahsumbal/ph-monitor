# import serial
#
# ser = serial.Serial()
# ser.baudrate = 9600
# ser.port = 'COM3'
# print(ser)
# ser.open()
# print(ser.is_open)
# ser.write(b'DSP?')
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    # parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,
    # bytesize=serial.EIGHTBITS
)

print(ser)

ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    print(input)
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        ser.flush()
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        print(ser.inWaiting())
        print(ser.out_waiting)
        # while ser.inWaiting() > 0:
        #     print(ser.inWaiting())
        out += ser.read(10)

        if out != '':
            print ">>" + out