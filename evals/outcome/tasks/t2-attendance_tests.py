def _rec(player, date, status, updated_at):
    return {"player": player, "date": date, "status": status, "updated_at": updated_at}

def _norm(records):
    return sorted((r["player"], r["date"], r["status"], r["updated_at"]) for r in records)

A = _rec("Ana", "2026-03-01", "present", "2026-03-01T18:00:00-05:00")
B = _rec("Ben", "2026-03-01", "absent", "2026-03-01T18:01:00-05:00")

def test_1():
    "wrong result for two different players with no duplicates"
    assert _norm(merge_attendance([A, B])) == _norm([A, B])

def test_2():
    "wrong result for an empty list"
    assert list(merge_attendance([])) == []

def test_3():
    "an exact duplicate of a record is not removed"
    assert _norm(merge_attendance([A, dict(A), B])) == _norm([A, B])

def test_4():
    "a correction sent 10 minutes later with the same UTC offset does not replace the first record"
    late = _rec("Ana", "2026-03-01", "absent", "2026-03-01T18:10:00-05:00")
    assert _norm(merge_attendance([A, late])) == _norm([late])
    assert _norm(merge_attendance([late, A])) == _norm([late])

def test_5():
    "the same player on two dates should keep both records"
    other = _rec("Ana", "2026-03-08", "absent", "2026-03-08T18:00:00-05:00")
    assert _norm(merge_attendance([A, other])) == _norm([A, other])

def test_6():
    "wrong record kept when one update is 18:05 at offset -05:00 and the other is 20:00 at offset +00:00 on the same day"
    newer = _rec("Ana", "2026-03-01", "absent", "2026-03-01T18:05:00-05:00")
    older = _rec("Ana", "2026-03-01", "present", "2026-03-01T20:00:00+00:00")
    assert _norm(merge_attendance([newer, older])) == _norm([newer])
    assert _norm(merge_attendance([older, newer])) == _norm([newer])
