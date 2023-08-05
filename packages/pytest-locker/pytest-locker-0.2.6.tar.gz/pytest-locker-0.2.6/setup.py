# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_locker']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4']

setup_kwargs = {
    'name': 'pytest-locker',
    'version': '0.2.6',
    'description': ' Used to lock object during testing. Essentially changing assertions from being hard coded to asserting that nothing changed ',
    'long_description': '# PyTest-Locker\n<div style="width: 400pt; margin: 0 auto">\n    <img src="https://raw.githubusercontent.com/Luttik/pytest-locker/master/docs/assets/images/example.svg" style="max-width: 100%;" alt="Example">\n</div>\n\n<p align="center">\n    PyTest-Locker: The fasted way to check for unexpected behaviour changes\n</p>\n\n<p align="center">\n    <a href="https://github.com/Luttik/pytest-locker/actions?query=workflow%3ACI+branch%3Amaster">\n        <img src="https://github.com/luttik/pytest-locker/workflows/CI/badge.svg" alt="actions batch">\n    </a>\n    <a href="https://pypi.org/project/pytest-locker/">\n        <img src="https://badge.fury.io/py/pytest-locker.svg" alt="pypi">\n    </a>\n    <a href="https://pypi.org/project/pytest-locker/">\n        <img src="https://shields.io/pypi/pyversions/pytest-locker" alt="python versions">\n    </a>\n    <a href="https://codecov.io/gh/luttik/pytest-locker">\n        <img src="https://codecov.io/gh/Luttik/pytest-locker/branch/master/graph/badge.svg" alt="codecov">\n    </a>\n    <a href="https://xgithub.com/Luttik/pytest-locker/blob/master/LICENSE">\n        <img src="https://shields.io/github/license/luttik/pytest-locker" alt="License: MIT">\n    </a>\n    <a href="https://github.com/psf/black">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">\n    </a>\n</p>\n\nThe test-locker can be used to "lock" data during a test. This means that rather than having to manually specify the\nexpected output you lock the data when it corresponds to expected behaviour, afterwards you only need to check if the\ndata has not changed.\n\nData can be a response, but state and previous calls can also be represented as data. This gives you the option to "\nlock" just about anything that your software does using this library.\n\n## Why use PyTest-Locker\n\n- Time efficient: No need to hard code expected responses. (Especially usefull for data heavy unittests)\n- Easy to verify changes:\n\n    - Seperates the logic of the test from the expected values.\n    - The lock files (containing the expected values), and changes to them, are easy to interpret. This makes it really\n      simple to evaluate changes during testing, in commits and in pull request.\n\n## Install\n\nrun `pip install pytest-locker`\n\n## Usage\n\n### Configuring the project and writing your first test.\n\n1. Add `from pytest_locker import locker` to your\n   [conftest.py](https://docs.pytest.org/en/2.7.3/plugins.html?highlight=re)\n   file\n2. To access the locker by adding it to the method parameters i.e. `def test_example(locker)`\n\n[//]: # (todo Also write instrcutions for non-string types.)\n4. Use `locker.lock(your_string, optional_name)` to lock the data (of-course you can also lock other types).\n5. Ensure that the [pytest rootdir](https://docs.pytest.org/en/latest/customize.html) is fixed.\n   See [the pytest customize documentation](https://docs.pytest.org/en/latest/customize.html) for all the options (one\n   is adding a `pytest.ini` to the root folder)\n6. Ensure that `.pytest_locker/` is synced via git, to ensure that you, your team, and your CI/CD pipelines are working\n   with the same data.\n\nAnd you\'re all set!\n\n### Accepting the current behavior and checking fo changes in this behavior\n\nThere are two modes based on for locking. The first is\n\n1. When user input is allowed, i.e. when running pytest with\n   `--capture  no` or `-s`\n\n   When user input is allowed and the given data does not correspond to the data in the lock the *user is prompted* if\n   the new data should be stored or if the tests should fail.\n\n2. When user input is captured which is default behavior for pytest\n\n   If user input is not allowed the tests will *automatically fail* if the expected lock file does not exist or if the\n   data does not correspond to the data in the lock file.\n\n## The Locker class\n\nYou can also use `pytest_locker.Locker` (i.e. the class of which the\n`locker` fixture returns an instance) directly to create fixtures that locks a (non-string) object without needing to\nturn the object into a string it.\n\nYou can also use `pytest_locker.Locker` as a basis for locking more complex objects than just strings.\nOne example is `pytest_locker.JsonLocker` (and the corresponding `pytest_locker.json_locker` fixture)\n\n## Examples\n\nFor example of use look at the tests in\n[repr-utils](https://github.com/Luttik/repr-utils).\n',
    'author': 'Luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pytest-locker.daanluttik.nl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
