# website-update-checker

Simple script that take an url and make an md5 an sha256 out of it. Check if it changed since last time.

## ideas of implementation of this program
- check if an awesome github page changed since last time you consulted it.
- check if a download page as changed, that could imply a change of version.
- etc...


## How to use

- with command line arguments ```python website-checker.py arg1 arg2 arg3```, ```python website-checker.py -h ``` for help
- with a ```site to analyze``` file ```python website-checker.py --file path_to_the_file``` (supports tags). For configuration look at the template.ini file at the repository root.

## Little problems

some website change everytime (google for exemple) => take only the body?

## to implement


- make a specific outfile for the user?
- implement a last_change_only option (w/ argparse) that record only if the last md5 /sha256 is different
