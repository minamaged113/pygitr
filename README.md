# PyGitter
Python git repository interface

## Usage

This library provides interfaces to interact with git repositories.

```python
r = Repo()              # to be executed in the directory that has local repo
# or
r = Repo(path=<PATH>)   # where path is a directory that contains `.git` dir
# or
r = Repo(remote=<URL>)  # URL, either HTTPS or SSH, you can also add `path` to specify dir to clone into.
```

## Working with the source code

To work with the source code, check the `CONTRIBUTE.md`
