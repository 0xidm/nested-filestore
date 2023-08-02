import os
import pytest

from nested_filestore.index import Index


def test_sync():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert len(i.groups) > 0
    assert len(i.get_group("/0/0").items) > 0
    assert len(i.get_group("/0/5").items) > 0
    assert len(i.get_group("/4/2").items) > 0

def test_which_group():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.which_group('420') == '/4/2'

def test_item_exists():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.exists('420')
    assert not i.exists('421')

def test_min_max():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.min == '0'
    assert i.max == '420'

def test_tgz():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.get_group("/0/1").is_tarball
    assert i.exists('10')
    assert not i.exists('9')
    assert not i.exists('20')

    assert i.get(11).inside_tarball
    assert not i.get(1).inside_tarball

    assert i.get_group("/0/1").path == "tests/data/filestore-1-1-1/0/1.tgz"
    assert i.get(11).path == "tests/data/filestore-1-1-1/0/1/11.bin"
    assert i.get(50).path == "tests/data/filestore-1-1-1/0/5/50.bin"

def test_get_group():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.get_group("/0/1")
    assert pytest.raises(ValueError, i.get_group, "/0/2")

def test_get():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.get(0)
    assert i.get(11)
    assert i.get(19)
    assert i.get(420)
    assert pytest.raises(ValueError, i.get, 421)

def test_missing():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert len(list(i.missing)) > 400

def test_tarball_fill():
    i = Index(path="tests/data/filestore-3-3-3", dimensions=[3,3,3])
    assert i.min == '0'
    assert i.max == '123456789'
    assert i.get_group("/000/000").is_tarball
    assert not i.get_group("/000/002").is_tarball

def test_get():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    assert i.get(0)

def test_put():
    i = Index(path="/tmp/filestore", dimensions=[1,1,1])
    i.put(12, "tests/data/12345678.bin")

def test_index_workflow(index_filestore):
    assert not index_filestore.exists(12345678)

    index_filestore.put(12345678, "tests/data/12345678.bin")
    assert index_filestore.exists(12345678)
    with index_filestore.get(12345678).open() as f:
        assert f.read() == b"hi"

def test_index_full(little_index_filestore):
    little_index_filestore = Index(path="/tmp/filestore", dimensions=[1,1,1])
    item = little_index_filestore.put(0, "tests/data/12345678.bin")
    assert not item.group.is_full

    assert pytest.raises(ValueError, little_index_filestore.put, 0, "tests/data/12345678.bin")

    for i in range(1, 9):
        little_index_filestore.put(i, filename="tests/data/12345678.bin")
    assert pytest.raises(ValueError, item.group.compact)

    item = little_index_filestore.put(9, filename="tests/data/12345678.bin")
    assert item.group.is_full
    assert item.group.compact()

    for i in range(10, 19):
        little_index_filestore.put(i, filename="tests/data/12345678.bin")

    item = little_index_filestore.put(19, filename="tests/data/12345678.bin")
    assert item.group.is_full
    assert item.group.compact()

    assert os.path.exists("/tmp/filestore/0/0.tgz")
    assert os.path.exists("/tmp/filestore/0/1.tgz")

    little_index_filestore.put(20, filename="tests/data/12345678.bin")
    assert os.path.exists("/tmp/filestore/0/2/20.bin")
