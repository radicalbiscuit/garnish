#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import datetime
import os
import re

CWD = os.getcwd()

# This dictionary keys license argument to ["longform license name", "license filename",
# boolean: recommend in-file notice?]
LIC_DETAILS = {
#        'artistic': ['Perl Foudation Artistic License, Version 2.0', 'LICENSE',
#        True],
             'agpl3': ['GNU Affero General Public License, Version 3.0',
                 'LICENSE', True],
#             'apache2': ['Apache License 2.0', 'LICENSE', True],
#             'bsd3': ['BSD 3-Clause License', 'LICENSE', False],
#             'bsd2': ['BSD 2-Clause License', 'LICENSE', False],
             'gpl2': ['GNU General Public License, Version 2.0', 'COPYING', True],
             'gpl3': ['GNU General Public License, Version 3.0', 'COPYING', True],
#             'lgpl3': ['GNU Lesser General Public License, Version 3.0'
#                 ,'COPYING.LESSER', True],
             'mit': ['MIT License' ,'LICENSE', False],
#             'mpl2': ['Mozilla Public License, Version 2.0', 'LICENSE', True],
             'gpl1': ['GNU General Public License, Version 1.0', 'COPYING', True],
#            'lgpl2': ['GNU Lesser General Public License, Version 2.0',
#            'COPYING.LESSER', True],
#             'lgpl2.1': ['GNU Lesser General Public License, Version 2.1',
#             'COPYING.LESSER', True],
#             'mpl1.1': ['Mozilla Public License, Version 1.1', 'LICENSE', True],
             'crapl': ['Community Research and Academic Programming License',
                 'LICENSE', False],
#             'unlicense': ['Unlicense', 'UNLICENSE', False],
             'wtfpl': ['Do What the Fuck You Want To Public License, Version 2',
             'LICENSE', False]}


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

args = parser.parse_args()

def check_arguments():
    help = 'Try -h for help information.'
    if args.license not in LIC_DETAILS.keys():
        print 'You have entered an invalid license name.'
        print help
        sys.exit(1)
    if args.remove_headers and args.add_headers:
        print 'You have used conflicting header options.'
        print help
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
            text_to_add = fill_template(text_to_add)
            readme.writelines('\n\n'+ text_to_add)
            print 'Copyright statement added to ' + readme_filename

def fill_template(text, author, year, program, filename):
    text = text.replace('OWNER_NAME', author)
    text = text.replace('COPYRIGHT_YEAR', year)
    text = text.replace('PROGRAM_NAME', program)
    text = text.replace('LICENSE_FILENAME', filename)
    return text

def install_license():
    lic_source = os.path.join('licenses',args.license)
    with open(LIC_DETAILS[args.license][1],'a') as new_license_file:
        with open(lic_source,'r') as license_source:
            the_license = license_source.read()
            new_license_file.write(the_license)
            print LIC_DETAILS[args.license][1] + ' file created'

def build_header_message(args, filetype):
   # Given license information in the args and a file extension string in
   # filetype variable, return a string containing the appropriate in-file
   # licensing header string.

    comments_chars = {
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
        '.tex': '%',
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

    if filetype in comments_chars.keys():
        comment_char = comments_chars[filetype]
    else:
        print 'Could not add header to {0}. Unknown filetype.'.format(filename)
        return

    start_msg_label = ' BEGIN LICENSE BLOCK '
    end_msg_label = ' END LICENSE BLOCK '
    filler = 10 * comment_char
    fillern = filler + '\n'

    notice = open(os.path.join('header-statements',args.license),'r').readlines()
    notice = map(fill_template, notice)
    notice = [comment_char + ' ' + x for x in notice]
    notice = ''.join(notice)

    start_msg = filler + start_msg_label + fillern
    end_msg = filler + end_msg_label + fillern

    complete_header = start_msg + notice + end_msg
    return complete_header

def add_header_to_file(filename, header_message):
    # Add a given license header message to the file
    # with name "filename"
    with open(filename, 'r+') as filetoedit:
        file_contents = filetoedit.read()

        complete_header = build_header_message(args.license)

        filetoedit.write(complete_header + file_contents)

def add_headers_to_files(args, list_of_files):
    # Take a list of filenames and add an appropriate
    # license header to each one.
    header_messages = {}
    for file_to_check in list_of_files:
        filetype = re.search('\..+', filename).group(0)
        if filetype in header_messages.keys():
            add_header_to_file(file_to_check, header_messages[filetype])
        else:
            header_messages[filetype] = build_header_message(args, filetype)
            add_header_to_file(file_to_check, header_messages[filetype])


if __name__ == "__main__":
    add_header_to_file('testfile.py')
    add_header_to_file('testfile.rb')
    add_header_to_file('testfile.scala')
    # check_arguments()
    # if not already_has_license():
    #     install_license()
     #    if args.r:
      #       write_readme()
