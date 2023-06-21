# g29py
> python driver for logitech g29 wheel/pedals


#### Install
`$ pip install g29py`

```
from g29py import G29

g29 = G29()

# write 
g29.wheel_cal()
g29.set_friction(0.5)

#read
g29.start_pumping() 
while 1:
    state = g29.get_state()
    print("steering:", state["steering"])
    print("brake:", state["brake"])

```

#### Sources

- Commands based on nightmode's [logitech-g29](https://github.com/nightmode/logitech-g29) node.js driver.
- Interface uses libhidapi ctype bindings from apmorton's [pyhidapi](https://github.com/apmorton/pyhidapi).


