import time

from g29py import G29

def test_init():
    g29 = None
    try:
        g29 = G29()
    except:
        assert False
    finally:
        assert g29 is not None

def test_reset():
    g29 = G29()
    assert g29 is not None
    g29.reset()
    assert True # did not throw

# TODO: test_connect

# WRITE

def test_force_off():
    g29 = G29()
    g29.force_off(0xf3)
    assert True # did not throw

# def test_force_constant():
#     g29 = G29()
#     # g29.connect()
#     g29.force_constant(0.7)

def test_force_friction():
    g29 = G29()
    g29.force_friction(0.5)
    assert True # did not throw
    time.sleep(5)
    g29.force_off(0xf3)
    assert True # did not throw

def test_set_range():
    g29 = G29()
    g29.set_range(500)
    assert True # did not throw
    time.sleep(5)
    g29.set_range(900) # set back to full range
    assert True # did not throw

def test_set_autocenter():
    g29 = G29()
    g29.set_autocenter(0.5, 0.5)
    assert True # did not throw
    time.sleep(5)
    g29.autocenter_off()

# def test_init_g29():
#     g29 = G29()
#     # g29.force_constant(0.5)
#     # g29.force_friction(0.5)
#     # g29.set_range(500)
#     # g29.set_autocenter(0.1, 0.2)
#     # g29.autocenter_off()
#     g29.start_pumping()
    
#     while 1:
#         print(g29.get_state()['steering'])
#         time.sleep(0.01)