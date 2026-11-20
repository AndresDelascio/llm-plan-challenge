def _res(qty, created_s, paid):
    return {"qty": qty, "created_s": created_s, "paid": paid}

def test_1():
    "wrong count with no reservations"
    assert available(10, [], 0) == 10

def test_2():
    "wrong count with one unpaid reservation made 100 seconds ago"
    assert available(10, [_res(3, 100, False)], 200) == 7

def test_3():
    "wrong count with one unpaid reservation made 301 seconds ago"
    assert available(10, [_res(3, 100, False)], 401) == 10

def test_4():
    "wrong count with one paid reservation made 10000 seconds ago"
    assert available(10, [_res(3, 0, True)], 10000) == 7

def test_5():
    "wrong count when live reservations exceed the stock"
    assert available(2, [_res(5, 100, False)], 150) == 0

def test_6():
    "wrong count with a mix of paid, live and expired reservations"
    assert available(10, [_res(2, 0, True), _res(3, 0, False), _res(4, 900, False)], 1000) == 4
