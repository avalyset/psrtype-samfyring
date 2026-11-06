# Contributing

Questions, error reports and suggestions are welcome as [Issues](https://github.com/avalyset/psrtype-samfyring/issues).

- **Errors in the code, the analysis or the documentation:** open an issue with the file, the line and what you
  expected. A pull request with a test is welcome.
- **Locked files:** files listed in a lock (`PREREG-v1.sha256`, `PREREG-v1-TILLEGG-01.sha256`) or deposited with a
  preregistration are not changed. A fix to one of them goes into a new version with its own record, and the old
  version stays as it is.
- **Tests:** run `python -m pytest -q -rs` before a pull request.

By contributing you agree that code contributions are licensed under the Apache-2.0 licence (`LICENSE`) and documentation
contributions under CC BY 4.0 (`LICENSE-DATA`).
