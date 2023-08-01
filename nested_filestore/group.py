import os

from .item import Item


class Group:
    def __init__(self, index, identifier, parent=None, is_tarball=None):
        self.identifier = identifier
        self.index = index
        self.parent = parent

        self._is_full = False
        self._tarball_filename = None
        self._items = dict()

        if is_tarball is True:
            self._is_tarball = True
            group_name = identifier.replace("/", "")

            # determine min and max from index dimensions and identifier
            bucket_size = self.index.base ^ self.index.dimensions[0]
            min_bucket = int(group_name) * bucket_size - 1
            max_bucket = min_bucket + bucket_size - 1

            for idx in range(min_bucket, max_bucket):
                self._items[str(idx)] = Item(self, str(idx))
        else:
            self._is_tarball = None

    def add_item(self, identifier):
        self._items[str(identifier)] = Item(self, str(identifier))

    def get_item(self, identifier):
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
        return str(identifier) in self._items
