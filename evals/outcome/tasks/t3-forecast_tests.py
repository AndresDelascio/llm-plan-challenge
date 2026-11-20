SALES = [5, 1, 4, 2, 8, 6, 3, 9, 7, 10]

def _close(a, b):
    return isinstance(a, (int, float)) and abs(a - b) < 1e-9

def test_1():
    "wrong forecast for day=9, window=3 on a 10-day list"
    assert _close(trailing_mean(SALES, 9, 3), 19 / 3)

def test_2():
    "wrong forecast for day=7 with the default window on a 10-day list"
    assert _close(trailing_mean(SALES, 7), 29 / 7)

def test_3():
    "day=0 should return None"
    assert trailing_mean(SALES, 0) is None

def test_4():
    "wrong forecast for day=3 with the default window (only 3 days of history)"
    assert _close(trailing_mean(SALES, 3), 10 / 3)

def test_5():
    "wrong forecast for day=1 with the default window"
    assert _close(trailing_mean(SALES, 1), 5.0)

def test_6():
    "wrong forecast for tomorrow (day=10 on a 10-day list)"
    assert _close(trailing_mean(SALES, 10), 45 / 7)
