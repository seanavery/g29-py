from g29_py import G29

def test_init_g29():
    g29 = G29()
    # g29.connect()
    # g29.force_constant(0.5)
    g29.force_friction(0.5)