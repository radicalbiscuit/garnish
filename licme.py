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
parser.add_argument('-q', '--quiet',
    help='supress some informational output',
    action='store_true',
    default=False,
    dest='q')

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
        if not args.q:
            print '\n  Conflicting files: \n    {0}'.format('\n    '.join(possible_licenses))
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

def update_readme():
    readme_filename = find_readme()
    with open(readme_filename,'a') as readme:
        with open(os.path.join('readme-statements',args.license),'r') as ADD_TO_README:
            text_to_add = ADD_TO_README.read()
            text_to_add = fill_template(text_to_add)
            readme.writelines('\n\n'+ text_to_add)
            print 'Copyright statement added to ' + readme_filename

def fill_template(temp):
    temp = temp.replace('OWNER_NAME', args.copyright_holder)
    temp = temp.replace('COPYRIGHT_YEAR', args.year)
    temp = temp.replace('PROGRAM_NAME', args.program_name)
    temp = temp.replace('LICENSE_FILENAME', LIC_DETAILS[args.license][1])
    return temp

def install_license():
    lic_source = os.path.join('licenses',args.license)
    with open(LIC_DETAILS[args.license][1],'a') as new_license_file:
        with open(lic_source,'r') as license_source:
            the_license = license_source.read()
            new_license_file.write(the_license)
            print LIC_DETAILS[args.license][1] + ' file created'

def install_headers():
    comment_chars = {
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

    if args.remove_headers:
        exclusions = []
        files_to_fix = get_files_to_add_header(exclusions, comment_chars.keys())
        remove_headers_from_files(files_to_fix, comment_chars)
    else:
        exclude = raw_input('Would you like to exclude any files from in-file license notice? (y/n) ') in 'yY'
        if exclude:
            exclusions = raw_input('Enter extensions or filenames, space delimited: ')
            exclusions = exclusions.split(' ')
            exclusions = [x.replace('*', '') for x in exclusions] # Sorry, no glob support
        else:
            exclusions = []

        files_to_prepend = get_files_to_add_header(exclusions, comment_chars.keys())
        add_headers_to_files(args, files_to_prepend, comment_chars)

def remove_headers_from_files(files_to_fix, comment_chars):
    header_messages = {}
    for file_to_fix in files_to_fix:
        filetype = re.search('\..+$', file_to_fix).group(0)
        if filetype in header_messages.keys():
            remove_header_from_file(file_to_fix, header_messages[filetype])
        else:
            header_messages[filetype] = build_header_message(args, filetype, comment_chars)
            remove_header_from_file(file_to_fix, header_messages[filetype])

def remove_header_from_file(filename, header):
    header = header.split('\n')
    header_start = header[0]
    header_end = header[-1]

    with open(filename, 'r') as original_file:
        original_text = original_file.readlines()
        start, end = 0, 0
        try:
            start = original_text.index(header_start)
            end = original_text.index(header_end)
        except:
            pass

        if end != 0:
            modified_text = original_text[0:start] + original_text[end+1:]
        else:
            modified_text = original_text

    with open(filename, 'w') as modified_file:
        modified_file.writelines(modified_text)


def build_header_message(args, filetype, comment_chars):
   # Given license information in the args and a file extension string in
   # filetype variable, return a string containing the appropriate in-file
   # licensing header string.

    if filetype in comment_chars.keys():
        comment_char = comment_chars[filetype]
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
    with open(filename, 'r') as original:
        file_contents = original.read()
    with open(filename, 'w') as modified:
        modified.write(header_message + file_contents)


def add_headers_to_files(args, list_of_files, comment_chars):
    # Take a list of filenames and add an appropriate
    # license header to each one.
    header_messages = {}
    for file_to_check in list_of_files:
        filetype = re.search('\..+$', file_to_check).group(0)
        if filetype in header_messages.keys():
            add_header_to_file(file_to_check, header_messages[filetype])
        else:
            header_messages[filetype] = build_header_message(args, filetype, comment_chars)
            add_header_to_file(file_to_check, header_messages[filetype])


def get_files_to_add_header(exclusions, whitelist):
    # Returns a recursive list of all files an all directories,
    # excluding .subdirectories and any explicit exclusions.
    # The exclusions argument should be a list of strings,
    # either file extensions or filenames.  For example,
    # ['.txt', 'README.md', 'not_this.py'].  Comparisons are
    # done with endswith instead of regex to keep this flexible.

    pathlist = []
    excluded_files = []
    for dirname, subdirs, files in os.walk(os.getcwd()):
        for subdir in subdirs:
            if re.match('^\.', subdir) != None:
                subdirs.remove(subdir) # Ignore dot-directories

        for item in files:
            excl = [item.endswith(x) for x in exclusions].count(True)
            white = [item.endswith(x) for x in whitelist].count(True)
            if white and not excl:
                pathlist.append(os.path.join(dirname, item))
            else:
                excluded_files.append(os.path.join(item))

    if excluded_files and not args.q:
        print 'The following files did not receive an in-file licensing  notice, '
        print 'because you specified them or I wasn\'t sure what type of file it '
        print 'was based on the file extension: '
        for e in excluded_files:
            print '    ' + e
        print

    return pathlist



if __name__ == "__main__":
    check_arguments()
    if not already_has_license():
        install_license()
        install_headers()
        if args.r:
            update_readme()
