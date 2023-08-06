# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaltherma']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pyaltherma',
    'version': '0.0.1',
    'description': 'Python scripts for controlling Daikin Altherma heat pump.',
    'long_description': None,
    'author': 'Tadas Danielius',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
