"""
Converting CMake is more annoying than converting manifest.xml.

The previous version took each cmake command and converted it, see
`conversions` and `manual_conversions`.

The denpendencies from the manifest files were added in the appropiate
positions. The location of most cmake commands was not really edited.

In the end you had a file with lots of TODOs and comments.

Maybe it would be better to have a cleaner version of the catkinized cmake
file. The "template approach" from the manifest conversion really makes clear
what happens during the conversion. Maybe we can adopt this approach.

Open questions:
    - what can we put between `find_packages` and `_catkinize_package`?
    - what MUST we put between `find_packages` and `_catkinize_package`?
    - what MUST be put after `_catkinize_package`?
"""

##############################################################################
from __future__ import print_function
import os
import re

import utils


##############################################################################
CMAKE_TEMPLATE = """\
# Catkin CMake Standard:
# http://www.ros.org/doc/groovy/api/catkin/html/user_guide/user_guide.html
cmake_minimum_required(VERSION 2.8.3)
project(%(project_name)s)

%(find_packages)s

%(msg_srv_section)s

%(before_catkin_package)s

catkin_package(
  INCLUDE_DIRS %(include)s
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS %(dependencies)s
)

%(after_catkin_package)s
"""

##############################################################################
MSG_SRV_SECTION = """\
%(comment_msg)sadd_message_files(DIRECTORY %(msg_dir)s FILES %(msg_files)s)
%(comment_srv)sadd_service_files(DIRECTORY %(srv_dir)s FILES %(srv_files)s)

%(comment_gen)sgenerate_messages(DEPENDENCIES %(files)s)
"""


##############################################################################
def handle_cmake(package_path, version, dryrun=True):
    """TODO add doc"""

    package_name = utils.get_package_name(package_path)
    cmake_path = utils.get_cmake_path(package_path)
    manifest_xml_path = utils.get_manifest_xml_path(package_path)

    # GUARDS
    if not os.path.exists(manifest_xml_path):
        print("%s does not exist. Aborting." % manifest_xml_path)
        return False

    if not os.path.exists(cmake_path):
        print("%s does not exist. Aborting." % cmake_path)
        return False

    fields = {}
    # get dependencies from the manifest file
    # we need to add the dependencies in multiple parts in the cmake file
    fields["dependencies"] = get_dependencies(manifest_xml_path)
    fields["package_name"] = package_name

    # read the cmake file
    with open(cmake_path, 'r') as f:
        cmake_content = f.read()

    fields["cmake_commands"] = FUNCALL_PATTERN.split(cmake_content)

    cmake_new = get_cmake_new(fields)

    return True


##############################################################################
def get_cmake_new(fields):
    raise NotImplementedError()


def get_dependencies(manifest_xml_path):
    raise NotImplementedError()








































