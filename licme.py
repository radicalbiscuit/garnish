#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

available_licenses = "artistic agpl3 aparche2 bsd3 gpl2 gpl3 lgpl3 mit mpl2 gpl1 lgpl2 lgpl2.1 mpl1.1 crapl unlicense"
available_licenses = available_licenses.split(' ')


parser = argparse.ArgumentParser(prog="LICME",
        description="""
        LICME is designed to help take the pain out of boilerplate licensing.
        You specify the copyright holder and the name of a popular open
        source license, and licme will create the appropriate LICENSE file
        in your project directory.  Copyright and license information will be
        appended to your existing README file, or one will be created for you
        if it does not already exist.

EXAMPLES
    licme -l gpl3 -c "Richard Stallman"
    licme -l crapl -c "Matt Might"
    licme -l mit -c "Tim the Beaver"

        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=open('licme-list.txt').read()+ """

CONTRIBUTING
    If there is another license you would like to see included in licme,
    please submit a pull request at http://www.github.com/jhamon/licme
        """)

parser.add_argument('-l', '--license',
        help="specify the license you would like to use.", required=True)
parser.add_argument('-c', '--copyright-holder', type=str, required=True)
myargs = parser.parse_args()
print myargs.license
print myargs.copyright_holder

