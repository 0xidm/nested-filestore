#!/usr/bin/env python3

import os
import json
import random
import logging

import click

from nested_filestore.tarball import GzipTarballNestedFilestore


@click.group()
def cli():
    pass

@cli.command()
@click.argument('filestore', type=str)
def upgrade_to_tarball(filestore):
    "Upgrade a NestedFilestore to a TarballNestedFilestore"
    filestore = GzipTarballNestedFilestore(
        root_path=os.path.expanduser(filestore),
        hierarchy_order=[3, 3, 3],
    )
    filestore.tarball_scan()

@cli.command()
@click.argument('input_filestore', type=str)
@click.argument('output_filestore', type=str)
def ingest(input_filestore, output_filestore):
    "Import a NestedFilestore into a GzipTarballNestedFilestore"
    filestore = GzipTarballNestedFilestore(
        root_path=os.path.expanduser(output_filestore),
        hierarchy_order=[3, 3, 3],
    )
    filestore.ingest_filesystem(input_filestore)
    filestore.tarball_scan()

if __name__ == "__main__":
    # init_logger(level=os.getenv("LOG_LEVEL", "INFO"))
    cli()
