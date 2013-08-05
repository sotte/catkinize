from __future__ import print_function

import sys
from handle_manifest import handle_manifest


if __name__ == "__main__":
    # TODO user arsparser
    version = sys.args[1]
    if not is_valid_version(version):
        print("not a valid version")
        sys.exit(-1)

    package_path = sys.args[2]

    # possible = handle_manifest(dryrun=True) and handle_cmake(dryrun=True) and handle_make(dryrun=True)

    possible = (handle_manifest(package_path, version, dryrun=True) and
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
