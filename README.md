# g29py
> python driver for logitech g29 wheel/pedals

> :warning: **Warning**: g29py is alpha software. This repository is under heavy development and subject to breaking changes. :warning:

![](etc/g29py.jpg)

## Install
```bash
pip install g29py
```

## Use

```python
from g29py import G29
g29 = G29()
```

```python
# write 
g29.set_range(500)
g29.set_friction(0.5)
```

```python
# read
g29.start_pumping() # thread
while 1:
    state = g29.get_state()
    print("steering:", state["steering"])
    print("brake:", state["brake"])
    print("accelerator", state["accelerator"])
```

## Read

### Pedals/Steering

| Pedal         | Value Range      | Neutral Position |
|---------------|------------------|------------------|
| `steering`    | Float: -1 to 1   | 0 (Centered)     |
| `accelerator` | Float: -1 to 1   | -1 (Not pressed) |
| `clutch`      | Float: -1 to 1   | -1 (Not pressed) |
| `brake`       | Float: -1 to 1   | -1 (Not pressed) |

### Buttons

| Button  | Value |
|---------|-------|
| `up`    | 0/1   |
| `down`  | 0/1   |
| `left`  | 0/1   |
| `right` | 0/1   |
| `X`     | 0/1   |
| `O`     | 0/1   |
| `S`     | 0/1   |
| `T`     | 0/1   |
| `R2`    | 0/1   |
| `R3`    | 0/1   |
| `L2`    | 0/1   |
| `L3`    | 0/1   |
| `Share` | 0/1   |
| `Options` | 0/1 |
| `+`     | 0/1   |
| `-`     | 0/1   |
| `track` | -1/1  |
| `back`  | 0/1   |
| `PS`    | 0/1   |

## Write

| Method Name       | Default Parameters                         | Parameter Types                  |
|-------------------|--------------------------------------------|----------------------------------|
| `force_constant`  | `val=0.5`                                  | `val`: float                     |
| `set_friction`    | `val=0.5`                                  | `val`: float                     |
| `set_range`       | `val=400`                                  | `val`: int                       |
| `set_autocenter`  | `strength=0.5, rate=0.05`                  | `strength`: float, `rate`: float |
| `set_anticenter`  | `angle1=180, angle2=180, strength=0.5, reverse=0x0, force=0.5` | `angle1`: int, `angle2`: int, `strength`: float, `reverse`: hexadecimal, `force`: float |
| `autocenter_off`  | None                                       | None                             |
| `force_off`       | `slot=0xf3`                                | `slot`: hexadecimal              |

## Sources

- Commands based on nightmode's [logitech-g29](https://github.com/nightmode/logitech-g29) node.js driver.
- Interface uses libhidapi ctype bindings from apmorton's [pyhidapi](https://github.com/apmorton/pyhidapi).
- Reference [wiki-brew](https://wiibrew.org/wiki/Logitech_USB_steering_wheel) for effects API.

## Support

Only Logitech G29 Driving Force Racing Wheels & Pedals kit supported on linux in ps3 mode.

On linux, remove sudo requirements by adding udev rule.

```bash
echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' \
    | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules
sudo udevadm control --reload-rules
```
