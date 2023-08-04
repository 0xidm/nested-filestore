#!/usr/bin/env python3

import os
import json
import random
import logging

import click

from nested_filestore import NestedFilestore


@click.group()
def cli():
    pass

@cli.command()
@click.argument('filestore', type=str)
def upgrade_to_tarball(filestore):
    "Upgrade a NestedFilestore to a TarballNestedFilestore"
    filestore = NestedFilestore(
        root_path=os.path.expanduser(filestore),
        hierarchy_order=[3, 3, 3],
    )
    filestore.tarball_scan()

@cli.command()
@click.argument('filestore', type=str)
def validate(filestore):
    "Check the index for validity"
    filestore = NestedFilestore(
        root_path=os.path.expanduser(filestore),
        hierarchy_order=[3, 3, 3],
    )

    bad_groups = []
    for group_uri in filestore.index.groups:
        group = filestore.index.get_group(group_uri)
        validation_result = group.validate()
        group.close()
        if validation_result is True:
            print(f"{group_uri} valid")
        else:
            bad_groups.append(group_uri)
            print(f"{group_uri} invalid: {validation_result}")
    
    if len(bad_groups) > 0:
        print("Bad groups:")
        for group_uri in bad_groups:
            print(f"  {group_uri}")
    else:
        print("Index is valid")


@cli.command()
@click.argument('input_filestore', type=str)
@click.argument('output_filestore', type=str)
def ingest(input_filestore, output_filestore):
    "Import a NestedFilestore into a NestedFilestore"
    filestore = NestedFilestore(
        root_path=os.path.expanduser(output_filestore),
        hierarchy_order=[3, 3, 3],
    )
    filestore.ingest_filesystem(input_filestore)
    filestore.tarball_scan()

if __name__ == "__main__":
    # init_logger(level=os.getenv("LOG_LEVEL", "INFO"))
    cli()
