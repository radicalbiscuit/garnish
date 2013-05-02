import sys

def fill_template(temp, args, longname, filename, url):
    """
    Takes a template string (temp) and replaces all template keywords with
    information from commandline arguments.
    """
    temp = temp.replace('OWNER_NAME', args.copyright_holder)
    temp = temp.replace('COPYRIGHT_YEAR', args.year)
    temp = temp.replace('PROGRAM_NAME', args.program_name)
    temp = temp.replace('LICENSE_LONGNAME', longname)
    temp = temp.replace('LICENSE_FILENAME', filename)
    temp = temp.replace('LICENSE_URL', url)
    return temp

def exit(bad=False):
        if bad:
            print 'The operation was not completed successfully.'
            sys.exit(1)
        else:
            sys.exit(0)
