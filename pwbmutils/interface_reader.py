"""Contains luigi class for interfacing with external component interfaces.
"""

__author__ = "Nick Janetos"
__copyright__ = "2018 Penn Wharton Budget Model"

from os import makedirs
from os.path import exists, join
from shutil import copyfile
import sys
from distutils.dir_util import copy_tree

import luigi
from .pwbm_task import PWBMTask

# pylint: disable=E1136


class InterfaceReader(PWBMTask):
    """Cached requested interfaces locally.
    """

    interface_info = luigi.DictParameter(
        description="Dictionary of information about the interface")

    filename = luigi.Parameter(
        default=None,
        description="Optional filename to get from interface")

    path_to_hpcc = luigi.Parameter(
        default=r"\\hpcc-ppi.wharton.upenn.edu\ppi" \
            if sys.platform == "win32" \
            else "/home/mnt/projects/ppi",
        description="Path to the HPCC.")

    def output(self):

        version = self.interface_info["version"]
        component = self.interface_info["component"]
        interface = self.interface_info["interface"]

        server_location = join(
            self.path_to_hpcc,
            component,
            "Interfaces",
            version,
            interface
        )

        if self.cache_location is not None:
            destination_folder = join(
                self.cache_location,
                component,
                "Interfaces",
                version,
                interface
            )

            if self.filename is None:
                return luigi.LocalTarget(join(destination_folder))
            else:
                return luigi.LocalTarget(join(destination_folder, self.filename))

        else:

            if self.filename is None:
                return luigi.LocalTarget(join(server_location))
            else:
                return luigi.LocalTarget(join(server_location, self.filename))


    def requires(self):
        # nothing, will fail if external file does not exist
        return []

    def work(self):

        version = self.interface_info["version"]
        component = self.interface_info["component"]
        interface = self.interface_info["interface"]

        server_location = join(
            self.path_to_hpcc,
            component,
            "Interfaces",
            version,
            interface
        )

        if self.cache_location is not None:

            destination_folder = join(
                self.cache_location,
                component,
                "Interfaces",
                version,
                interface
            )

            if not exists(destination_folder):
                makedirs(destination_folder)

            if self.filename is not None:

                file_location = join(
                    server_location,
                    self.filename
                )

                copyfile(file_location, join(destination_folder, self.filename))

            else:

                copy_tree(server_location, destination_folder)

        else:
            # do nothing if no copy requested
            pass