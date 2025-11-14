import pytest
from project.hashtable import HashTable


def test_set_get_len():
    """Test set, get, len methods"""
    t = HashTable()
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


def test_contain():
    """Test contain method"""
    t = HashTable()
    t["k1"] = 1
    assert "k1" in t
    assert "k2" not in t


def test_delete():
    """Test delition of items"""
    t = HashTable()
    t["k"] = 1
    assert "k" in t
    del t["k"]
    assert "k" not in t
    with pytest.raises(KeyError):
        del t["k"]


def test_clear():
    """Test clear method"""
    t = HashTable()
    t["k1"] = 1
    t["k2"] = 2
    t.clear()
    assert len(t) == 0
    assert list(t.keys()) == []


def test_resize():
    """Test resize method"""
    t = HashTable(num_slots=2)
    t["a"] = 1
    t["b"] = 2
    assert len(t) == 2
    assert t["a"] == 1
    assert t["b"] == 2
    t["c"] = 3
    assert t["c"] == 3
    assert t.num_slots == 4


def test_hash_same():
    """Test hash of same key"""
    t = HashTable()
    key = "k"
    a = t._hash(key)
    b = t._hash(key)
    assert a == b


def test_collision():
    """Test collision"""
    t = HashTable(num_slots=2)
    keys = ["k1", "k2", "k3", "k4"]
    vals = [1, 2, 3, 4]
    for k, v in zip(keys, vals):
        t[k] = v
    for k, v in zip(keys, vals):
        assert t[k] == v
        assert k in t
    for k, v in zip(keys, vals):
        del t[k]
        assert k not in t
