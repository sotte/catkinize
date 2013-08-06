#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys

from handle_manifest import handle_manifest
from utils import is_valid_version


if __name__ == "__main__":
    # TODO user arsparser
    package_path = sys.argv[1]
    package_name = sys.argv[2]
    version = sys.argv[3]

    if not is_valid_version(version):
        print("%s is not a valid version" % version)
        sys.exit(-1)

    possible = (
        handle_manifest(package_path, version, dryrun=True) and
        # handle_cmake(package_path, version, dryrun=True) and
        # handle_make(package_path, version, dryrun=True)
        True
    )

    if not possible:
        print("Errors occured, aborting.")
        sys.exit(-1)

    if confirm("Continue? [y/n]", "y"):
        handle_manifest(package_path, version, dryrun=False)
        # handle_cmake(package_path, version, dryrun=False)
        # handle_make(package_path, version, dryrun=False)

    else:
        print("You aborted catkinizing.")
