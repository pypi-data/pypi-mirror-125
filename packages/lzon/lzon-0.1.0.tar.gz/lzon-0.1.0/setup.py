# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lzon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lzon',
    'version': '0.1.0',
    'description': 'Lazy loading for JSON packets',
    'long_description': '# LZON (Lazy JSON)',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/lzon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
