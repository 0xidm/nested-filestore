import os


class Item:
    def __init__(self, group, identifier):
        self.group = group
        self.identifier = str(identifier)

    def open(self):
        if self.inside_tarball:
            tarball = self.group._ratarmount
            info = tarball.getFileInfo(f"{self.uri}.bin")
            return tarball.open(info)
        else:
            return open(self.path, "rb")

    def __repr__(self):
        return self.identifier

    @property
    def inside_tarball(self):
        return self.group.is_tarball

    @property
    def uri(self):
        return f"{self.group.uri}/{self.identifier}"
    
    @property
    def path(self):
        return f"{self.group._path_dir}/{self.identifier}.bin"
