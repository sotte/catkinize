"""
TODO write doc

TODO Extract all doctest to proper unittests.
"""

##############################################################################
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
  <description>
    %(description)s
  </description>
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
# MAIN LOGIC
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
    print()

    # create manifest_xml_str
    package_xml_str = create_package_xml_str(fields)

    # writing package.xml
    print("writing package.xml...")
    if not dryrun:
        with open(package_xml_path, "w") as f:
            f.write(package_xml_str)
    print("Done")

    return True


def create_package_xml_str(fields):
    """Create the xml_str from the given fields dict."""
    subs = {
        'maintainers_part': make_section('maintainer', fields["maintainers"]),
        'licenses_part': make_section("license", fields["licenses"]),
        'bugtracker_part': make_bugtrackre_section(fields["bugtracker_url"]),
        'authors_part': make_section('author', fields["authors"]),
        'build_depends_part': make_section('build_depend', fields["depends"]),
        'run_depends_part': make_section('run_depend', fields["depends"]),
        'test_depends_part': make_section_commented("test_depend", fields["depends"]),
        # TODO make_section('replace', fields["replaces"])
        'replaces_part': "",
        # TODO make_section('conflict', fields["conflicts"])
        'conflicts_part': "",
        'version': fields["version"],
        'package_name': fields["package_name"],
        'description': fields["description"],
        'website_url': fields["website_url"],
        # TODO "metapackage" # TODO "architecture_independent
        'exports_part': make_exports_section( fields["exports"], False,  False),
    }
    return PACKAGE_TEMPLATE % subs


def get_fields_from_manifest(manifest_xml_path):
    """Extract all fields from the manifest.xml and return a dict with the
    extracted fields.
    """

    with open(manifest_xml_path) as f:
        manifest_str = f.read()
    manifest = ET.XML(manifest_str)

    # collect all fields
    fields = {
        "description": get_descrpition(manifest),
        "authors": get_authors_field(manifest),
        "licenses": get_licenses(manifest),
        "website_url": get_website_url(manifest),
        "maintainers": get_maintainers(manifest),
        "depends": get_depend(manifest),
        "exports": get_exports(manifest),
        "bugtracker_url": "",
    }
    return fields


##############################################################################
# Get fields from manifest.xml
##############################################################################
def get_exports(manifest):
    export_tags = xml_lib.xml_find(manifest, 'export').getchildren()
    return [(e.tag, e.attrib) for e in export_tags]


def get_depend(manifest):
    depend_tags = manifest.findall('depend')
    return [d.attrib['package'] for d in depend_tags]


def get_maintainers(manifest):
    authors = get_authors_field(manifest)
    result = [
        (author, {'email': ''})
        if isinstance(author, basestring)
        else author for author in authors
    ]
    return result


def get_website_url(manifest):
    return xml_lib.xml_find(manifest, 'url').text


def get_licenses(manifest):
    licenses_str = xml_lib.xml_find(manifest, 'license').text
    return SPACE_COMMA_RE.split(licenses_str)


def get_descrpition(manifest):
    return xml_lib.xml_find(manifest, 'description').text.strip()


def get_authors_field(manifest):
    """Extract author names and email addresses from free-form text in the
    <author> tag of manifest.xml.

    TODO fix unittests
    #>>> get_authors_field('Alice/alice@somewhere.bar, Bob')
    #[('Alice', {'email': 'alice@somewhere.bar'}), 'Bob']
    #>>> get_authors_field(None)
    #[]
    """
    authors_str = xml_lib.xml_find(manifest, 'author').text
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
# Make special section in the manifest.xml
##############################################################################
def make_bugtrackre_section(bugtracker_url):
    """Make the bugtracker section.

    >>> make_bugtrackre_section("www.ros.org")
    '<url type="bugtracker">www.ros.org</url>'
    >>> make_bugtrackre_section("")
    '<!-- <url type="bugtracker"></url> -->'
    """
    result = '<url type="bugtracker">%s</url>' % bugtracker_url
    if bugtracker_url == "":
        result = comment_out(result)
    return result


def make_exports_section(exports, architecture_independent, metapackage):
    """Make the export section."""
    parts = [make_empty_tag(name, attrs_dict)
             for name, attrs_dict in exports]
    if architecture_independent:
        parts.append('<architecture_independent/>')
    if metapackage:
        parts.append('<metapackage/>')
    parts = [indent(p, 2) for p in parts]
    return '\n'.join(parts)


##############################################################################
# XML formating
# TODO why don't we use the xml package to create the xml files?
##############################################################################
def make_section(tag_name, rows):
    r"""Make a string in XML format for a section with a given tag name.

    >>> make_section("test_depend", ["std_msgs"])
    '  <test_depend>std_msgs</test_depend>'
    >>> make_section("test_depend", ["std_msgs", "geo_msgs"])
    '  <test_depend>std_msgs</test_depend>\n  <test_depend>geo_msgs</test_depend>'
    """
    return '\n'.join(indent(make_tag_from_row(tag_name, row)) for row in rows)


def make_section_commented(tag_name, rows):
    r"""Make a string in XML format for a section with a given tag name and
    comment out each section.
    >>> make_section_commented("test_depend", ["std_msgs"])
    '  <!-- <test_depend>std_msgs</test_depend> -->'
    >>> make_section_commented("test_depend", ["std_msgs", "geo_msgs"])
    '  <!-- <test_depend>std_msgs</test_depend> -->\n  <!-- <test_depend>geo_msgs</test_depend> -->'
    """
    return '\n'.join(indent(comment_out(make_tag_from_row(tag_name, row)))
                     for row in rows)


def make_tag_from_row(name, row):
    """Make an XML tag from a row.

    >>> make_tag_from_row('foo', 'bar')
    '<foo>bar</foo>'
    >>> make_tag_from_row('foo', ('bar', dict(baz='buzz')))
    '<foo baz="buzz">bar</foo>'
    """
    if isinstance(row, basestring):
        return make_tag(name, attrs_dict={}, contents=row)
    if isinstance(row, tuple):
        return make_tag(name, attrs_dict=row[1], contents=row[0])


def comment_out(xml):
    return '<!-- %s -->' % xml


def dict_to_attrs(values):
    """Convert a dictionary to a string containing attributes in XML format."""
    return ' '.join('%s="%s"' % (k, v) for k, v in values.items())


def make_tag(name, attrs_dict, contents):
    return '<%s>%s</%s>' % (space_join([name, dict_to_attrs(attrs_dict)]),
                            contents,
                            name)


def make_empty_tag(name, attrs_dict):
    return '<%s/>' % space_join([name, dict_to_attrs(attrs_dict)])


def space_join(words):
    return ' '.join(w for w in words if w)


def indent(strg, amount=1):
    return (amount * '  ') + strg


##############################################################################
# PATH and FILE related functions
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
