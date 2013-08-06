from __future__ import print_function
import os

import utils


##############################################################################
DEFAULT_MAKEFILE = "include $(shell rospack find mk)/cmake.mk"
DEFAULT_MAKEFILE_STACK = "include $(shell rospack find mk)/cmake_stack.mk"


##############################################################################
def handle_make(package_path,  dryrun=True):
    """Handle the Makefile of the package, i.e., backup the makefile if it has
    the content of the default Makefiles.

    :package_path: path of the package
    :dryrun: if dryrun == True then don't perform any file operation
    :returns: True iff all actions could be performed
    """

    makefile_path = utils.get_makefile_path(package_path)

    # GUARDS
    if not os.path.exists(makefile_path):
        print("%s does not exits" % makefile_path)
        return False

    makefile_str = open(makefile_path).read()
    print(makefile_str)
    if makefile_str not in [DEFAULT_MAKEFILE, DEFAULT_MAKEFILE_STACK]:
        print("The existing Makefile has custom changes. Nothing is done with "
              "it")
        return False

    # Backup old Makefile
    makefile_backup_path = makefile_path + '.backup'
    print("Backing up %s to %s." % (makefile_path, makefile_backup_path))
    if not dryrun:
        os.rename(makefile_path, makefile_backup_path)
    print("Done")

    return True
