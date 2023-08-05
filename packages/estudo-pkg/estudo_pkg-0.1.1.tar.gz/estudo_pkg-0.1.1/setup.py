# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['estudo_pkg']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['estudocli = estudo_pkg.myLib:cli']}

setup_kwargs = {
    'name': 'estudo-pkg',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'pabloverly',
    'author_email': 'pablopierre.pv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
