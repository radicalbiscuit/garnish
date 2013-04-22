#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import datetime
import os

CWD = os.getcwd()

LIC_DETAILS = {
#        'artistic': ['Perl Foudation Artistic License, Version 2.0', 'LICENSE'],
             'agpl3': ['GNU Affero General Public License, Version 3.0', 'LICENSE'],
#             'apache2': ['Apache License 2.0', 'LICENSE'],
#             'bsd3': ['BSD 3-Clause License', 'LICENSE'],
#             'bsd2': ['BSD 2-Clause License', 'LICENSE'],
             'gpl2': ['GNU General Public License, Version 2.0', 'LICENSE'],
             'gpl3': ['GNU General Public License, Version 3.0', 'LICENSE'],
#             'lgpl3': ['GNU Lesser General Public License, Version 3.0'
#                 ,'COPYING.LESSER'],
             'mit': ['MIT License' ,'LICENSE'],
#             'mpl2': ['Mozilla Public License, Version 2.0', 'LICENSE'],
             'gpl1': ['GNU General Public License, Version 1.0', 'LICENSE'],
#            'lgpl2': ['GNU Lesser General Public License, Version 2.0', 'COPYING.LESSER'],
#             'lgpl2.1': ['GNU Lesser General Public License, Version 2.1', 'COPYING.LESSER'],
#             'mpl1.1': ['Mozilla Public License, Version 1.1', 'LICENSE'],
             'crapl': ['Community Research and Academic Programming License', 'LICENSE'],
#             'unlicense': ['Release code to public domain.  See unlicense.org.', 'UNLICENSE'],
             'wtfpl': ['Do What the Fuck You Want To Public License, Version 2',
             'LICENSE']}

COMMENT_CHARS = {
        '.py':'#',
        '.rb': '#',
        '.pl': '#',
        '.pm': '#',
        '.php': '#',
        '.php3': '#',
        '.php4': '#',
        '.php5': '#',
        '.phps': '#',
        '.cobra': '#',
        '.sh': '#',
        '.tex':'%', 
        '.hs': '--',
        '.lhs': '--',
        '.sql': '--',
        '.abd': '--',
        '.ads': '--',
        '.scpt': '--',
        '.AppleScript': '--',
        '.lua': '--',
        '.as': '//',
        '.h': '//',
        '.c': '//',
        '.hh': '//',
        '.hpp': '//',
        '.hxx': '//',
        '.h++': '//',
        '.cc': '//',
        '.cp': '//',
        '.cpp': '//',
        '.cxx': '//',
        '.c++': '//',
        '.d': '//',
        '.go': '//',
        '.java': '//',
        '.class': '//',
        '.jar': '//',
        '.js': '//',
        '.p': '//',
        '.pp': '//',
        '.pas': '//',
        '.xib': '//',
        '.scala': '//',
        '.sass': '//',
        '.f': '!',
        '.for': '!',
        '.f90': '!',
        '.f95': '!',
        '.lisp ': ';',
        '.clj': ';',
        '.r': ';',
        '.scm': ';',
        '.ss': ';'
        }

parser = argparse.ArgumentParser(prog="LICME",
        description="""
        LICME is designed to help take the pain out of boilerplate licensing.
        You specify the copyright holder and the name of a popular open
        source license, and licme will create the appropriate LICENSE file
        in your project directory.  Copyright and license information will be
        appended to your existing README file, or one will be created for you
        if it does not already exist.

        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=open('licme-list.txt').read()+ """

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

args = parser.parse_args()

def check_valid_license_choice():
    if args.license not in LIC_DETAILS.keys():
        print '''You have entered an invalid license name.  Use -h to see the
        list of licenses and their abbreviations that licme knows about.'''
        sys.exit(1)

def already_has_license():
    """ returns boolean value indicating whether there is
    already a file in the current working directory that has
    'license' in the filename
    """
    common_license_filenames = ['license',
                                'copying',
                                'unlicense',
                                'copying.lesser',
                                'license.txt',
                                'unlicense.txt',
                                'copying.txt']
    cwd_files = os.listdir(CWD)
    possible_licenses = [x for x in cwd_files if x.lower() in
            common_license_filenames]
    if len(possible_licenses) != 0:
        print 'This repository appears to contain license information already.'
        print 'If you would like to apply a new license using licme, first'
        print 'remove any license files such as LICENSE, COPYING, or UNLICENSE.'
        print '\n   Conflicting files: {0}'.format(' '.join(possible_licenses))
        print '\nNo changes have been made.'
        sys.exit(1)
    else:
        return False

def find_readme():
    """ Finds the filename of any existing readme (regardless of file extension)
    and returns the name of the file.  If none is found, 'README' is
    returned."""
    readme_file = [x for x in os.listdir(CWD) if x is 'README' or 'readme.' in x.lower()]
    if len(readme_file) == 0:
        return 'README'
    else:
        return readme_file[0]

def write_readme():
    readme_filename = find_readme()
    with open(readme_filename,'a') as readme:
        with open(os.path.join('readme-statements',args.license),'r') as ADD_TO_README:
            text_to_add = ADD_TO_README.read()
            text_to_add = text_to_add.replace('OWNER_NAME',
                    args.copyright_holder)
            text_to_add = text_to_add.replace('COPYRIGHT_YEAR', args.year)
            text_to_add = text_to_add.replace('PROGRAM_NAME', args.program_name)
            readme.writelines('\n\n'+ text_to_add)
            print 'Copyright statement added to ' + readme_filename

def install_license():
    lic_source = os.path.join('licenses',args.license)
    with open(LIC_DETAILS[args.license][1],'a') as new_license_file:
        with open(lic_source,'r') as license_source:
            the_license = license_source.read()
            new_license_file.write(the_license)
            print LIC_DETAILS[args.license][1] + ' file created'

if __name__ == "__main__":
    check_valid_license_choice()
    if not already_has_license():
        install_license()
        if args.r:
            write_readme()
