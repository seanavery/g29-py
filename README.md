# g29py
> python driver for logitech g29 wheel/pedals

<p align="center">
  <a href="https://pkg.go.dev/go.viam.com/rdk"><img src="https://pkg.go.dev/badge/go.viam.com/rdk" alt="PkgGoDev"></a>
</p>

#### install
`$ pip install g29py`

```
from g29py import G29
g29 = G29()
g29.connect()
```

```
# write 
g29.set_range(500)
g29.set_friction(0.5)
```

```
#read
g29.start_pumping() 
while 1:
    state = g29.get_state()
    print("steering:", state["steering"])
    print("brake:", state["brake"])
```

#### sources

- Write.md Read.md 
- Commands based on nightmode's [logitech-g29](https://github.com/nightmode/logitech-g29) node.js driver.
- Interface uses libhidapi ctype bindings from apmorton's [pyhidapi](https://github.com/apmorton/pyhidapi).


### support

Only Logitech G29 Driving Force Racing Wheels & Pedals kit supported on linux in ps3 mode.
