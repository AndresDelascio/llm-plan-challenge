def _close(a, b):
    return isinstance(a, (int, float)) and abs(a - b) < 1e-9

def test_1():
    "wrong time for start_tick=0, stop_tick=10000"
    assert _close(gate_time_s(0, 10000), 1.0)

def test_2():
    "wrong time for start_tick=1000, stop_tick=31000"
    assert _close(gate_time_s(1000, 31000), 3.0)

def test_3():
    "wrong time for start_tick=5, stop_tick=5"
    assert _close(gate_time_s(5, 5), 0.0)

def test_4():
    "wrong time for start_tick=60000, stop_tick=4464"
    assert _close(gate_time_s(60000, 4464), 1.0)

def test_5():
    "wrong time for start_tick=65535, stop_tick=0"
    assert _close(gate_time_s(65535, 0), 0.0001)
