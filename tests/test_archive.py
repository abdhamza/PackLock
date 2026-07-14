import zipfile

import pytest

from packlock.archive import pack_folder, unpack_archive


def test_pack_and_unpack_roundtrip(tmp_path):
    source = tmp_path / "source"
    (source / "nested").mkdir(parents=True)
    (source / "a.txt").write_text("hello")
    (source / "nested" / "b.txt").write_text("world")

    archive_bytes = pack_folder(source)

    destination = tmp_path / "destination"
    unpack_archive(archive_bytes, destination)

    assert (destination / "a.txt").read_text() == "hello"
    assert (destination / "nested" / "b.txt").read_text() == "world"


def test_unpack_rejects_zip_slip(tmp_path):
    malicious_zip = tmp_path / "evil.zip"
    with zipfile.ZipFile(malicious_zip, "w") as zf:
        zf.writestr("../../evil.txt", "pwned")

    destination = tmp_path / "destination"
    with pytest.raises(ValueError):
        unpack_archive(malicious_zip.read_bytes(), destination)
