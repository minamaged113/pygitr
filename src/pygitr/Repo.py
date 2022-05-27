import logging
import subprocess
import os
from typing import Union

class Repo:
    b_repo_exists = False
    remote = None
    path = None
    branches = None
    tags = None

    def __init__(self, path: str=None, remote:str=None) -> None:
        self.logger = logging.getLogger(f"{type(self).__name__}")
        self.logger.setLevel(logging.DEBUG)

        if remote:
            self.logger.debug(f"creating a Repo object with remote set to: {remote}, "
            f"and with path: {path}")
            self.remote = remote
            self.path = path
            self.logger.info(f"Repo object created with remote: {self.remote}")
            self.logger.info(f"Repo object created with remote: {self.path}")
        else:
            self.path = self.get_git_dir_path(path)
            self.branches = self.get_branches()
            self.tags = self.get_tags()

    def __repr__(self) -> str:
        """Provide string representation of Repo class.

        Returns:
            str: A string in the following format: 'Repo().remote@Repo().path'.
                Will return '@' if neither Repo().remote or Repo().path is set.
        """
        return f"{self.remote}@{self.path}"

    def clone(self, path:str=None) -> str:
        """Clone remote repository into a given path.
        If the path is given, use the path to clone the repo into.
        If the path is not given, check if the path is set into class variables.

        If the given path is not valid the command will fail.

        Args:
            path (str, optional): Path-like string. Defaults to None.

        Returns:
            str: Path of the repository in the file system.
        """
        if path:
            self.path = path

        self.run(f"git clone {self.remote} .")
        return self.path

    def checkout(self, ref) -> str:
        self.run(f"git checkout {ref}")

    def get_git_dir_path(self, path:str) -> str:
        """Get the root directory of the git repository.

        Args:
            path (str): path string.

        Returns:
            str: path to the git directory containing `.git` directory.
        """
        git_dir = self.run("git rev-parse --git-dir", path=path).stdout.decode().strip()
        if git_dir == ".git":
            # This is the root repository directory
            return path or os.getcwd()
        else:
            return git_dir.split(".git")[0]

    def run(self, command: str, path:str=None) -> subprocess.CompletedProcess:
        return subprocess.run(
            command,
            cwd=path or self.path,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

    def get_branches(self) -> Union[dict,None]:
        out = self.run(
            "git branch --format=\'%(refname);;%(refname:short);;%(objectname);;%(subject);;%(authorname);;%(authoremail);;%(authordate)\' -a"
        )
        raw_branches = out.stdout.decode("utf-8")
        if len(raw_branches) == 0:
            return None
        
        dict_branches = {}
        branches = raw_branches.splitlines()
        for branch in branches:
            branch = branch.split(";;")
            dict_branches[branch[1]] = {
                "refname": branch[0],
                "shortrefname": branch[1],
                "objectname": branch[2],
                "subject": branch[3],
                "authorname": branch[4],
                "authoremail": branch[5],
                "authordate": branch[6]
            }

        return dict_branches

    def get_tags(self) -> Union[dict,None]:
        out = self.run("git tag -l --format=\'%(refname);;%(refname:short);;%(objectname)\'")
        raw_tags = out.stdout.decode("utf-8")
        if len(raw_tags) == 0:
            return None

        dict_tags = {}
        tags = raw_tags.splitlines()
        for tag in tags:
            tag = tag.split(";;")
            dict_tags[tag[1]] = {
                "refname": tag[0],
                "shortrefname": tag[1],
                "objectname": tag[2]
            }
        return dict_tags