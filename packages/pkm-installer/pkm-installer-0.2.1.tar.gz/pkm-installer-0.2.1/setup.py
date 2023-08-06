# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkm_installer']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.7.0']}

setup_kwargs = {
    'name': 'pkm-installer',
    'version': '0.2.1',
    'description': 'lightweight installer for pkm',
    'long_description': '',
    'author': 'bennyl',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
