import usb.core
import usb.util

vendor_id = 0x2447
product_id = 0x4

device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

# use the first/default configuration
# device.set_configuration()
print(device)

endpoint = device[0][(0,0)][0]
# print(endpoint)

# read a data packet
data = None
# data = device.read(endpoint.bEndpointAddress,
#                    endpoint.wMaxPacketSize)
while True:
    try:
        data = device.read(endpoint.bEndpointAddress,
                           endpoint.wMaxPacketSize)
        print("data",data)

    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue