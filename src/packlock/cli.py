"""Command-line interface for PackLock."""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path
from typing import Optional, Sequence

from packlock.archive import pack_folder, unpack_archive
from packlock.crypto import DecryptionError, decrypt, encrypt

VAULT_SUFFIX = ".vault"


def _read_password(confirm: bool) -> str:
    password = getpass.getpass("Password: ")
    if not password:
        raise SystemExit("Password cannot be empty.")
    if confirm and getpass.getpass("Confirm password: ") != password:
        raise SystemExit("Passwords do not match.")
    return password


def _default_vault_path(folder_path: Path) -> Path:
    # Append rather than use with_suffix(): it fails on "." and truncates
    # dotted names like "my.photos".
    resolved = folder_path.resolve()
    if not resolved.name:
        raise SystemExit(f"Cannot derive a vault name for '{folder_path}'; use --output.")
    return resolved.with_name(resolved.name + VAULT_SUFFIX)


def lock(folder: str, output: Optional[str]) -> None:
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise SystemExit(f"'{folder}' is not a directory.")

    output_path = Path(output) if output else _default_vault_path(folder_path)
    password = _read_password(confirm=True)

    print(f"Packing '{folder_path}'...")
    archive_bytes = pack_folder(folder_path)

    print("Encrypting...")
    vault_bytes = encrypt(archive_bytes, password)

    output_path.write_bytes(vault_bytes)
    print(f"Created '{output_path}'")


def unlock(vault: str, output: Optional[str]) -> None:
    vault_path = Path(vault)
    if not vault_path.is_file():
        raise SystemExit(f"'{vault}' is not a file.")

    output_dir = Path(output) if output else vault_path.with_suffix("")
    password = _read_password(confirm=False)

    vault_bytes = vault_path.read_bytes()

    print("Decrypting...")
    try:
        archive_bytes = decrypt(vault_bytes, password)
    except DecryptionError as exc:
        raise SystemExit(str(exc)) from exc

    print(f"Unpacking to '{output_dir}'...")
    output_dir.mkdir(parents=True, exist_ok=True)
    unpack_archive(archive_bytes, output_dir)
    print("Done.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="packlock",
        description="Pack it. Lock it. Share it safely.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    lock_parser = subparsers.add_parser("lock", help="Compress and encrypt a folder.")
    lock_parser.add_argument("folder", help="Path to the folder to lock.")
    lock_parser.add_argument("-o", "--output", help="Path to the output .vault file.")

    unlock_parser = subparsers.add_parser("unlock", help="Decrypt and extract a vault.")
    unlock_parser.add_argument("vault", help="Path to the .vault file to unlock.")
    unlock_parser.add_argument("-o", "--output", help="Directory to extract into.")

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "lock":
            lock(args.folder, args.output)
        elif args.command == "unlock":
            unlock(args.vault, args.output)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())
