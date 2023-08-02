import os
import shutil

import pytest

from nested_filestore import NestedFilestore
from nested_filestore.index import Index


@pytest.fixture()
def filestore():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return NestedFilestore("/tmp/filestore", [3, 3, 3])

@pytest.fixture()
def existing_filestore():
    return NestedFilestore("tests/data/filestore-3-3-3", [3, 3, 3])

@pytest.fixture()
def index_filestore():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return Index(path="/tmp/filestore", dimensions=[3, 3, 3])

@pytest.fixture()
def little_index_filestore():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return Index(path="/tmp/filestore", dimensions=[1, 1, 1])
