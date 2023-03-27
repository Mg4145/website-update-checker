# website-update-checker

Simple script that take an url and make an md5 an sha256 out of it.
Check if it changed since last time.

## Ideas
- Check if an awesome github page changed since last time you consulted it.
- Check if a download page as changed, that could imply a change of version.
- etc...


## Usage

* For configuration look at the template.ini file at the repository root.

Running with arguments:

```python
website-checker.py arg1 arg2 arg3
```

Help running:

```python
website-checker.py -h
```

With website to analyze (supports tags):

```python
website-checker.py --file path_to_the_file
```

## Problems

- Some website change everytime (Google for example) => take only the body?

## Implement

- make a specific outfile for the user?
- implement a last_change_only option (w/ argparse) that record only if the
  last md5 /sha256 is different
