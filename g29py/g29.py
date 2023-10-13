import hid
import time
import threading
import logging as log

NAME = "Logitech G29 Driving Force Racing Wheel"
GUID = "030000006d0400004fc2000011010000"
VENDOR_ID = 1133
PRODUCT_ID = 49743

STEERING_COARSE_AXIS = 4
STEERING_FINE_AXIS = 5
ACCELERATOR_AXIS = 6
BRAKE_AXIS = 7
CLUTCH_AXIS = 8
SLOT_RANGE = [0x1, 0xF]

class G29:
    cache = None
    state = {
        "steering": 50,
        "accelerator": 255,
        "clutch": 255,
        "brake": 255
    }

    def __init__(self):
        try:
            device = hid.Device(VENDOR_ID, PRODUCT_ID)
        except:
            raise Exception("Device not found. Is it plugged in?")
        log.debug(f'Device manufacturer: {device.manufacturer}')
        log.debug(f'Product: {device.product}')
        self.device = device

    def connect(self):
        self.pump() # load cache
        self.reset()

    def reset(self):
        # wheel calibration
        self.device.write(bytes([0xf8, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00]))
        self.device.write(bytes([0xf8, 0x09, 0x05, 0x01, 0x01, 0x00, 0x00]))
        time.sleep(10) # wait for calibration

    # WRITE

    def force_constant(self, val=0.5):
        if val < 0 or val > 1:
            raise ValueError("force_constant val must be between 0 and 1")
        # normalze to 0-255
        val = round(int(val * 255))
        log.debug(f'force_constant: {val}')
        msg = [0x11, 0x00, val, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_friction(self, val=0.5):
        if val < 0 or val > 1:
            raise ValueError("force_fricion val must be between 0 and 1")
        # normalze to 0-8
        val = round(int(val * 8))
        log.debug(f'force_friction: {val}')
        msg = [0x21, 0x02, val, 0x00, val, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_range(self, val=400):
        if val < 400 or val > 900:
            raise ValueError("set_range val must be between 400 and 900")
        range1 = val & 0x00ff
        range2 = (val & 0xff00) >> 8
        log.debug(f'range: {range1},{range2}')
        msg = [0xf8, 0x81, range1, range2, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_autocenter(self, strength=0.5, rate=0.05):
        if strength < 0 or strength > 1:
            raise ValueError("force_constant val must be between 0 and 1")
        if rate < 0 or rate > 1:
            raise ValueError("force_constant val must be between 0 and 1")
        # autocenter up
        up_msg = [0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(up_msg))
        # normalze strength to 0-15
        strength = round(int(strength * 15))
        # normalze rate to 0-255
        rate = round(int(rate * 255))
        log.debug(f'autocenter: {strength} {rate}')
        msg = [0xfe, 0x0d, strength, strength, rate, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_anticenter(self, angle1=180, angle2=180, strength=0.5, reverse=0x0, force=0.5):
        if angle1 < 0 or angle1 > 255:
            raise ValueError("angle1 val must be between 0 and 255")
        if angle2 < 0 or angle2 > 255:
            raise ValueError("angle2 val must be between 0 and 255")
        if reverse < 0 or reverse > 1:
            raise ValueError("reverse val must be between 0 and 1")
        if strength < 0 or strength > 15:
            raise ValueError("force_constant val must be between 0 and 1")
        # normalze strength to 0-15
        strength = round(int(strength * 15))
        # normalze force to 0-255
        force = round(int(force * 255))
        log.debug(f'anticenter: {angle1} {angle2} {strength} {reverse} {force}')
        msg = [0x11, 0x03, 0x00, 0x00, 0x00, 0x00, force]
        self.device.write(bytes(msg))
        

    def autocenter_off(self):
        msg = [0xf5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    # slot 0-4, or 0xf3 for all
    def force_off(self, slot=0xf3):
        if slot < 0 or slot > 4 and slot !=0xf3:
            raise ValueError("force_off slot must be between 0 and 4 or 0xf3")
        log.debug(f'force_off: {slot}')
        msg = [slot, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    # READ

    def pump(self, timeout=10):
        dat = self.device.read(16, timeout)

        # only handle 12 byte msgs
        byte_array = bytearray(dat)
        if len(byte_array) >= 12:
            self.update_state(byte_array)
            self.cache = byte_array
            
        return dat

    def start_pumping(self, timeout=10):
        self.pump_thread = threading.Thread(target=self.pump_forever, args=(timeout,))
        self.pump_thread.start()

    def pump_forever(self, timeout=10):
        while 1:
            self.pump(timeout)
    
    def stop_pumping(self):
        if self.thread is not None:
            self.pump_thread.join()
    
    def get_state(self):
        return self.state
    
    def update_state(self, byte_array):
        if self.cache is None:
            log.warn("cache not available")
            return 

        # update only diffs
        # steering
        if byte_array[4] != self.cache[4] or byte_array[5] != self.cache[5]:
            steering_val = self.calc_steering(byte_array[5], byte_array[4])
            self.state["steering"] = steering_val
        # accelerator
        if byte_array[6] != self.cache[6]:
            self.state["accelerator"] = byte_array[6]
        # brake
        if byte_array[7] != self.cache[7]:
            self.state["brake"] = byte_array[7]
        # clutch
        if byte_array[8] != self.cache[8]:
            self.state["clutch"] = byte_array[8]

    def calc_steering(self, coarse, fine):
        # coarse 0-255        # fine 0-255
        # normalize to 0-100
        coarse = (coarse/256) * (100-(100/256))
        # normalize to 0-3
        fine = (fine/256) * (100/256)
        # add together
        return round(coarse + fine)
