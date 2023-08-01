import os
import re
import glob
import logging
import datetime

from .group import Group


class Index:
    def __init__(self, path, dimensions, pad_character="0", base=10, sync=True):
        self.path = path
        self.dimensions = dimensions
        self.base = 10
        self.pad_character = pad_character
        self.groups = dict()
        if sync:
            self.sync()

    def get_group(self, group_uri):
        "given a group uri, return the group object"
        if group_uri in self.groups:
            return self.groups[group_uri]
        else:
            raise ValueError(f"{group_uri} not found in {self}")
    
    def get(self, identifier):
        "given an identifier, return the item object"
        identifier = str(identifier)
        group_uri = self.which_group(identifier)
        try:
            group = self.get_group(group_uri)
            return group.get(identifier)
        except ValueError:
            raise ValueError(f"{identifier} not found in {self}")
    
    def sync(self):
        "sync the index with the filesystem"

        # first locate .bin files
        # create a group from the path, as necessary
        # then create individual items
        for binfile in glob.glob(f'{self.path}/**/*.bin', recursive=True):
            binfile = binfile.replace(self.path, "")
            binfile = binfile.replace(".bin", "")
            identifier = os.path.basename(binfile)
            subdir = os.path.dirname(binfile)
            if subdir not in self.groups:
                self.groups[subdir] = Group(self, subdir)
            self.groups[subdir].add(identifier)

        # # then locate .tgz files
        for tarball in glob.glob(f'{self.path}/**/*.tgz', recursive=True):
            tarball = tarball.replace(self.path, "")
            tarball = tarball.replace(".tgz", "")
            if tarball not in self.groups:
                self.groups[tarball] = Group(self, tarball, is_tarball=True)

    def __repr__(self):
        return f"Index({self.path})"
    
    @property
    def min(self):
        min_group = self.groups[next(iter(sorted(self.groups)))]
        return min_group.min

    @property
    def max(self):
        max_group = self.groups[next(reversed(sorted(self.groups)))]
        return max_group.max

    def which_group(self, identifier):
        "based on the hierarchy order, return a tuple of the path components for the given identifier"
        identifier_str = str(identifier)

        # get the leaf id, which is the last N digits of the identifier
        leaf_order = self.dimensions[0]

        # remove the right-most leaf_order digits from the string
        identifier_str = identifier_str[:-leaf_order]

        subdirs = []
        for level in self.dimensions[1:]:
            # get the subdir id, which is the last N digits of the identifier
            subdir_id = identifier_str[-level:]

            # pad the subdir id with the pad character if it is too short
            if len(subdir_id) < level:
                subdir_id = subdir_id.rjust(level, self.pad_character)
            subdirs.insert(0, subdir_id)

            # remove right-most level digits from the string
            identifier_str = identifier_str[:-level]

        return "/" + os.path.join(*subdirs)

    def exists(self, identifier):
        # determine which group should contain the item with the given identifier
        identifier = str(identifier)
        group_uri = self.which_group(identifier)
        try:
            group = self.get_group(group_uri)
            return group.exists(identifier)
        except ValueError:
            return False

    @property
    def missing(self):
        for idx in range(int(self.min), int(self.max)):
            if not self.exists(idx):
                yield idx
