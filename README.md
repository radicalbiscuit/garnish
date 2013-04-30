# Status: In Development; minimally working, mostly broken 

Although this software has been tested, there is a chance that any files handled
by the software could be lost.  Consequently, **do not use kale on work that has
not been commited to your repository.**  As per the MIT License, I am not
responsible for any data loss that may occur as a result of using this tool.

# TODO list:

    - Add some unit tests
    - Install.sh?
    - Write documentation
    - Read about distutils to figure out how packaging should be handled
    - Add header-statements templates for more licenses
    - register twitter account for project
    - How to upload projects to pypi?
    - Better code syntax detection? Filename suffix is not sufficient for
      perl/prolog .pl problem.
    - Allow user-defined header notices


# kale - taking the work out of boilerplate licensing 

A recent study found that (only 15% of github
projects)[http://www.theregister.co.uk/2013/04/18/github_licensing_study/] have
clearly stated license terms.  Omitting a license from your open source project
limits its usefulness to the community.  

This project aims to reduce the "pain" of creating boilerplate LICENSE files for
your FOSS projects. 

## How to use

Run `kale` in your project root directory to create a `LICENSE` file containing
the standard license of your choice.  To see a full list of options  

    $ kale --help
    $ kale gpl3 "GNU Foundation" "Emacs 23.0"

kale can also add copyright and licensing notices at the beginning of your
source files; this is standard practice with some projects and some licenses.
For licenses that recommend this practice, the user will be prompted
interactively on whether they want to apply the in-file copyright notices.

## Installation instructions

    git clone http://www.github.com/jhamon/kale
    cd kale 
    sh install.sh

## Sources

The license text installed by the the `kale` command line tool is taken from the
Open Source Initiative  

## License

Kale is Copyright (c) 2013 Jennifer Hamon (jhamon@gmail.com) and released under
the MIT license. For details about this license, please see the text of LICENSE. 

## About the author

My name is Jennifer Hamon.  I am not a lawyer, and this software does not
provide legal advice.  However, if you've found this software useful, I'd love
to hear from you.  Reach out on twitter @xorq or email jhamon@gmail.com.
