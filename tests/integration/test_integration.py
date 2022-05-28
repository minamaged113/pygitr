import os
from pygitter.Repo import Repo


def test_clone(tmpdir):
    """Clone a repository from the web. and check the README content.

    Args:
        tmpdir (pytest.fixture): Pytest temporary directory.
    """
    repo = Repo(remote="https://github.com/xournalpp/xournalpp.git")
    repo.path = tmpdir.strpath
    repo.clone()
    readme_filepath = os.path.join(repo.path,"README.md")
    with open(readme_filepath, "r") as fh:
        data = fh.read()

    assert "# Xournal++" in data