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

## Quickstart guide 

For python devs, installing the latest release of garnish is as simple as 

    pip install garnish

If you're not a regular python user, you can also install it the standard way

    git clone git://github.com/jhamon/garnish.git
    cd garnish
    python setup.py install

Next nagivate to your project root, and use the following syntax on the command
line

    garnish <license name> <copyright holder> <your awesome project name> 

A few examples of basic usage:

    garnish gpl3 "GNU Foundation" "Emacs" 
    garnish mit "Google Inc" "Angular JS"

To see the full list of available licenses, type `garnish -h`.

Garnish can also add copyright and licensing notices at the beginning of your
source files; this is standard practice with some projects and some licenses.
Those licenses which recommend the use of headers will prompt you about it.  For
licenses that recommend this practice, the user will be prompted interactively
o. 

For those licenses which don't recommend in-file copyright and license notices,
you can still explicitly ask garnish to apply them with the `-w` or
`--with-headers` options if you would like.  copyright notices.

## License

Garnish is Copyright (c) 2013 Jennifer Hamon (jhamon@gmail.com) and released under
the MIT license. For details about this license, please see the text of LICENSE. 

## Contacting the author

I am not a lawyer, and this software does not provide legal advice.  However, if
you've found this software useful, I'd love to hear from you.  Reach out on
twitter @xorq or email jhamon@gmail.com.

Please report any issues or problems, please use the github issue tracker
available at [here](https://github.com/jhamon/garnish/issues).
