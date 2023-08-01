import os

from .item import Item


class Group:
    def __init__(self, index, identifier, parent=None, is_tarball=None):
        self.identifier = str(identifier)
        self.index = index
        self.parent = parent

        # determine min and max from index dimensions and identifier
        group_name = identifier.replace("/", "")
        self.bucket_size = self.index.base ** self.index.dimensions[0]
        self.bucket_min = int(group_name) * self.bucket_size
        self.bucket_max = self.bucket_min + self.bucket_size

        self._is_full = False
        self._is_tarball = is_tarball
        self._tarball_filename = None
        self._items = dict()

        if self._is_tarball is True:
            for idx in range(self.bucket_min, self.bucket_max):
                self._items[str(idx)] = Item(self, str(idx))

    def add_item(self, identifier):
        identifier = str(identifier)
        self._items[identifier] = Item(self, identifier)

    def get_item(self, identifier):
        identifier = str(identifier)
        if self.exists(identifier):
            return self.items[str(identifier)]
        else:
            raise ValueError(f"{identifier} not found in {self}")

    @property
    def is_full(self):
        return self._is_full

    @property
    def is_tarball(self):
        if self._is_tarball is None:
            self._is_tarball = os.path.isfile(self.path + ".tgz")
        return self._is_tarball

    @property
    def uri(self):
        if self.parent:
            return os.path.join(self.parent.path, self.identifier)
        else:
            return self.identifier

    @property
    def path(self):
        return os.path.join(self.index.path, self.uri)

    @property
    def min(self):
        return self.items[next(iter(sorted(self.items)))].identifier

    @property
    def max(self):
        return self.items[next(reversed(sorted(self.items)))].identifier

    @property
    def items(self):
        return self._items

    def __repr__(self):
        return self.identifier

    def exists(self, identifier):
        identifier = str(identifier)
        return identifier in self._items
