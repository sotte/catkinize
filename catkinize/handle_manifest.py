from __future__ import print_function

import os


##############################################################################
# The final package is going to look like the PACKAGE_TEMPLATE
PACKAGE_TEMPLATE = """\
<package>
  <name>%(package_name)s</name>
  <version>%(version)s</version>
  <description>%(description)s</description>
%(maintainers_part)s

%(licenses_part)s

  <url type="website">%(website_url)s</url>
%(bugtracker_part)s

%(authors_part)s

  <!-- Dependencies which this package needs to build itself. -->
  <buildtool_depend>catkin</buildtool_depend>

  <!-- Dependencies needed to compile this package. -->
%(build_depends_part)s

  <!-- Dependencies needed after this package is compiled. -->
%(run_depends_part)s

  <!-- Dependencies needed only for running tests. -->
%(test_depends_part)s

%(replaces_part)s
%(conflicts_part)s

  <export>
%(exports_part)s
  </export>
</package>
"""


##############################################################################
def handle_manifest(package_path, version, dryrun=True):
    """Convert the package.xml to a catkinized manifest.xml file.

    TODO: arguments
    """
    package_name = get_package_name(package_path)
    manifest_xml_path = get_manifest_path(package_path)
    package_xml_path = get_package_xml_path(package_path)

    os.path.basename
    # guards
    if not os.path.exists(manifest_xml_path):
        print("manifest.xml does not exits")
        return False

    if os.path.exists(package_xml_path):
        print("package.xml does already exist. Aborting.")
        return False

    # get all fields
    with open(manifest_xml_path) as f:
        fields = get_fields_from_manifest(f)
    fields["package_name"] = package_name
    fields["version"] = version

    # create manifest_xml_str
    print("package.xml:")
    manifest_xml_str = create_package_xml_str(fields)
    print(manifest_xml_str)

    # writing package.xml
    print("writing package.xml...")
    if not dryrun:
        with open(manifest_xml_path, "w") as f:
            f.write(manifest_xml_str)
    print("Done")

    return True


##############################################################################
def get_manifest_path(package_path):
    pass


def get_package_xml_path(package_path):
    pass
