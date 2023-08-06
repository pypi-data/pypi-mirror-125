# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mlnotify', 'mlnotify.plugins']

package_data = \
{'': ['*']}

install_requires = \
['gorilla>=0.4.0,<0.5.0', 'qrcode>=6.1,<7.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.8']}

setup_kwargs = {
    'name': 'mlnotify',
    'version': '1.0.51',
    'description': "No need to keep checking your training. Add just 1 import line and MLNotify will let you know the second it's done.",
    'long_description': None,
    'author': 'Aporia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mlnotify.aporia.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
