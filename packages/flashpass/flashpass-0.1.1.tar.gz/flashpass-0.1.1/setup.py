# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flashpass']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.8,<4.0.0', 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['flashpass = flashpass.cli:main']}

setup_kwargs = {
    'name': 'flashpass',
    'version': '0.1.1',
    'description': 'Encrypt & Decrypt FlashPass .fp files',
    'long_description': None,
    'author': 'Carson Mullins',
    'author_email': 'carsonmullins@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
