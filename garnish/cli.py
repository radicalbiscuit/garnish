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
from header import Header
from utils import fill_template, exit, wrap_paragraphs
import pkg_resources
import textwrap
import logging

class Garnish(object):
    """ main class for cli licensing tool """

    def __init__(self):
        self.parser = self.setup_parser()
        self.cwd = os.getcwd()

    def run(self):
        self.args = self.parser.parse_args()
        self.license = self.args.license
        self.setup_license_details()
        self.setup_logs()
        self.validate_cli_arguments()
        self.check_if_already_has_license()

        if self.args.r:
            self.update_readme()

        if self.args.remove_headers:
            Header(self.args, self.longname, self.license_filename, self.url).install_headers()
            self.args.remove_headers = False

        self.install_license()
        Header(self.args, self.longname, self.license_filename, self.url).install_headers()

    def setup_parser(self):
        """
        Returns argparse instance, with command line options configured
        """

        parser = argparse.ArgumentParser(prog="garnish",
                description="""
            garnish is designed to help take the pain out of boilerplate licensing.
            You specify the copyright holder and the name of a popular open
            source license, and garnish will create the appropriate LICENSE file
            in your project directory.  Copyright and license information will be
            appended to your existing README file, or one will be created for you
            if it does not already exist.

        BASIC EXAMPLE

            $ garnish gpl3 "Free Software Foundation, Inc." "Emacs 24"
            $ garnish mit "Jennifer Hamon" "garnish"

                """,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="""
        SUPPORTED LICENSES
            garnish supports many popular and interesting software licenses.

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
            If there is another license you would like to see included in garnish,
            please submit a pull request at http://www.github.com/jhamon/garnish
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
            help='remove in-file license notices previously applied by garnish',
            action='store_true',
            default=False,
            dest='remove_headers')
        parser.add_argument('-q', '--quiet',
            help='supress some informational output',
            action='store_true',
            default=False,
            dest='q')
        perser.add_argument('-c', '--custom-header',
            help='specify a custom template for in-file copyright and licensing notices',
            nargs=1,
            action='store',
            dest='custom_header')

        return parser

    def setup_logging():
        logging.basicConfig(filename='.garnish.log',level=logging.DEBUG)
        logging.info('Starting.')


    def setup_license_details(self):
        """
        Defines the following:
            self.longname => string
            self.recommend_infile => boolean
            self.license_filename => string
            self.supported_licenses => list
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

        # Store supported licenses into an object variable for reference during the
        # option validation step.
        self.supported_licenses = filename_LICENSE + filename_COPYING
        self.supported_licenses += filename_COPYINGLESSER + ['unlicense']

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

        urls = {}

        urls['wtfpl'] = 'http://www.wtfpl.net/'
        urls['unlicense'] = 'http://unlicense.org/'
        urls['artistic'] = 'http://dev.perl.org/licenses/artistic.html'
        urls['agpl3'] = 'http://www.gnu.org/licenses/agpl.html'
        urls['apache2'] = 'http://www.apache.org/licenses/LICENSE-2.0.html'
        urls['bsd3'] = 'http://opensource.org/licenses/BSD-3-Clause'
        urls['bsd2'] = 'http://opensource.org/licenses/BSD-2-Clause'
        urls['gpl2'] = 'http://www.gnu.org/licenses/gpl-2.0.html'
        urls['gpl3'] = 'http://www.gnu.org/licenses/gpl.html'
        urls['lgpl3'] = 'http://www.gnu.org/copyleft/lesser.html'
        urls['lgpl2'] = 'http://www.gnu.org/licenses/lgpl-2.0.html'
        urls['lgpl2.1'] = 'http://www.gnu.org/licenses/lgpl-2.1.html'
        urls['mit'] = 'http://opensource.org/licenses/MIT'
        urls['mpl2'] = 'http://www.mozilla.org/MPL/2.0/'
        urls['mpl1.1'] = 'http://www.mozilla.org/MPL/1.1/'
        urls['gpl1'] = 'http://www.gnu.org/licenses/gpl-1.0.html'
        urls['crapl'] = 'http://matt.might.net/articles/crapl/'


        self.longname = longnames[self.license]
        self.url = urls[self.license]
        self.recommend_infile = self.license in recommend_infile
        self.license_filename = license_filenames[self.license]

    def validate_cli_arguments(self):
        """
        Checks for obvious conflicts in options given by the user.  If any are
        found, stops execution.
        """
        help = 'Try -h for help information.'
        log_msg = 'Exiting. Failed validate_cli_arguments()'
        if self.args.license not in self.supported_licenses:
            print 'You have entered an invalid license name.'
            print help
            logging.error('License not supported.')
            logging.error(log_msg)
            exit(bad=True)
        if self.args.remove_headers and self.args.add_headers:
            print 'You have used conflicting header options.'
            print help
            logging.error('Cannot simultaneously add and remove headers.')
            logging.error(log_msg)
            exit(bad=True)

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
            print 'If you would like to apply a new license using garnish, first'
            print 'remove any license files such as LICENSE, COPYING, or UNLICENSE.'
            if not self.args.q:
                print '\n  Conflicting files: \n    {0}'.format('\n    '.join(possible_licenses))
            print '\nNo changes have been made.'
            logging.info('A license file is already present: {0}'.format(possible_licenses[0]))
            logging.info('Exiting.')
            exit(bad=True)
        else:
            return False


    def install_license(self):
        """
        Writes appropriate license text to LICENSE, COPYING, or other file. The name of
        the file will vary according to convention.  E.g. GPL projects often put the
        license into COPYING, projects using the "unlicense" are requested to use
        UNLICENSE, etc.
        """
        resource_name = 'data/licenses/' + self.license
        # pkg_resource API explicitly asks for names joined by '/' regardless of
        # OS.  os.path.join is not recommended.

        with open(self.license_filename,'a') as new_license_file:
            license_source = pkg_resources.resource_stream('garnish', resource_name)
            the_license = license_source.read()
            new_license_file.write(the_license)
            license_source.close()
        if not self.args.q:
            print self.license_filename + ' file created.'
        logging.info('{0} file created.'.format(self.license_filename))


    def update_readme(self):
        """
        Adds a brief copyright and licensing statement to the readme file. For
        longer licenses the reader is referred to the appropriate
        COPYING/LICENSE/etc file, while for shorter licenses (BSD, MIT, etc) the
        full license is appended to the README.
        """

        # Check if there is already a readme file
        dirlist = os.listdir(self.cwd)
        readme_file = [x for x in dirlist if x is 'README' or 'readme.' in x.lower()]
        if len(readme_file) == 0:
            readme_filename = 'README'
        else:
            readme_filename = readme_file[0]

        # Append notice to the README
        with open(readme_filename,'a') as readme:
            resource_location = 'data/readme-statements/' + self.license
            # Again, pkg_resource API requires paths joined by '/'.
            # Don't use os.path.join
            readme_statement = pkg_resources.resource_stream('garnish', resource_location)
            text_to_add = readme_statement.read()
            text_to_add = fill_template(text_to_add, self.args, self.longname, self.license_filename, self.url)
            text_to_add = wrap_paragraphs(text_to_add, 80)
            readme.writelines('\n\n'+ text_to_add)
            status_msg = 'Copyright statement added to ' + readme_filename
            print status_msg
            logging.info(status_msg)


def main():
    my_garnish = Garnish()
    my_garnish.run()

if __name__ == '__main__':
    main()
