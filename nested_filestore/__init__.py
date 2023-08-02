import os
import re
import glob
import shutil


from .index import Index


class NestedFilestore:
    """
    NestedFilestore is a filestore that stores files in a nested directory structure.
    This is a thin wrapper around the Index class.
    """

    def __init__(self, root_path, hierarchy_order, pad_character="0", base=10):
        "args are root filesystem path, and order of hierarchy starting from leaf back to the root"
        self.index = Index(
            path=root_path,
            dimensions=hierarchy_order,
            pad_character=pad_character,
            base=base,
        )

    def exists(self, identifier):
        "does the specified identifier exist as a file? If it exists, return True"
        return self.index.exists(identifier)
    
    def put(self, identifier, filename=None, filehandle=False, move=False, overwrite=False):
        "given the path to an existing file, and given an identifier, copy the file to the file store and put it in the right place, creating directories as needed."
        return self.index.put(
            identifier,
            filename=filename,
            filehandle=filehandle,
            move=move,
            overwrite=overwrite
        )

    def writer(self, identifier, overwrite=False):
        "given an identifier, return a writable file handle pointing to the file UNLESS it exists"
        return self.index.put(
            identifier,
            filehandle=True,
            overwrite=overwrite
        )
    
    def get(self, identifier):
        "given an identifier, return a file handle pointing to the file if it exists"
        return self.index.get(identifier).open()

    def ingest_filesystem(self, filestore_path):
        "low-level filesystem scan of filestore_path for .bin files, which it imports"

        file_list = glob.glob(os.path.join(filestore_path, "**/*.bin"), recursive=True)
        for filename in sorted(file_list):
            match = re.search(r'([^/]+).bin', filename)
            if match:
                index = int(match.group(1))
                self.put(index, filename=filename, move=True)
