# Status: In Development; minimally working, mostly broken 

Although this software has been tested, there is a slim chance that any files
handled by the software could be lost.  Consequently, **do not use licme for
data that has not been commited to your reposity.**  I am not responsible for
your data loss.

# LICME - taking the work out of boilerplate licensing 

A recent study found that (only 15% of github projects)[http://www.theregister.co.uk/2013/04/18/github_licensing_study/] have clearly stated license terms.  Omitting a license from your open source project limits its usefulness to the community.  

This project aims to reduce the "pain" of creating boilerplate LICENSE files for your FOSS projects. 

## How to use

Run `licme` in your project root directory to create a `LICENSE` file containing the standard license of your choice.  To see a full list of options  

    $ licme help
    $ licme -l
    $ licme mit
    $ licme gpl3

## Installation instructions

    git clone http://www.github.com/jhamon/licme
    cd licme 
    sh install.sh

## Sources

The license text installed by the the `licme` command line tool is taken from the Open Source Initiative  

## License

This project is Copyright (c) 2013 Jennifer Hamon (jhamon@gmail.com) and released under the MIT license. For details about this license, please see the text of LICENSE. 
