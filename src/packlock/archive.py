"""Folder <-> zip archive helpers with zip-slip protection."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path


def pack_folder(folder: Path) -> bytes:
    """Compress all files under ``folder`` into an in-memory zip archive."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(folder))
    return buffer.getvalue()


def unpack_archive(data: bytes, destination: Path) -> None:
    """Extract a zip archive into ``destination``.

    Rejects archives containing entries that would resolve outside of
    ``destination`` (a "zip-slip" path traversal attack).
    """
    destination = destination.resolve()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for member in zf.infolist():
            target = (destination / member.filename).resolve()
            try:
                target.relative_to(destination)
            except ValueError:
                raise ValueError(f"Unsafe path in archive: {member.filename}") from None
        zf.extractall(destination)
