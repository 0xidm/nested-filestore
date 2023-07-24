import os
import shutil

import pytest

from nested_filestore import NestedFilestore
from nested_filestore.tarball import TarballNestedFilestore


@pytest.fixture()
def filestore():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return NestedFilestore("/tmp/filestore", [3, 3, 3])

@pytest.fixture()
def tarball_filestore():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return TarballNestedFilestore("/tmp/filestore", [3, 3, 3])

@pytest.fixture()
def tarball_little_filestore():
    shutil.rmtree("/tmp/filestore", ignore_errors=True)
    return TarballNestedFilestore("/tmp/filestore", [1, 1, 1])
