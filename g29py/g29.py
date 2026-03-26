import hid
import time
import threading
import copy
import logging as log
from .params import *

class G29:
    # Add dial
    def __init__(self):
        self.connected = False
        self.cache = None
        self.state_lock = threading.Lock()
        self.state = {
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
                    "dial": DIAL_CENTER, # -100 to 100
                    "PS": 0,
                },
            }
        }
        self.dial_val = DIAL_CENTER
        self.pump_thread = None
        try:
            device = hid.Device(VENDOR_ID, PRODUCT_ID)
        except:
            raise Exception("Device not found. Is it plugged in?")
        log.debug(f'Device manufacturer: {device.manufacturer}')
        log.debug(f'Product: {device.product}')
        self.device = device
        self.connected = True

    # TODO(seanp): Why is reset not working?
    def reset(self):
        # wheel calibration
        self.device.write(bytes([0xf8, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00]))
        self.device.write(bytes([0xf8, 0x09, 0x05, 0x01, 0x01, 0x00, 0x00]))
        time.sleep(5) # wait for calibration

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

    def read(self, timeout=10):
        try:
            dat = self.device.read(16, timeout)
        except Exception as e:
            log.error("G29 disconnected: %s", e)
            self.connected = False
            return

        # only handle 12 byte msgs
        byte_array = bytearray(dat)
        if len(byte_array) >= 12:
            self.update_state(byte_array)
            self.cache = byte_array
        return dat

    def listen(self, timeout=10):
        if self.pump_thread is not None and self.pump_thread.is_alive():
            return
        self.pump_thread = threading.Thread(target=self.pump, args=(timeout,))
        self.pump_thread.start()

    def pump(self, timeout=10):
        while self.connected:
            self.read(timeout)

    def stop_pumping(self):
        if self.pump_thread is None:
            return
        if not self.pump_thread.is_alive():
            self.pump_thread = None
            return
        self.pump_thread.join()
        self.pump_thread = None

    def get_state(self):
        if not self.connected:
            raise Exception("G29 not connected")
        with self.state_lock:
            return copy.deepcopy(self.state)

    def update_state(self, byte_array):
        with self.state_lock:
            self.state = self.decode_packet(byte_array)

    def decode_packet(self, byte_array):
        state = {
            "steering": self.calc_steering(
                byte_array[STEERING_COARSE],
                byte_array[STEERING_FINE],
            ),
            "accelerator": self.calc_pedal(byte_array[PEDAL_ACCELERATOR]),
            "clutch": self.calc_pedal(byte_array[PEDAL_CLUTCH]),
            "brake": self.calc_pedal(byte_array[PEDAL_BRAKE]),
            "buttons": {
                "gamepad": {
                    "up": 0,
                    "down": 0,
                    "left": 0,
                    "right": 0,
                    "X": 0,
                    "O": 0,
                    "S": 0,
                    "T": 0,
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
                    "dial": self.dial_val,
                    "PS": 0,
                    "back": 0,
                },
            },
        }
        self.apply_gamepad(state, byte_array[GAME_PAD])
        self.apply_misc(state, byte_array[BUTTON_MISC])
        self.apply_plus(state, byte_array[BUTTON_PLUS])
        self.apply_misc2(state, byte_array[BUTTON_MISC2])
        return state

    def calc_steering(self, coarse_byte, fine_byte):
        # coarse 0-255
        # fine 0-255
        steering_raw = (coarse_byte << 8) | fine_byte  # 0-65535 for 16 bit integer
        # scale to -1 to 1
        steering_normalized = (steering_raw / 65535.0) * 2 - 1

        return steering_normalized

    def calc_pedal(self, val):
        # input 255-0
        normalized = (255 - val) / 255.0

        # scale to -1 to 1
        return normalized * 2 - 1

    def apply_gamepad(self, state, val):
        if val == GAME_PAD_NIL:
            return
        elif val == GAME_PAD_UP:
            state["buttons"]["gamepad"]["up"] = 1
        elif val == GAME_PAD_DOWN:
            state["buttons"]["gamepad"]["down"] = 1
        elif val == GAME_PAD_RIGHT:
            state["buttons"]["gamepad"]["right"] = 1
        elif val == GAME_PAD_LEFT:
            state["buttons"]["gamepad"]["left"] = 1
        elif val == GAME_PAD_X:
            state["buttons"]["gamepad"]["X"] = 1
        elif val == GAME_PAD_SQUARE:
            state["buttons"]["gamepad"]["S"] = 1
        elif val == GAME_PAD_CIRCLE:
            state["buttons"]["gamepad"]["O"] = 1
        elif val == GAME_PAD_TRIANGLE:
            state["buttons"]["gamepad"]["T"] = 1
        else:
            log.debug(f"unknown gamepad value: {val}")

    def apply_misc(self, state, val):
        if val == MISC_NIL:
            return
        elif val == MISC_R2:
            state["buttons"]["misc"]["R2"] = 1
        elif val == MISC_R3:
            state["buttons"]["misc"]["R3"] = 1
        elif val == MISC_L2:
            state["buttons"]["misc"]["L2"] = 1
        elif val == MISC_L3:
            state["buttons"]["misc"]["L3"] = 1
        elif val == MISC_SHARE:
            state["buttons"]["misc"]["Share"] = 1
        elif val == MISC_OPTIONS:
            state["buttons"]["misc"]["Options"] = 1
        else:
            log.debug(f"unknown misc value: {val}")

    def apply_plus(self, state, val):
        if val == BUTTON_PLUS_ON:
            state["buttons"]["+"] = 1
        elif val == BUTTON_PLUS_NIL:
            state["buttons"]["+"] = 0
        else:
            log.debug(f"unknown plus value: {val}")

    def apply_misc2(self, state, val):
        if val == MISC2_NIL:
            return
        elif val == MISC2_MINUS:
            state["buttons"]["misc2"]["-"] = 1
        elif val == MISC2_TRACK_RIGHT:
            state["buttons"]["misc2"]["dial"] = self.update_dial(1)
        elif val == MISC2_TRACK_LEFT:
            state["buttons"]["misc2"]["dial"] = self.update_dial(-1)
        elif val == MISC2_BACK:
            state["buttons"]["misc2"]["back"] = 1
        elif val == MISC_PSTATION:
            state["buttons"]["misc2"]["PS"] = 1
        else:
            log.debug(f"unknown misc2 value: {val}")

    def update_dial(self, val):
        pos = self.dial_val + val
        # check pos is in range
        if pos > DIAL_CENTER + DIAL_RANGE / 2:
            pos = DIAL_CENTER + DIAL_RANGE / 2
        if pos < DIAL_CENTER - DIAL_RANGE / 2:
            pos = DIAL_CENTER - DIAL_RANGE / 2
        self.dial_val = pos
        return pos
