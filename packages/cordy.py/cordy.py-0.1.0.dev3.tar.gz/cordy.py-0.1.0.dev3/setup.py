# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cordy', 'cordy.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'typing-extensions>=3.10.0,<4.0.0',
 'yarl>=1.6.3,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=4.1.2,<5.0.0', 'furo>=2021.7.5-beta.38,<2022.0.0']}

setup_kwargs = {
    'name': 'cordy.py',
    'version': '0.1.0.dev3',
    'description': 'A simple to use Discord API wrapper',
    'long_description': '<h1 align="center">\n    Cordy\n</h1>\n\n<div align="center">\n    A simple, fun to use Discord API wrapper.\n</div>\n\n<p></p>\n\n> This is an upcoming project stay tuned!\n\n## Contribution\nAll contributions and ideas are welcomed!\nJoin our [amazing discord server](https://discord.gg/G4VhjVkGzu) for discussions.\n',
    'author': 'BytesToBits',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BytesToBits/Cordy#readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
