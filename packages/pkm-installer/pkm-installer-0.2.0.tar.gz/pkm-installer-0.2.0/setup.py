# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkm_installer']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.8.1,<5.0.0']

setup_kwargs = {
    'name': 'pkm-installer',
    'version': '0.2.0',
    'description': 'lightweight installer for pkm',
    'long_description': '',
    'author': 'bennyl',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
