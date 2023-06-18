import hid
import time 

NAME = "Logitech G29 Driving Force Racing Wheel"
GUID = "030000006d0400004fc2000011010000"
VENDOR_ID = 1133
PRODUCT_ID = 49743

class G29:
    def __init__(self):
        device = hid.Device(VENDOR_ID, PRODUCT_ID)
        print(f'Device manufacturer: {device.manufacturer}')
        print(f'Product: {device.product}')
        print(f'Serial Number: {device.serial}')
        self.device = device

    def connect(self):
        # test read
        dat = self.device.read(1024, 100)
        print(dat)

        self.device.write([0xf8, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.device.write([0xf8, 0x09, 0x05, 0x01, 0x01, 0x00, 0x00])


        # wheel calibration
        

    def wheel_init(self):
        


        
    
        