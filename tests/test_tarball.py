import os
import shutil

import pytest

from nested_filestore.tarball import TarballNestedFilestore


def test_init_tarball():
    filestore = TarballNestedFilestore(
        root_path="/tmp/filestore",
        hierarchy_order=[3, 3, 3],
        base=10,
    )
    assert filestore.root_path == "/tmp/filestore"
    assert filestore.hierarchy_order == [3, 3, 3]
    assert filestore.base == 10
    assert filestore.pad_character == "0"
    assert filestore.container_size == 1000

def test_tarball_workflow(gzip_tarball_filestore):
    # ensure the test file does not exist before we start
    assert not gzip_tarball_filestore.exists(12345678)
    gzip_tarball_filestore.put(12345678, "tests/data/12345678.bin")
    assert gzip_tarball_filestore.exists(12345678)
    with gzip_tarball_filestore.get(12345678) as f:
        assert f.read() == b"hi"

def test_little_tarball(gzip_tarball_little_filestore):
    assert gzip_tarball_little_filestore.container_size == 10

def test_tarball_create(gzip_tarball_little_filestore):
    assert not gzip_tarball_little_filestore.container_full(0)

    for i in range(0, 9):
        gzip_tarball_little_filestore.put(i, "tests/data/12345678.bin")
        assert not gzip_tarball_little_filestore.container_full(i)
    
    gzip_tarball_little_filestore.put(9, "tests/data/12345678.bin")
    assert gzip_tarball_little_filestore.container_full(9)

    for i in range(10, 19):
        gzip_tarball_little_filestore.put(i, "tests/data/12345678.bin")
        assert not gzip_tarball_little_filestore.container_full(i)

    gzip_tarball_little_filestore.put(19, "tests/data/12345678.bin")
    assert gzip_tarball_little_filestore.container_full(19)

    gzip_tarball_little_filestore.tarball_scan()

    assert os.path.exists("/tmp/filestore/0/0.tgz")
    assert os.path.exists("/tmp/filestore/0/1.tgz")

    gzip_tarball_little_filestore.put(20, "tests/data/12345678.bin")
    assert os.path.exists("/tmp/filestore/0/2/20.bin")

def test_tarball_get(gzip_tarball_little_filestore):
    for i in range(0, 9):
        gzip_tarball_little_filestore.put(i, "tests/data/12345678.bin")
        assert not gzip_tarball_little_filestore.container_full(i)
    gzip_tarball_little_filestore.put(9, "tests/data/12345679.bin")
    gzip_tarball_little_filestore.put(10, "tests/data/12345679.bin")
    gzip_tarball_little_filestore.put(11, "tests/data/12345678.bin")

    gzip_tarball_little_filestore.tarball_scan()
    assert os.path.exists("/tmp/filestore/0/0.tgz")

    # get an index that is in the tarball
    with gzip_tarball_little_filestore.get(1) as f:
        assert f.read() == b"hi"

    # this is in the tarball with different content
    with gzip_tarball_little_filestore.get(9) as f:
        assert f.read() == b"bye"

    # this one is not inside a tarball
    with gzip_tarball_little_filestore.get(10) as f:
        assert f.read() == b"bye"

def test_tarball_tiny_get():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return TarballNestedFilestore("/tmp/filestore", [1, 1])

    for i in range(0, 10):
        tarball_tiny_filestore.put(i, "tests/data/12345678.bin")
        assert not tarball_tiny_filestore.container_full(i)

    assert os.path.exists("/tmp/filestore/0.tgz")

    # get an index that is in the tarball
    for i in range(0, 10):
        with tarball_tiny_filestore.get(i) as f:
            assert f.read() == b"hi"

def test_scan(gzip_tarball_little_filestore):
    for i in range(0, 39):
        gzip_tarball_little_filestore.put(i, "tests/data/12345678.bin")

    assert not os.path.exists("/tmp/filestore/0/0.tgz")

    gzip_tarball_little_filestore.tarball_scan()
    assert os.path.exists("/tmp/filestore/0/0.tgz")
    assert os.path.exists("/tmp/filestore/0/1.tgz")
    assert os.path.exists("/tmp/filestore/0/2.tgz")
