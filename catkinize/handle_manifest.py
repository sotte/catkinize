from __future__ import print_function

# standard library imports
import os
import re

# related third party imports
import xml.etree.ElementTree as ET

# local application/library specific imports
from catkinize import xml_lib


##############################################################################
SPACE_COMMA_RE = re.compile(r',\s*')

# The final package is going to look like the PACKAGE_TEMPLATE
PACKAGE_TEMPLATE = """\
<package>
  <name>%(package_name)s</name>
  <version>%(version)s</version>
  <description>%(description)s</description>
%(maintainers_part)s
%(authors_part)s
%(licenses_part)s
  <url type="website">%(website_url)s</url>
%(bugtracker_part)s


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
    manifest_xml_path = get_packg_xml_path(package_path)
    package_xml_path = get_package_xml_path(package_path)

    # GUARDS
    if not os.path.exists(manifest_xml_path):
        print("manifest.xml does not exits")
        return False

    if os.path.exists(package_xml_path):
        print("package.xml does already exist. Aborting.")
        return False

    # get all fields
    fields = get_fields_from_manifest(manifest_xml_path)
    fields["package_name"] = package_name
    fields["version"] = version
    for k in fields:
        print("%s --> %s" % (k, fields[k]))
    return False

    # create manifest_xml_str
    print("package.xml:")
    manifest_xml_str = create_package_xml_str(fields)

    # writing package.xml
    print("writing package.xml...")
    if not dryrun:
        with open(manifest_xml_path, "w") as f:
            f.write(manifest_xml_str)
    print("Done")

    return True


##############################################################################
def get_fields_from_manifest(manifest_xml_path):

    with open(manifest_xml_path) as f:
        manifest_str = f.read()
    manifest = ET.XML(manifest_str)

    # collect all fields
    fields = {}

    fields["description"] = xml_lib.xml_find(manifest, 'description').text.strip()

    authors_str = xml_lib.xml_find(manifest, 'author').text
    fields["authors"] = get_authors_field(authors_str)

    licenses_str = xml_lib.xml_find(manifest, 'license').text
    fields["licenses"] = SPACE_COMMA_RE.split(licenses_str)

    fields["website_url"] = xml_lib.xml_find(manifest, 'url').text

    fields["maintainers"] = [
        (author, {'email': ''})
        if isinstance(author, basestring)
        else author for author in fields["authors"]]

    depend_tags = manifest.findall('depend')
    fields["depends"] = [d.attrib['package'] for d in depend_tags]

    export_tags = xml_lib.xml_find(manifest, 'export').getchildren()
    fields["exports"] = [(e.tag, e.attrib) for e in export_tags]

    return fields


def get_authors_field(authors_str):
    """Extract author names and email addresses from free-form text in the
    <author> tag of manifest.xml.

    >>> get_authors_field('Alice/alice@somewhere.bar, Bob')
    [('Alice', {'email': 'alice@somewhere.bar'}), 'Bob']
    >>> get_authors_field(None)
    []
    """
    if authors_str is None:
        return []

    authors = []
    for s in SPACE_COMMA_RE.split(authors_str):
        parts = s.split('/')
        if len(parts) == 1:
            authors.append(parts[0])
        elif len(parts) == 2:
            pair = (parts[0], dict(email=parts[1]))
            authors.append(pair)
    return authors


##############################################################################
# Utility functions
##############################################################################
def get_package_name(package_path):
    """Return the package name for the given package_path.

    >>> get_package_name("some/path/to/a/package/XYZ_package")
    'XYZ_package'
    >>> get_package_name("XYZ_package")
    'XYZ_package'
    """
    return os.path.basename(os.path.abspath(package_path))


def get_packg_xml_path(package_path):
    """Return the path to the manifest.xml file for the given package_path.

    >>> get_packg_xml_path("some/path/to/a/package/XYZ_package")
    'some/path/to/a/package/XYZ_package/manifest.xml'
    >>> get_packg_xml_path("XYZ_package")
    'XYZ_package/manifest.xml'
    """
    return os.path.join(package_path, "manifest.xml")


def get_package_xml_path(package_path):
    """Return the path to the package.xml file for the given package_path.

    >>> get_package_xml_path("some/path/to/a/package/XYZ_package")
    'some/path/to/a/package/XYZ_package/package.xml'
    >>> get_package_xml_path("XYZ_package")
    'XYZ_package/package.xml'
    """
    return os.path.join(package_path, "package.xml")
