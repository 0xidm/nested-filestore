import os


class Item:
    def __init__(self, group, identifier):
        self.group = group
        self.identifier = str(identifier)
        self._filestore_item_path = None

    def get(self):
        if self.inside_tarball:
            return self._get_from_tarball()
        else:
            return self._get_from_filesystem()

    def _get_from_filesystem(self):
        return open(self.filestore_item_path, "rb")

    def _get_from_tarball(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.identifier

    @property
    def filestore_item_path(self):
        if self._filestore_item_path is None:
            self._filestore_item_path = os.path.join(self.group.filestore_path, self.identifier)
        return self._filestore_item_path

    @property
    def inside_tarball(self):
        return self.group.is_tarball
