
def update_readme():
    """
    Adds a brief copyright and licensing statement to the readme file. For
    longer licenses the reader is referred to the appropriate
    COPYING/LICENSE/etc file, while for shorter licenses (BSD, MIT, etc) the
    full license is appended to the README.
    """

    # Check if there is already a readme file
    readme_file = [x for x in os.listdir(CWD) if x is 'README' or 'readme.' in x.lower()]
    if len(readme_file) == 0:
        readme_filename = 'README'
    else:
        readme_filename = readme_file[0]

    # Append notice to the README
    with open(readme_filename,'a') as readme:
        with open(os.path.join('readme-statements',args.license),'r') as ADD_TO_README:
            text_to_add = ADD_TO_README.read()
            text_to_add = fill_template(text_to_add)
            readme.writelines('\n\n'+ text_to_add)
            print 'Copyright statement added to ' + readme_filename


def fill_template(temp):
    """
    Takes a template string (temp) and replaces all template keywords with
    information from commandline arguments.
    """
    temp = temp.replace('OWNER_NAME', args.copyright_holder)
    temp = temp.replace('COPYRIGHT_YEAR', args.year)
    temp = temp.replace('PROGRAM_NAME', args.program_name)
    temp = temp.replace('LICENSE_FILENAME', LIC_DETAILS[args.license][1])
    return temp


def install_license():
    """
    Writes appropriate license text to LICENSE, COPYING, or other file. The name of
    the file will vary according to convention.  E.g. GPL projects often put the
    license into COPYING, projects using the "unlicense" are requested to use
    UNLICENSE, etc.
    """
    lic_source = os.path.join('licenses',args.license)
    with open(LIC_DETAILS[args.license][1],'a') as new_license_file:
        with open(lic_source,'r') as license_source:
            the_license = license_source.read()
            new_license_file.write(the_license)
    if not args.q:
        print LIC_DETAILS[args.license][1] + ' file created.'


