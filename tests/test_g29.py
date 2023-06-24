import time

from g29py import G29

def test_init():
    g29 = G29()
    assert g29 is not None

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