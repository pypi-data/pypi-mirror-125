[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]

muzzle
======

Little XML parser library based on defusedxml and xmltodict.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Release](#release)

## Installation

[muzzle is available on PyPI](https://pypi.org/project/muzzle/), so to install it simply use:

```
$ pip install muzzle
```

## Usage

See the [`examples` directory](/examples) for more scripts.


## Release

To create a new release, follow these steps (please respect [Semantic Versioning](http://semver.org/)):

1. Adapt the version number in `muzzle/__init__.py`
1. Update the CHANGELOG with the version
1. Create a [pull request to merge `develop` into `main`](https://github.com/metaodi/muzzle/compare/main...develop?expand=1) (make sure the tests pass!)
1. Create a [new release/tag on GitHub](https://github.com/metaodi/muzzle/releases) (on the main branch)
1. The [publication on PyPI](https://pypi.python.org/pypi/muzzle) happens via [GitHub Actions](https://github.com/metaodi/muzzle/actions?query=workflow%3A%22Upload+Python+Package%22) on every tagged commit


<!-- Badges -->
[pypi-image]: https://img.shields.io/pypi/v/muzzle
[pypi-url]: https://pypi.org/project/muzzle/
[build-image]: https://github.com/metaodi/muzzle/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/metaodi/muzzle/actions/workflows/build.yml
