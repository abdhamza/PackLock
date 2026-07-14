# Contributing to PackLock

Thanks for your interest in improving PackLock!

## Setup

```bash
git clone https://github.com/abdhamza/PackLock.git
cd PackLock
pip install -e ".[dev]"
```

## Running tests

```bash
pytest -v
```

All existing tests must continue to pass, and new behavior should come with
new tests (see `tests/test_crypto.py` and `tests/test_archive.py` for examples).

## Submitting changes

1. Fork the repo and create a branch off `main`.
2. Make your change, keeping it focused and consistent with the existing style.
3. Make sure `pytest -v` passes locally.
4. Open a pull request describing what changed and why.

CI runs the test suite on Linux and Windows across multiple Python versions for
every pull request — make sure it's green before requesting review.

## Reporting bugs

Open a GitHub issue with steps to reproduce, the command you ran, and your
OS/Python version.

For security vulnerabilities, please follow [SECURITY.md](SECURITY.md) instead
of opening a public issue.
