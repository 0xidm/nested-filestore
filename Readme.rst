Nested Filestore
================

This is a simple filestore that stores files in a nested directory structure.

Install
-------

.. code-block:: bash

   pip install "git+https://github.com/0xidm/nested-filestore"

Usage
-----

The following example creates a nested filestore in /tmp/files with 2 nested levels.
The leaf nodes will be grouped into containers containing 10^2 files each.
There will be subdirectories of 10^1 containers each.
Finally, the root node will be grouped into containers containing 10^1 files each.

.. code-block:: python

   filestore = NestedFilestore("/tmp/files", [2, 1, 1])
   filestore.put(0, "tests/data/12345678.bin")
   assert filestore.exists(0)
   with filestore.get(0) as f:
      print(f.read())

Online resources
----------------

- `Github repository <https://github.com/0xidm/nested-filestore>`_
- `Documentation <https://nested-filestore.readthedocs.org>`_
