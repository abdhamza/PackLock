from pathlib import Path

import pytest

from packlock.cli import _default_vault_path


def test_default_vault_path_for_current_directory(tmp_path, monkeypatch):
    folder = tmp_path / "project"
    folder.mkdir()
    monkeypatch.chdir(folder)

    assert _default_vault_path(Path(".")) == tmp_path / "project.vault"


def test_default_vault_path_keeps_dotted_name(tmp_path):
    folder = tmp_path / "my.photos"
    folder.mkdir()

    assert _default_vault_path(folder) == tmp_path / "my.photos.vault"


def test_default_vault_path_rejects_filesystem_root():
    with pytest.raises(SystemExit):
        _default_vault_path(Path(Path.cwd().anchor))
