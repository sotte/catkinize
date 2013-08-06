import os
import re
import sys


##############################################################################
def is_valid_version(version):
    """Check if `version` is a valid version according to
    http://ros.org/reps/rep-0127.html#version
    """
    match = re.match(r'^\d+\.\d+\.\d+$', version)
    return match is not None


def confirm(msg, confirm_key):
    def _get_input(prompt):
        """Helper function to provide python2 + python3 compatible get_input"""
        if sys.hexversion > 0x03000000:
            return input(prompt)
        else:
            return raw_input(prompt)

    return _get_input(msg) == confirm_key


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


def get_makefile_path(package_path):
    """Return the path of the Makefile for the given package_path.

    >>> get_makefile_path("some/path/to/a/package/XYZ_package")
    'some/path/to/a/package/XYZ_package/Makefile'
    >>> get_makefile_path("XYZ_package")
    'XYZ_package/Makefile'
    """
    return os.path.join(package_path, "Makefile")


def get_package_path(package_path):
    """Return the path to the manifest.xml file for the given package_path.

    >>> get_package_path("some/path/to/a/package/XYZ_package")
    'some/path/to/a/package/XYZ_package/manifest.xml'
    >>> get_package_path("XYZ_package")
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
