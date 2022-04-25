from pygitr.Repo import Repo
from test_fixtures import TestEnv, use_empty_repo, use_basic_repo, use_repo_with_content


def test_Repo_class_exists():
    repo = Repo()
    assert isinstance(repo, Repo)

def test_read_local_repository_from_path(use_basic_repo):
    repo = Repo(path=use_basic_repo.path, remote=TestEnv.remote)
    assert repo.path == use_basic_repo.path
    assert repo.remote == TestEnv.remote

def test_read_all_branches(use_repo_with_content):
    repo = Repo(path=use_repo_with_content.path, remote=use_repo_with_content.remote)
    assert "master" in repo.branches.keys()
    assert "develop" in repo.branches.keys()

def test_read_all_tags(use_repo_with_content):
    repo = Repo(path=use_repo_with_content.path, remote=use_repo_with_content.remote)
    assert TestEnv.test_tag in repo.tags.keys()