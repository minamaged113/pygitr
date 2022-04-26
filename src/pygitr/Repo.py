import subprocess
import os
from typing import Union

class Repo():
    remote = None
    path = None
    branches = None
    tags = None

    def __init__(self, path: str=None, remote:str=None) -> None:
        self.path = self.get_git_dir_path(path)
        self.remote = remote
        self.branches = self.get_branches()
        self.tags = self.get_tags()

    def get_git_dir_path(self, path):
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