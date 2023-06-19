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
    
        # wheel calibration
        self.device.write(bytes([0xf8, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00]))
        self.device.write(bytes([0xf8, 0x09, 0x05, 0x01, 0x01, 0x00, 0x00]))
        time.sleep(10) # wait for calibration

    def wheel_init(self):
        return 0

    def force_constant(self, val=0.5):
        # normalze to 0-255
        val = round(int(val * 255))
        print("force_constant:", val)
        msg = [0x11, 0x00, val, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    def force_friction(self, val=0.5):
        # normalze to 0-8
        val = round(int(val * 8))
        print("force_friction:", val)
        msg = [0x21, 0x02, val, 0x00, val, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_range(self, val=400):
        assert val >= 400 and val <= 900
        range1 = val & 0x00ff
        range2 = (val & 0xff00) >> 8
        print('range:', range1, range2)
        msg = [0xf8, 0x81, range1, range2, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))
