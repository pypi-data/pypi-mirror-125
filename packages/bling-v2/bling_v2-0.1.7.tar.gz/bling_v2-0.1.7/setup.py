# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bling_v2', 'bling_v2.controllers', 'bling_v2.models', 'bling_v2.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'dynaconf>=3.1.7,<4.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.3.3,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'bling-v2',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Carmo-sousa',
    'author_email': 'carmosousa20@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
