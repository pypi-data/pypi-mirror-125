# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['joshk']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'joshk',
    'version': '0.1.2',
    'description': "A package of Josh K's things",
    'long_description': None,
    'author': 'Josh K',
    'author_email': '59419126+this-josh@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
