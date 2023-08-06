# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ceplib',
 'ceplib.errors',
 'ceplib.interfaces',
 'ceplib.loader',
 'ceplib.model',
 'ceplib.services',
 'ceplib.services.awesomeapi',
 'ceplib.services.cepla',
 'ceplib.services.correios',
 'ceplib.services.viacep',
 'ceplib.services.widenet',
 'ceplib.transforms',
 'ceplib.validations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ceplib',
    'version': '0.1.1',
    'description': 'An easy way to fetch Brazil Zip code using several services',
    'long_description': None,
    'author': 'Erick Duarte',
    'author_email': 'erickod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
