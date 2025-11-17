import pytest
import multiprocessing
from project.hashtable_multiprocessing import HashTable


def test_basic_methods():
    """Test all basic methods"""
    t = HashTable(num_slots=8)
    assert len(t) == 0
    t["k1"] = 1
    assert t["k1"] == 1
    t["k1"] = 3
    assert t["k1"] == 3
    assert len(t) == 1
    t["k2"] = 2
    assert t["k2"] == 2
    assert len(t) == 2
    with pytest.raises(KeyError):
        assert t["k3"]
    assert "k1" in t
    assert "k3" not in t
    del t["k2"]
    assert len(t) == 1
    with pytest.raises(KeyError):
        del t["k2"]
    t.clear()
    assert len(t) == 0


def incr(ht, keys):
    for k in keys:
        ht[k] = k + 1


def cleaning(t):
    t.clear()


def test_parallel_insert_clear():
    """Test parallel insert and clear"""
    t = HashTable()
    lists = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    keys = list(range(9))
    for k in keys:
        t[k] = k

    proc = []
    for sp in lists:
        p = multiprocessing.Process(target=incr, args=(t, sp))
        proc.append(p)
        p.start()
    for p in proc:
        p.join()
    assert len(t) == len(keys)
    for k in keys:
        assert t[k] == k + 1

    clear_proc = []
    for i in range(5):
        p = multiprocessing.Process(target=cleaning, args=(t,))
        clear_proc.append(p)
        p.start()
    for p in clear_proc:
        p.join()
    assert len(t) == 0
    for k in keys:
        assert k not in t


def incr_val(t, key):
    for i in range(100):
        t[key] = t.get(key, 0) + 1


def test_no_deadlock():
    """Test that hash table has not deadlock"""
    t = HashTable()
    for k in range(5):
        t[k] = k
    proc = []
    for i in range(5):
        p = multiprocessing.Process(target=incr_val, args=(t, i))
        proc.append(p)
    for p in proc:
        p.start()
    for p in proc:
        p.join(timeout=5)
    for k in range(5):
        exp = k + 100
        assert t[k] == exp
