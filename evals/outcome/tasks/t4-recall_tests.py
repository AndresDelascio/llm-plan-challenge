def _close(a, b):
    return isinstance(a, (int, float)) and abs(a - b) < 1e-9

def test_1():
    "wrong recall for highlights [(0,10),(20,30)] and clips [(2,5),(22,25)]"
    assert _close(clip_recall([(0, 10), (20, 30)], [(2, 5), (22, 25)]), 1.0)

def test_2():
    "wrong recall when there are no clips"
    assert _close(clip_recall([(0, 10)], []), 0.0)

def test_3():
    "wrong recall for highlight (0,10) and clip (10,15)"
    assert _close(clip_recall([(0, 10)], [(10, 15)]), 0.0)

def test_4():
    "wrong recall for highlights [(0,10),(20,30)] and one clip (5,25)"
    assert _close(clip_recall([(0, 10), (20, 30)], [(5, 25)]), 0.5)

def test_5():
    "wrong recall for highlights [(0,10),(8,12)] and clips [(5,9),(0,3)]"
    assert _close(clip_recall([(0, 10), (8, 12)], [(5, 9), (0, 3)]), 1.0)

def test_6():
    "wrong recall for highlights [(0,10),(8,20),(18,30)] and clips [(5,9),(15,19),(0,3)]"
    assert _close(clip_recall([(0, 10), (8, 20), (18, 30)], [(5, 9), (15, 19), (0, 3)]), 1.0)
