import os

from .item import Item


class Group:
    def __init__(self, index, identifier, is_tarball=None):
        self.identifier = str(identifier)
        self.index = index

        # determine min and max from index dimensions and identifier
        group_name = identifier.replace("/", "")
        self._bucket_size = self.index.base ** self.index.dimensions[0]
        self._bucket_min = int(group_name) * self._bucket_size
        self._bucket_max = self._bucket_min + self._bucket_size

        self._is_full = False
        self._is_tarball = is_tarball
        self._items = dict()

    def add(self, identifier):
        identifier = str(identifier)
        self._items[identifier] = Item(self, identifier)

    def get(self, identifier):
        identifier = str(identifier)
        if self.is_tarball:
            if identifier not in self._items:
                self._items[identifier] = Item(self, identifier)
            return self._items[identifier]
        elif self.exists(identifier):
            return self.items[identifier]
        else:
            raise ValueError(f"{identifier} not found in {self}")

    @property
    def is_full(self):
        return self._is_full

    @property
    def is_tarball(self):
        if self._is_tarball is None:
            self._is_tarball = os.path.isfile(self._path_tgz)
        return self._is_tarball

    @property
    def uri(self):
        return self.identifier

    @property
    def path(self):
        if self._is_tarball:
            return self._path_tgz
        else:
            return self._path_dir

    @property
    def _path_dir(self):
        return f"{self.index.path}{self.uri}"

    @property
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

    def exists(self, identifier):
        if self.is_tarball:
            return True
        identifier = str(identifier)
        return identifier in self._items
