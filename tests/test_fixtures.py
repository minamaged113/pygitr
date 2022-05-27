import re
import subprocess
import tempfile
import time

import pytest


class _TestEnv:
    username = "pygitr_tester"
    email = "pygitr_tester@example.com"
    path = None
    remote = "https://git/repo.git"
    test_tag = "1.0.0"
    
    
    def __init__(self,
        path: str = None,
        remote: str = None,
        username: str = None,
        email: str = None
    ) -> None:
        self.path = path or tempfile.TemporaryDirectory(prefix=str(int(time.time()))+"-", suffix="pygitr-tests").name
        self.remote = remote
        self.username = username
        self.email = email
        self.git_version = self.run("git --version").stdout.decode("utf-8")

    def run(self, command: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            command,
            cwd=self.path,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        

    def configure_repo(self, username: str = None, email: str = None) -> None:
        self.run(
            f"git config --local user.name '{self.username or username}' &&"
            f"git config --local user.email '{self.email or email}'"
        )

    def create_change(self, content: str=None, filename: str = "file.txt") -> None:
        self.run(
            f"echo '{time.time()}' > {filename}"
        )

    def stage_change(self, filename: str = "file.txt") -> None:
        self.run(f"git add {filename}")
    
    def commit_change(self, message:str="dummy") -> None:
        self.run(f"git commit -m {message}")

    def create_git_repository(self) -> None:
        self.run("git init .")
    
    def add_remote_url(self, remote: str=None) -> None:
        self.run(
            f"git remote add origin {self.remote or remote}"
        )

    def create_tag(self, tag:str, message:str="dummy_tag", commit_id:str=None) -> None:
        self.run(f"git tag -a {tag} {commit_id if commit_id else ''} -m '{message}'")

    def create_branch(self, branch_name:str) -> None:
        self.run(f"git branch {branch_name}")

    def checkout(self, ref:str) -> None:
        self.run(f"git checkout {ref}")


@pytest.fixture
def use_empty_repo(tmpdir) -> _TestEnv:
    """Repository with no remote.

    Args:
        tmpdir (pytest.fixture): tempdir pytest fixture

    Returns:
        TestEnv: An instance of class TestEnv that represents the repository.
    """
    env = _TestEnv(path=tmpdir.strpath)
    env.create_git_repository()
    return env

@pytest.fixture
def use_basic_repo(use_empty_repo) -> _TestEnv:
    use_empty_repo.add_remote_url()
    use_empty_repo.configure_repo()
    return use_empty_repo

@pytest.fixture
def use_repo_with_content(use_basic_repo) -> _TestEnv:
    use_basic_repo.create_change()
    use_basic_repo.stage_change()
    use_basic_repo.commit_change()
    use_basic_repo.create_tag(tag=_TestEnv.test_tag)
    use_basic_repo.create_branch("develop")
    return use_basic_repo
