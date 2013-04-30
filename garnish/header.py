
class Header(object):
    def install_headers(self):
        """
        This function handles the installation and removal of in-file licensing
        notices.

        The default behavior is to adds a brief copyright header message to every file and file in a
        subdirectory, except those files whose "type" cannot be identified from
        filename suffix or files/filetypes that are excluded by the user when
        prompted.  The list of subfiles to be edited is compiled by a different
        function (list_files_in_subdirs).

        If the -r option is used on the command line, install_headers() will remove
        any license notices that have previously been installed by the program.  I
        considered making a separate uninstall_headers(), but decided to keep these
        together in one scope so as to avoid repeating the massive comment_chars
        dict or resorting to global variables.
        """
        poundsign = '.py .rb .pl .pm .php .php3 .php4 .php5 .phps .cobra .sh'.split(' ')
        dashes = '.hs .lhs .sql .abd .ads .scpt .AppleScript .lua'.split(' ')
        slashes = '.as .h .c .hh .hpp .hxx .h++ .cc .cp .cpp .cxx .c++ '
        slashes += '.d .go .java .class .jar .js .p .pp .pas .xib .scala .sass'
        slashes = slashes.split(' ')
        exclamation = '.f .for .f90 .f95'.split(' ')
        semicolon = '.lisp .clj .r .scm .ss'.split(' ')

        comment_chars = {item:'#' for item in poundsign}
        comment_chars.update({item:'--' for item in dashes})
        comment_chars.update({item:'//' for item in slahes})
        comment_chars.update({item:'!' for item in exclamation})
        comment_chars.update({item:';' for item in semicolon})
        comment_chars['.tex'] = '%'

        # If user has requested with -r option, uninstall previously installed header notices
        if args.remove_headers:
            exclusions = []
            files_to_fix = list_files_in_subdirs(exclusions, comment_chars.keys())
            print len(files_to_fix), files_to_fix
            remove_headers_from_files(files_to_fix, comment_chars)

        # Since the -r remove_header option was not used, proceed with adding new header
        # notices.
        else:
            exclude = raw_input('Would you like to exclude any files from in-file license notice? (y/n) ') in 'yY'
            if exclude:
                exclusions = raw_input('Enter extensions or filenames, space delimited: ')
                exclusions = exclusions.split(' ')
                exclusions = [x.replace('*', '') for x in exclusions] # Sorry, no glob support
            else:
                exclusions = []

            files_to_prepend = list_files_in_subdirs(exclusions, comment_chars.keys())
            add_headers_to_files(files_to_prepend, comment_chars)


    def remove_headers_from_files(self, list_of_files):
        for filename in list_of_files:
            with open(filename, 'r') as original_file:
                original_text = original_file.readlines()
                beginmsg = ':::::::::::::::: BEGIN LICENSE BLOCK :::::::::::::::'
                endmsg = '::::::::::::::::  END LICENSE BLOCK  :::::::::::::::'

                start = [k for k,v in enumerate(original_text) if beginmsg in v][0]
                end = [k for k,v in enumerate(original_text) if endmsg in v][0]
                if end != []:
                    modified_text = original_text[0:start] + original_text[end+1:]
                    print 'nuhhhhhh'
                else:
                    modified_text = original_text
                    print 'asdfasdf'

            with open(filename, 'w') as modified_file:
                modified_file.writelines(modified_text)


    def add_headers_to_files(self, list_of_files, comment_chars):
        # Take a list of filenames and add an appropriate
        # license header to each one.
        def add_header_to_file(filename, header_message):
            """
            Add a given license header message to the file
            with name "filename"
            """
            with open(filename, 'r') as original:
                file_contents = original.read()
            with open(filename, 'w') as modified:
                modified.write(header_message + file_contents)

        def build_header_message(filetype, comment_chars):
            """
            Given license information in the args and a file extension string in
            filetype variable, return a string containing the appropriate in-file
            licensing header string.
            """

            if filetype in comment_chars.keys():
                comment_char = comment_chars[filetype]
            else:
                print 'Could not add header to {0}. Unknown filetype.'.format(filename)
                return

            start_msg = comment_char + ' :::::::::::::::: BEGIN LICENSE BLOCK :::::::::::::::'
            end_msg = comment_char + ' ::::::::::::::::  END LICENSE BLOCK  :::::::::::::::'

            notice = open(os.path.join('header-statements',args.license),'r').readlines()
            notice = map(fill_template, notice)
            notice = [comment_char + ' ' + x for x in notice]
            notice = ''.join(notice)

            complete_header = start_msg + notice + end_msg
            return complete_header

        # Store header messages as they are built using file extension as keys.
        header_messages = {}
        for file_to_check in list_of_files:
            filetype = re.search('\..+$', file_to_check).group(0)
            if filetype in header_messages.keys():
                add_header_to_file(file_to_check, header_messages[filetype])
            else:
                header_messages[filetype] = build_header_message(filetype, comment_chars)
                add_header_to_file(file_to_check, header_messages[filetype])


    def list_files_in_subdirs(self, exclusions, whitelist):
        """
        Returns a recursive list of all files an all directories,
        excluding .subdirectories and any explicit exclusions.
        The exclusions argument should be a list of strings,
        either file extensions or filenames.  For example,
        ['.txt', 'README.md', 'not_this.py'].  Comparisons are
        done with endswith instead of regex to keep this flexible.
        """

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

