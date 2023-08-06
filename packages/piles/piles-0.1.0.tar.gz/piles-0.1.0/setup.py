# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piles']

package_data = \
{'': ['*']}

install_requires = \
['bunches>=0.1.0,<0.2.0', 'more-itertools>=8.10.0,<9.0.0']

setup_kwargs = {
    'name': 'piles',
    'version': '0.1.0',
    'description': 'lightweight, flexible, extensible python composite data structures',
    'long_description': "The goal of piles is provide lightweight, turnkey, extensible composite data \nstructures. \n\npiles's framework supports a wide range of coding styles. You can create \ncomplex multiple inheritance structures with mixins galore or simpler, \ncompositional objects. Even though the data structures are necessarily object-\noriented, all of the tools to modify them are also available as functions, for \nthose who prefer a more funcitonal approaching to programming. \n\nThe project is also highly documented so that users and developers and make\npiles work with their projects. It is designed for Python coders at all \nlevels. Beginners should be able to follow the readable code and internal\ndocumentation to understand how it works. More advanced users should find\ncomplex and tricky problems addressed through efficient code.\n\n\n",
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WithPrecedent/piles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
