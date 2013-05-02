import sys
import textwrap

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

def wrap_paragraphs(readlines_list, textwidth=80):
    """ Takes a list of strings called readlines_list and returns a single
    string with lines wrapped to textwidth columns.  readlines_list should
    follow the format produced by calls to open().readlines().  """

    def split_paragraph(readlines_list):
        """ Transform the readlines_list into a nested list.  Each list in the
        output represents the lines of an unwrapped or improperly wrapped
        paragraph. """

        list_of_lists = []
        para_list = []
        for line in readlines_list:
            if line ==  '\n':
                list_of_lists.append(para_list)
                para_list = []
            else:
                para_list.append(line)
        list_of_lists.append(para_list)
        return list_of_lists

    paragraph_list = split_paragraph(readlines_list)

    wrapped_list = []
    for para in paragraph_list:
        newlines = textwrap.wrap(''.join(para),textwidth)
        wrapped_list.extend(newlines)
        wrapped_list.append('\n') # Separate paragraphs
    return '\n'.join(wrapped_list)

