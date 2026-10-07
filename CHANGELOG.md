# Changelog

All notable changes to main releases are recorded in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and releases follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Separate focused development checks from remote PR candidate validation.
- Prepare the main changelog through reviewed release preparation PRs and
  publish future SemVer tags and GitHub Releases through one producer.

### Removed

- Automatic production of the moving `main-current` tag. Historical tag objects
  remain preserved.
