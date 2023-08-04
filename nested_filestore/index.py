import os
import re
import glob
import shutil
import logging
import threading
import datetime

from functools import lru_cache

from .exceptions import GroupNotFullError
from .group import Group
from .item import Item


class Index:
    def __init__(self, path, dimensions, pad_character="0", base=10, sync=True):
        self.path = path
        self.dimensions = dimensions
        self.base = 10
        self.pad_character = pad_character
        self.groups = dict()
        self._mkdir_lock = threading.Lock()
        if sync:
            self.sync()

    def get_group(self, group_uri):
        "given a group uri, return the group object"
        if group_uri in self.groups:
            return self.groups[group_uri]
        else:
            raise ValueError(f"{group_uri} not found in {self}")

    def get(self, identifier:str):
        "given an identifier, return the item object"
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

        self.groups = dict(sorted(self.groups.items()))

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

    @lru_cache(maxsize=None)
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
        for idx in range(int(self.min), int(self.max) + 1):
            if not self.exists(idx):
                yield idx

    def put(self, identifier, filename=None, filehandle=False, move=False, overwrite=False):
        "given the path to an existing file, and given an identifier, copy the file to the file store and put it in the right place, creating directories as needed."

        if not overwrite and self.exists(identifier):
            raise ValueError(f"{identifier} already exists.")

        dst_group_uri = self.which_group(identifier)

        # if group does not already exist, create it
        if dst_group_uri not in self.groups:
            with self._mkdir_lock:
                self.groups[dst_group_uri] = Group(self, dst_group_uri)
                dst_group = self.groups[dst_group_uri]

                if dst_group.is_tarball:
                    # if group is inside a tarball, raise an error for now
                    raise ValueError(f"{identifier} is inside a tarball. Cannot put.")
                else:
                    # ensure the path exists if not tarball
                    os.makedirs(dst_group._path_dir, exist_ok=True)
        else:
            dst_group = self.groups[dst_group_uri]

        new_item = Item(dst_group, identifier)
        dst_group.add(new_item)

        if filehandle:
            return open(new_item.path, "wb")
        elif filename:
            if move:
                shutil.move(filename, new_item.path)
            else:
                shutil.copy(filename, new_item.path)
            return new_item
        else:
            raise ValueError("either filename or filehandle must be specified.")

    def compact(self):
        "given an identifier, try to compact the group its group, ignoring GroupNotFullError"
        for group_uri in self.groups:
            group = self.get_group(group_uri)
            group.compact()

    @property
    def is_valid(self):
        "check that the index is valid"
        return self.validate() is True

    def validate(self, raise_exception=False, debug=False):
        "check that the index is valid"
        for group_uri in self.groups:
            group = self.get_group(group_uri)
            validation_result = group.validate(
                raise_exception=raise_exception,
                debug=debug
            )
            group.close()
        return True
