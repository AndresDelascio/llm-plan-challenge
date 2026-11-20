def _same(got, want):
    return got is not None and len(got) == 2 and all(abs(g - w) < 1e-9 for g, w in zip(got, want))

def test_1():
    "wrong result for the frame center (960, 540)"
    assert _same(to_tracker(960, 540), (360, 270))

def test_2():
    "wrong result for (240, 0)"
    assert _same(to_tracker(240, 0), (0, 0))

def test_3():
    "wrong result for (100, 500)"
    assert to_tracker(100, 500) is None

def test_4():
    "wrong result for (1700, 500)"
    assert to_tracker(1700, 500) is None

def test_5():
    "wrong result for (241, 1)"
    assert _same(to_tracker(241, 1), (0.5, 0.5))

def test_6():
    "wrong result for (1000, 333)"
    assert _same(to_tracker(1000, 333), (380, 166.5))
