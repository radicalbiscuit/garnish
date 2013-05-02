# Status: In Development; minimally working, mostly broken 

Although this software has been tested, there is a chance that any files handled
by the software could be lost.  Consequently, **do not use garnish on work that has
not been commited to your repository.**  As per the MIT License, I am not
responsible for any data loss that may occur as a result of using this tool.

# TODO list:

    - Add some unit tests
    - Write documentation
    - Add header-statements templates for more licenses
    - Better code syntax detection? Filename suffix is not sufficient for
      perl/prolog .pl problem.
    - Allow user-defined header notices
    - Check for existence of headers before adding new ones


# garnish - taking the work out of boilerplate licensing 

A recent study found that [only 15% of github
projects](http://www.theregister.co.uk/2013/04/18/github_licensing_study/) have
clearly stated license terms.  Omitting a license from your open source project
limits its usefulness to the community.  

This project aims to reduce the "pain" of creating boilerplate LICENSE files for
your FOSS projects. 

## How to use

Run `garnish` in your project root directory to create a `LICENSE` file containing
the standard license of your choice.  To see a full list of options  

    $ garnish --help
    $ garnish gpl3 "GNU Foundation" "Emacs 23.0"

Garnish can also add copyright and licensing notices at the beginning of your
source files; this is standard practice with some projects and some licenses.
For licenses that recommend this practice, the user will be prompted
interactively on whether they want to apply the in-file copyright notices.

## Installation instructions

    git clone http://www.github.com/jhamon/garnish
    cd garnish 
    sh install.sh

## Sources

The license text installed by the the `garnish` command line tool is taken from the
Open Source Initiative  

## License

Garnish is Copyright (c) 2013 Jennifer Hamon (jhamon@gmail.com) and released under
the MIT license. For details about this license, please see the text of LICENSE. 

## About the author

My name is Jennifer Hamon.  I am not a lawyer, and this software does not
provide legal advice.  However, if you've found this software useful, I'd love
to hear from you.  Reach out on twitter @xorq or email jhamon@gmail.com.
