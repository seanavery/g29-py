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

| Key           | Description                         | Value Range      | Neutral Position |
|---------------|-------------------------------------|------------------|------------------|
| steering    | Steering wheel position.            | Float: -1 to 1   | 0 (Centered)     |
| accelerator | Accelerator pedal position.         | Float: -1 to 1   | -1 (Not pressed) |
| clutch      | Clutch pedal position.              | Float: -1 to 1   | -1 (Not pressed) |
| brake       | Brake pedal position.               | Float: -1 to 1   | -1 (Not pressed) |


### Buttons

| Button  | Value |
|---------|-------|
| Up      | 0/1   |
| Down    | 0/1   |
| Left    | 0/1   |
| Right   | 0/1   |
| X       | 0/1   |
| O       | 0/1   |
| S       | 0/1   |
| T       | 0/1   |
| R2      | 0/1   |
| R3      | 0/1   |
| L2      | 0/1   |
| L3      | 0/1   |
| Share   | 0/1   |
| Options | 0/1   |
| +       | 0/1   |
| -       | 0/1   |
| Track   | -1/1  |
| Back    | 0/1   |
| PS      | 0/1   |

## Sources

- Commands based on nightmode's [logitech-g29](https://github.com/nightmode/logitech-g29) node.js driver.
- Interface uses libhidapi ctype bindings from apmorton's [pyhidapi](https://github.com/apmorton/pyhidapi).


## Support

Only Logitech G29 Driving Force Racing Wheels & Pedals kit supported on linux in ps3 mode.

On linux, remove sudo requirements by adding udev rule.

```bash
echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' \
    | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules
sudo udevadm control --reload-rules
```
