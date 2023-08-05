# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_paramiko',
 'nornir_paramiko.plugins',
 'nornir_paramiko.plugins.connections',
 'nornir_paramiko.plugins.tasks']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3.0.0,<4.0.0', 'paramiko>=2.7,<3.0', 'scp>=0.13.3,<0.14.0']

extras_require = \
{'docs': ['sphinx>=3,<4',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0']}

entry_points = \
{'nornir.plugins.connections': ['paramiko = '
                                'nornir_paramiko.plugins.connections:Paramiko']}

setup_kwargs = {
    'name': 'nornir-paramiko',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Devon Mar',
    'author_email': 'devonm@mdmm.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
