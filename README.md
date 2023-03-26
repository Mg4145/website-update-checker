# website-update-checker

Simple script that take an url and make an md5 an sha256 out of it. Check if it changed since last time.

## Little problems

some website change everytime => take only the body?

## to implement

- make a function that verifies if 2 urls point on the same website for exemple https://github.com/ and https://github.com
- make a specific outfile for the user?
- implement a last_change_only option (w/ argparse) that record only if the last md5 /sha256 is different
