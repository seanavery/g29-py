import hid
import time
import threading
import logging as log
from .params import *

class G29:
    cache = None
    state = {
        "steering": 0.0,
        "accelerator": -1.0,
        "clutch": -1.0,
        "brake": -1.0,
        "buttons": {
            "gamepad": {
                "up": 0,
                "down": 0,
                "left": 0,
                "right": 0,
                "X": 0,
                "O": 0,
                "S": 0,
                "T": 0
            },
            "misc": {
                "R2": 0,
                "R3": 0,
                "L2": 0,
                "L3": 0,
                "Share": 0,
                "Options": 0,
            },
            "+": 0,
            "misc2": {
                "-": 0,
                "track": 0,
                "back": 0,
                "PS": 0,
            },
        }
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
        """Sets the force constant of the wheel.

        Args:
            val (float, optional): Defaults to 0.5.

        Raises:
            ValueError: force_constant val must be between 0 and 1
        """
        if val < 0 or val > 1:
            raise ValueError("force_constant val must be between 0 and 1")
        # normalze to 0-255
        val = round(int(val * 255))
        log.debug(f'force_constant: {val}')
        msg = [0x11, 0x00, val, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_friction(self, val=0.5):
        """Sets the friction of the wheel.

        Args:
            val (float, optional): Defaults to 0.5.

        Raises:
            ValueError: force_fricion val must be between 0 and 1
        """
        if val < 0 or val > 1:
            raise ValueError("force_fricion val must be between 0 and 1")
        # normalze to 0-8
        val = round(int(val * 8))
        log.debug(f'force_friction: {val}')
        msg = [0x21, 0x02, val, 0x00, val, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_range(self, val=400):
        """Sets the range of the wheel.

        Args:
            val (int, optional): Defaults to 400.

        Raises:
            ValueError: set_range val must be between 400 and 900
        """
        if val < 400 or val > 900:
            raise ValueError("set_range val must be between 400 and 900")
        range1 = val & 0x00ff
        range2 = (val & 0xff00) >> 8
        log.debug(f'range: {range1},{range2}')
        msg = [0xf8, 0x81, range1, range2, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    def set_autocenter(self, strength=0.5, rate=0.05):
        """Sets the autocenter of the wheel.

        Args:
            strength (float, optional): Defaults to 0.5.
            rate (float, optional): Defaults to 0.05.

        Raises:
            ValueError: strength val must be between 0 and 1
            ValueError: rate val must be between 0 and 1
        """
        if strength < 0 or strength > 1:
            raise ValueError("strength val must be between 0 and 1")
        if rate < 0 or rate > 1:
            raise ValueError("rate val must be between 0 and 1")
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
        """_summary_

        Args:
            angle1 (int, optional): Defaults to 180.
            angle2 (int, optional): Defaults to 180.
            strength (float, optional): Defaults to 0.5.
            reverse (hexadecimal, optional): Defaults to 0x0.
            force (float, optional): _description_to 0.5.

        Raises:
            ValueError: angle1 val must be between 0 and 255
            ValueError: angle2 val must be between 0 and 255
            ValueError: reverse val must be between 0 and 1
            ValueError: force_constant val must be between 0 and 1
        """
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
        """Turns off autocentering"""
        msg = [0xf5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.device.write(bytes(msg))

    # slot 0-4, or 0xf3 for all
    def force_off(self, slot=0xf3):
        """_summary_

        Args:
            slot (hexadecimal, optional): Defaults to 0xf3.

        Raises:
            ValueError: slot must be between 0 and 4 or 0xf3
        """
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
        if byte_array[GAME_PAD] != self.cache[GAME_PAD]:
            self.update_gamepad(byte_array[GAME_PAD])
        if byte_array[BUTTON_MISC] != self.cache[BUTTON_MISC]:
            self.update_misc(byte_array[BUTTON_MISC])
        if byte_array[BUTTON_PLUS] != self.cache[BUTTON_PLUS]:
            print("byte_array[2] != self.cache[2]", byte_array[2])
        if byte_array[BUTTON_MISC2] != self.cache[BUTTON_MISC2]:
            self.update_misc2(byte_array[BUTTON_MISC2])
        if byte_array[STEERING_COARSE] != self.cache[STEERING_COARSE] or byte_array[STEERING_FINE] != self.cache[STEERING_FINE]:
            steering_val = self.calc_steering(byte_array[STEERING_FINE], byte_array[STEERING_COARSE])
            self.state["steering"] = steering_val
        if byte_array[PEDAL_ACCELERATOR] != self.cache[PEDAL_ACCELERATOR]:
            self.state["accelerator"] = self.calc_pedal(byte_array[PEDAL_ACCELERATOR])
        if byte_array[PEDAL_BRAKE] != self.cache[PEDAL_BRAKE]:
            self.state["brake"] = self.calc_pedal(byte_array[7])
        if byte_array[PEDAL_CLUTCH] != self.cache[PEDAL_CLUTCH]:
            self.state["clutch"] = self.calc_pedal(byte_array[8])

    def calc_steering(self, coarse, fine):
        # coarse 0-255
        # fine 0-255
        # TODO: implemeent fine tune
        coarse_normalized = (coarse / 255.0) * 2 - 1
        
        return coarse_normalized

    def calc_pedal(self, val):
        # input 255-0
        normalized = (255 - val) / 255.0

        # scale to -1 to 1
        return normalized * 2 - 1
    
    def update_gamepad(self, val):
        if val == GAME_PAD_NIL:
            for k in self.state["buttons"]["gamepad"]:
                self.state["buttons"]["gamepad"][k] = 0
        if val == GAME_PAD_UP:
            self.state["buttons"]["gamepad"]["up"] = 1
        if val == GAME_PAD_DOWN:
            self.state["buttons"]["gamepad"]["down"] = 1
        if val == GAME_PAD_RIGHT:
            self.state["buttons"]["gamepad"]["right"] = 1
        if val == GAME_PAD_LEFT:
            self.state["buttons"]["gamepad"]["left"] = 1
        if val == GAME_PAD_X:
            self.state["buttons"]["gamepad"]["X"] = 1
        if val == GAME_PAD_SQUARE:
            self.state["buttons"]["gamepad"]["S"] = 1
        if val == GAME_PAD_CIRCLE:
            self.state["buttons"]["gamepad"]["O"] = 1
        if val == GAME_PAD_TRIANGLE:
            self.state["buttons"]["gamepad"]["T"] = 1
            
    def update_misc(self, val):
        if val == MISC_NIL:
            for k in self.state["buttons"]["misc"]:
                self.state["buttons"]["misc"][k] = 0
        if val == MISC_R2:
            self.state["buttons"]["misc"]["R2"] = 1
        if val == MISC_R3:
            self.state["buttons"]["misc"]["R3"] = 1
        if val == MISC_L2:
            self.state["buttons"]["misc"]["L2"] = 1
        if val == MISC_L3:
            self.state["buttons"]["misc"]["L3"] = 1
        if val == MISC_SHARE:
            self.state["buttons"]["misc"]["Share"] = 1
        if val == MISC_OPTIONS:
            self.state["buttons"]["misc"]["Options"] = 1

    def update_misc2(self, val):
        # handle nil case
        if val == MISC2_NIL:
            for k in self.state["buttons"]["misc2"]:
                self.state["buttons"]["misc2"][k] = 0
        if val == MISC2_MINUS:
            self.state["buttons"]["misc2"]["-"] = 1
        if val == MISC2_TRACK_RIGHT:
            self.state["buttons"]["misc2"]["track"] = 1
        if val == MISC2_TRACK_LEFT:
            self.state["buttons"]["misc2"]["track"] = -1
        if val == MISC2_BACK:
            self.state["buttons"]["misc2"]["back"] = 1
        if val == MISC_PSTATION:
            self.state["buttons"]["PS"] = 1
            