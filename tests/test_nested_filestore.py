import pytest

from nested_filestore.item import Item


def test_filestore_resolve(existing_filestore):
    group_uri = existing_filestore.index.which_group(12)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=12).path == "tests/data/filestore-3-3-3/000/000/12.bin"

    group_uri = existing_filestore.index.which_group(123)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=123).path == "tests/data/filestore-3-3-3/000/000/123.bin"

    group_uri = existing_filestore.index.which_group(1234)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=1234).path == "tests/data/filestore-3-3-3/000/001/1234.bin"

    group_uri = existing_filestore.index.which_group(12345)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=12345).path == "tests/data/filestore-3-3-3/000/012/12345.bin"

    group_uri = existing_filestore.index.which_group(123456)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=123456).path == "tests/data/filestore-3-3-3/000/123/123456.bin"

    group_uri = existing_filestore.index.which_group(1234567)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=1234567).path == "tests/data/filestore-3-3-3/001/234/1234567.bin"

    group_uri = existing_filestore.index.which_group(12345678)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=12345678).path == "tests/data/filestore-3-3-3/012/345/12345678.bin"

    group_uri = existing_filestore.index.which_group(123456789)
    group = existing_filestore.index.get_group(group_uri)
    assert Item(group=group, identifier=123456789).path == "tests/data/filestore-3-3-3/123/456/123456789.bin"

def test_filestore_workflow(filestore):
    # ensure the test file does not exist before we start
    assert not filestore.exists(12345678)

    filestore.put(12345678, "tests/data/12345678.bin")
    assert filestore.exists(12345678)
    with filestore.get(12345678) as f:
        assert f.read() == b"hi"

def test_does_not_exist(filestore):
    # ensure the test file does not exist before we start
    assert not filestore.exists(12345678)

    # try to get the file and ensure it raises ValueError
    with pytest.raises(ValueError):
        filestore.get(12345678)

def test_filestore_min_max(filestore):
    filestore.put(12, "tests/data/12345678.bin")
    filestore.put(1234, "tests/data/12345678.bin")
    filestore.put(12345678, "tests/data/12345678.bin")
    assert filestore.index.min == "12"
    assert filestore.index.max == "12345678"
