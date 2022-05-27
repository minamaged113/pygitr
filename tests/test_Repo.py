from cgi import test
from pygitr.Repo import Repo
from test_fixtures import _TestEnv, use_empty_repo, use_basic_repo, use_repo_with_content


def test_Repo_class_exists():
    """test create repo where current working directory is a git repo."""
    repo = Repo()
    assert isinstance(repo, Repo)

def test_read_local_repository_from_path(use_basic_repo):
    """Test local repository is read from path.

    Args:
        use_basic_repo (pytest.fixture): Repo with remote and git config.
    """
    repo = Repo(path=use_basic_repo.path, remote=_TestEnv.remote)
    assert repo.path == use_basic_repo.path
    assert repo.remote == _TestEnv.remote

def test_read_all_branches(use_repo_with_content):
    """Test reading all branches works.

    Args:
        use_repo_with_content (pytest.fixtures): Repo with remote, git config, and some
            dummy content committed.
    """
    repo = Repo(path=use_repo_with_content.path, remote=use_repo_with_content.remote)
    assert "master" in repo.branches.keys()
    assert "develop" in repo.branches.keys()

def test_read_all_tags(use_repo_with_content):
    """Test reading all tags works.

    Args:
        use_repo_with_content (pytest.fixtures): Repo with remote, git config, and some
            dummy content committed.
    """
    repo = Repo(path=use_repo_with_content.path, remote=use_repo_with_content.remote)
    assert _TestEnv.test_tag in repo.tags.keys()
 