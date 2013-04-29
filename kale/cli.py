#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cli.py
=========

Description: A command line tool for adding boilerplate licensing to your open
source projects.

Author: Jennifer Hamon (jhamon@gmail.com)

License: MIT (see LICENSE)
"""

import argparse
import sys
import datetime
import os
import re
from headers import Header
from utils import install_license, update_readme



class Licme(object):
    """ main class for cli licensing tool """

    def __init__(self):
        self.parser = self.setup_parser()
        self.cwd = os.getcwd()

    def run(self):
        self.args = self.parser.parse_args()
        self.validate_cli_arguments()
        self.setup_license_details()
        self.check_if_already_has_license()

        if self.args.r:
            update_readme()

        if self.args.remove_headers:
            Header.install_headers()
            self.args.remove_headers = False

        install_license()
        Header.install_headers()

    def exit(self, *bad=None):
        if bad:
            print 'The operation was not completed successfully.'
            sys.exit(1)
        else:
            sys.exit(0)


    def setup_parser(self):
        """
        Returns argparse instance, with command line options configured
        """

        parser = argparse.ArgumentParser(prog="LICME",
                description="""
            LICME is designed to help take the pain out of boilerplate licensing.
            You specify the copyright holder and the name of a popular open
            source license, and licme will create the appropriate LICENSE file
            in your project directory.  Copyright and license information will be
            appended to your existing README file, or one will be created for you
            if it does not already exist.

        BASIC EXAMPLE

            $ licme gpl3 "Free Software Foundation, Inc." "Emacs 24"
            $ licme mit "Jennifer Hamon" "Licme"

                """,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="""
        SUPPORTED LICENSES
            Licme supports many popular and interesting software licenses.

            Popular:
                    artistic  Perl Foudation Artistic License, Version 2.0
                    agpl3     GNU Affero General Public License, Version 3.0
                    apache2   Apache License, Version 2.0
                    bsd3      BSD 3-Clause License
                    bsd2      BSD 2-Clause License
                    gpl2      GNU General Public License, Version 2.0
                    gpl3      GNU General Public License, Version 3.0
                    lgpl3     GNU Lesser General Public License,Version 3.0
                    mit       MIT License
                    mpl2      Mozilla Public License, Version 2.0

            Old and Deprecated:
                    gpl1      GNU General Public License, Version 1.0
                    lgpl2     GNU Lesser General Public License, Version 2.0
                    lgpl2.1   GNU Lesser General Public License, Version 2.1
                    mpl1.1    Mozilla Public License, Version 1.1

            Other:
                    crapl       Community Research and Academic Programming License
                    unlicense   Release code to public domain.  See unlicense.org.
                    wtfpl       Do What the Fuck You Want To Public License, Version 2



        CONTRIBUTING
            If there is another license you would like to see included in licme,
            please submit a pull request at http://www.github.com/jhamon/licme
                """)

        parser.add_argument('license',
            help="specify the license you would like to use.")
        parser.add_argument('copyright_holder',
            help="specify the author or copyright holder.",
            type=str)
        parser.add_argument('program_name', help="specify the name of your software")
        parser.add_argument('-y', '--year',
            help="specify copyright year other than the present year",
            dest="year",
            default=str(datetime.date.today().year))
        parser.add_argument('-n', '--no-readme',
            help="use this option to prevent changes to the README file.",
            action="store_false",
            default=True,
            dest="r")
        parser.add_argument('-a', '--add-sourcefile-headers',
            help='add short copyright and license notice to individual source files',
            action='store_true',
            default=False,
            dest='add_headers')
        parser.add_argument('-r', '--remove-sourcefile-headers',
            help='remove in-file license notices previously applied by licme',
            action='store_true',
            default=False,
            dest='remove_headers')
        parser.add_argument('-q', '--quiet',
            help='supress some informational output',
            action='store_true',
            default=False,
            dest='q')

        return parser

    def setup_license_details(self):
        """
        Defines the following:
            self.longname => string
            self.recommend_infile => boolean
            self.license_filename => string
        """

        # This is a list of all licenses whose usage guidelines recommend a copyright
        # and brief licensing notice be present in each file.
        recommend_infile = 'mpl1.1 lgpl2.1 gpl1 gpl2 gpl3 mpl2 agpl3 apache2 artistic'.split(' ')

        # Some licenses have special recommendations for the name of the file in which
        # the full license text is stored.  In practice it shouldn't matter, but it is
        # good to follow tradition. The prefered name of the license file is stored in a
        # dictionary license_filenames, keyed by license name.
        filename_LICENSE = 'mit agpl3 apache2 bsd3 bsd2 mpl2 crapl wtfpl'.split(' ')
        filename_COPYING = 'gpl1 gpl2 gpl3'.split(' ')
        filename_COPYINGLESSER = 'lgpl2.1 lgpl2'.split(' ')
        filename_UNLICENSE = ['unlicense']
        license_filenames = {key:'LICENSE' for key in filename_LICENSE}
        license_filenames.update({key:'COPYING' for key in filename_COPYING})
        license_filenames.update({key:'COPYING.LESSER' for key in filename_COPYINGLESSER})
        license_filenames.update({key:'UNLICENSE' for key in filename_UNLICENSE})

        # To fill some templates, we need to know the "long" version of each filename.
        # Those are also stored in a dictionary.
        longnames = {}
        longnames['wtfpl'] = 'Do What the Fuck You Want To Public License, Version 2'
        longnames['unlicense'] = 'Unlicense'
        longnames['artistic'] = 'Perl Foundation Artistic License, Version 2.0'
        longnames['agpl3'] = 'GNU Affero General Public License, Version 3.0'
        longnames['apache2'] = 'Apache License 2.0'
        longnames['bsd3'] = 'BSD 3-Clause License'
        longnames['bsd2'] = 'BSD 2-Clause License'
        longnames['gpl2'] = 'GNU General Public License, Version 2.0'
        longnames['gpl3'] = 'GNU General Public License, Version 3.0'
        longnames['lgpl3'] = 'GNU Lesser General Public License, Version 3.0'
        longnames['lgpl2'] = 'GNU Lesser General Public License, Version 2.0'
        longnames['lgpl2.1'] = 'GNU Lesser General Public License, Version 2.1'
        longnames['mit'] = 'MIT License'
        longnames['mpl2'] = 'Mozilla Public License, Version 2.0'
        longnames['mpl1.1'] = 'Mozilla Public License, Version 1.1'
        longnames['gpl1'] = 'GNU General Public License, Version 1.0'
        longnames['crapl'] = 'Community Research and Academic Programming License'

        self.longname = longnames[self.license]
        self.recommend_infile = self.license in recommend_infile
        self.license_filename = license_filenames[self.license]

    def validate_cli_arguments(self):
        """
        Checks for obvious conflicts in options given by the user.  If any are
        found, stops execution.
        """
        help = 'Try -h for help information.'
        if args.license not in LIC_DETAILS.keys():
            print 'You have entered an invalid license name.'
            print help
            self.exit(bad=True)
        if args.remove_headers and args.add_headers:
            print 'You have used conflicting header options.'
            print help
            self.exit(bad=True)

    def check_if_already_has_license(self):
        """ returns boolean value indicating whether there is
        already a file in the current working directory that has
        'license' or similar in the filename
        """
        common_license_filenames = ['license',
                                    'copying',
                                    'unlicense',
                                    'copying.lesser',
                                    'license.txt',
                                    'unlicense.txt',
                                    'copying.txt']
        cwd_files = os.listdir(self.cwd)
        possible_licenses = [x for x in cwd_files if x.lower() in
                common_license_filenames]
        if len(possible_licenses) != 0:
            print 'This repository appears to contain license information already.'
            print 'If you would like to apply a new license using licme, first'
            print 'remove any license files such as LICENSE, COPYING, or UNLICENSE.'
            if not self.args.q:
                print '\n  Conflicting files: \n    {0}'.format('\n    '.join(possible_licenses))
            print '\nNo changes have been made.'
            self.exit(bad=True)
        else:
            return False

if __name__ == '__main__':
    my_licme = Licme()
    my_listme.run()
