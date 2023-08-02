import os
import tarfile
import threading
from functools import cached_property

import ratarmountcore as rmc

from .item import Item
from .exceptions import GroupNotFullError


class Group:
    def __init__(self, index, identifier:str, is_tarball=None):
        self.identifier = str(identifier)
        self.index = index

        # determine min and max from index dimensions and identifier
        group_name = identifier.replace("/", "")
        self._bucket_size = self.index.base ** self.index.dimensions[0]
        self._bucket_min = int(group_name) * self._bucket_size
        self._bucket_max = self._bucket_min + self._bucket_size

        self._is_tarball = is_tarball
        self._tar_lock = threading.Lock()
        self._tar_rmc = None
        self._items = dict()

    def add(self, identifier:str):
        identifier = str(identifier)
        self._items[identifier] = Item(self, identifier)

    def get(self, identifier:str):
        identifier = str(identifier)
        if self.is_tarball:
            if identifier not in self._items:
                self._items[identifier] = Item(self, identifier)
            return self._items[identifier]
        elif self.exists(identifier):
            return self._items[identifier]
        else:
            raise ValueError(f"{identifier} not found in {self}")

    @cached_property
    def _ratarmount(self):
        if self._tar_rmc is None:
            self._tar_rmc = rmc.open(self._path_tgz, recursive=True)
        return self._tar_rmc

    @property
    def is_full(self):
        return not self.is_tarball and len(self._items) >= self._bucket_size

    @property
    def is_tarball(self):
        if self._is_tarball is None:
            self._is_tarball = os.path.isfile(self._path_tgz)
        return self._is_tarball

    @cached_property
    def uri(self):
        return self.identifier

    @property
    def path(self):
        if self._is_tarball:
            return self._path_tgz
        else:
            return self._path_dir

    @cached_property
    def _path_dir(self):
        return f"{self.index.path}{self.uri}"

    @cached_property
    def _path_tgz(self):
        return f"{self.index.path}{self.uri}.tgz"

    @property
    def min(self):
        if self.is_tarball:
            return str(self._bucket_min)
        return self.items[next(iter(sorted(self.items)))].identifier

    @property
    def max(self):
        if self.is_tarball:
            return str(self._bucket_max)
        return self.items[next(reversed(sorted(self.items)))].identifier

    @property
    def items(self):
        return self._items

    def __repr__(self):
        return self.identifier

    def exists(self, identifier:str):
        if self.is_tarball:
            return True
        return str(identifier) in self._items

    def compact(self):
        "create a tarball for this group"
        if not self.is_full:
            raise ValueError(f"cannot compact non-full group {self}")

        tarball_filename = self._path_tgz
        container_path = self.uri
        full_container_path = self._path_dir

        with self._tar_lock:
            filenames_to_remove = []

            # iterate files in the container path and add them to the tarball
            with tarfile.open(tarball_filename, mode="w") as tarball:
                for filename in sorted(os.listdir(full_container_path)):
                    full_filename = os.path.join(full_container_path, filename)
                    tarball.add(
                        full_filename,
                        arcname=os.path.join(container_path, filename),
                        recursive=False
                    )
                    filenames_to_remove.append(full_filename)

                # ensure the right number of files are now in the tarball
                if len(tarball.getmembers()) != len(os.listdir(full_container_path)):
                    raise ValueError(f"tarball {tarball_filename} contains different number of files than container path")

            # iterate files again and delete them
            for full_filename in filenames_to_remove:
                os.remove(full_filename)
            os.rmdir(full_container_path)


        self._is_tarball = True
        return True
