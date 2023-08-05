# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunches']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.10.0,<9.0.0']

setup_kwargs = {
    'name': 'bunches',
    'version': '0.1.0',
    'description': 'flexible, extensible python data structures',
    'long_description': "The goal of bunches is provide lightweight, turnkey, extensible data containers.\nbunches's framework supports a wide range of coding styles. You can create \ncomplex multiple inheritance structures with mixins galore or simpler, \ncompositional objects.\n\nThe current classes available (as bunches.ContainerThatIWant) are:\n    Listing: list-like class with 'add', 'prepend', and 'subset' methods. The\n        'add' method tries to intelligently decide whether the passed item(s)\n        to add should be appended or extended on the stored list.\n    Hybrid: list-like class that also has a full dict interface. Stored items\n        must have a 'name' attribute or allow name inference via the 'get_name'\n        function.\n    Dictionary: dict-like class with 'add' and 'subset' methods. It also \n        includes a 'default_factory' parameter providing the same functionality\n        as a defaultdict.\n    Catalog: dict-like class that allows lists of keys to be used for its\n        various methods (including dunder access methods) and supports three\n        wildcard keys: 'none', 'default', and 'all'. If lists of keys are \n        passed or the 'default' and 'all' keys are used, a list of values is\n        returned.\n    Library: dict-like class that includes two chained dicts: 'instances' and\n        'classes'. Users can deposit classes and instances in a Library and\n        they are stored and accessed intelligently. When instances are \n        deposited, it is stored in 'instances' and its class is stored in \n        'classes'.\n\nThe project is also highly documented so that users and developers and make\nbunches work with their projects. It is designed for Python coders at all \nlevels. Beginners should be able to follow the readable code and internal\ndocumentation to understand how it works. More advanced users should find\ncomplex and tricky problems addressed through efficient code.\n",
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WithPrecedent/bunches',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
