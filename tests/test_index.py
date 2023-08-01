import pytest

from nested_filestore.index import Index


def test_sync():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert len(i.groups) > 0
    assert len(i.get_group("/0/0").items) > 0
    assert len(i.get_group("/0/5").items) > 0
    assert len(i.get_group("/4/2").items) > 0

def test_which_group():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert i.which_group('420') == '/4/2'

def test_item_exists():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert i.exists('420')
    assert not i.exists('421')

def test_min_max():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert i.min == '0'
    assert i.max == '420'

def test_tgz():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert i.get_group("/0/1").is_tarball
    assert i.exists('10')
    assert not i.exists('9')
    assert not i.exists('20')

    assert i.get_item(11).inside_tarball
    assert not i.get_item(1).inside_tarball

def test_get_group():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert i.get_group("/0/1")
    assert pytest.raises(ValueError, i.get_group, "/0/2")

def test_get_item():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert i.get_item(0)
    assert i.get_item(11)
    assert i.get_item(19)
    assert i.get_item(420)
    assert pytest.raises(ValueError, i.get_item, 421)

def test_missing():
    i = Index(path="tests/data/filestore-1-1-1", dimensions=[1,1,1])
    i.sync()
    assert len(list(i.missing)) > 400
