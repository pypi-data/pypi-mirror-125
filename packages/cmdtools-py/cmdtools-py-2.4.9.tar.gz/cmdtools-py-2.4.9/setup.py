# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'cmdtools'}

packages = \
['cmdtools', 'cmdtools.ext', 'ext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cmdtools-py',
    'version': '2.4.9',
    'description': 'command text parser and command processor',
    'long_description': '<div id="headline" align="center">\n  <h1>cmdtools</h1>\n  <p>A module for parsing and processing commands.</p>\n  <a href="https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml">\n    <img src="https://github.com/HugeBrain16/cmdtools/actions/workflows/python-package.yml/badge.svg" alt="tests"></img>\n  </a>\n  <a href="https://pypi.org/project/cmdtools-py">\n    <img src="https://img.shields.io/pypi/dw/cmdtools-py" alt="downloads"></img>\n    <img src="https://badge.fury.io/py/cmdtools-py.svg" alt="PyPI version"></img>\n    <img src="https://img.shields.io/pypi/pyversions/cmdtools-py" alt="Python version"></img>\n  </a>\n  <a href="https://codecov.io/gh/HugeBrain16/cmdtools">\n    <img src="https://codecov.io/gh/HugeBrain16/cmdtools/branch/main/graph/badge.svg?token=mynvRn223H"/>\n  </a>\n  <a href=\'https://cmdtools-py.readthedocs.io/en/latest/?badge=latest\'>\n    <img src=\'https://readthedocs.org/projects/cmdtools-py/badge/?version=latest\' alt=\'Documentation Status\' />\n  </a>\n</div>\n\n## Installation\n\n```\npip install --upgrade cmdtools-py\n```\ninstall latest commit from GitHub  \n```\npip install git+https://github.com/HugeBrain16/cmdtools.git\n```\n## Examples\n\nmore examples [here](https://github.com/HugeBrain16/cmdtools/tree/main/examples)\n\n### Basic example\n\n```py\nimport cmdtools\n\n\ndef ping():\n    print("pong.")\n\n\ncmd = cmdtools.Cmd(\'/ping\')\ncmd.process_cmd(ping)\n```\n  \n### Command with arguments\n\n```py\nimport cmdtools\n\n\ndef give(name, item_name, item_amount):\n    print(f"You gave {item_amount} {item_name}s to {name}")\n\n\n# surround argument that contains whitespaces with quotes\n# set `convert_args` to `True` to automatically convert numbers argument\n\n# this will raise an exception,\n# if the number of arguments provided is less than the number of positional callback parameters.\ncmd = cmdtools.Cmd(\'/give Josh "Golden Apple" 10\', convert_args=True)\n\n# check for command instance arguments data type.\n# format indicates [\'str\',\'str\',\'int\'].\n# integer or float can also match string format, and character \'c\' if the argument only has 1 digit.\n\n# `max_args` set to 3, check the first 3 arguments, the rest will get ignored, \n# otherwise if it set to default,\n# it will raise an exception if the number of arguments is not equal to the number of formats\nif cmd.match_args(\'ssi\', max_args=3):\n    cmd.process_cmd(give)\nelse:\n    print(\'Correct Usage: /give <name: [str]> <item-name: [str]> <item-amount: [int]>\')\n```\n\n## Links\n\nPyPI project: https://pypi.org/project/cmdtools-py  \nSource code: https://github.com/HugeBrain16/cmdtools  \nIssues tracker: https://github.com/HugeBrain16/cmdtools/issues  \nDocumentation: https://cmdtools-py.readthedocs.io/en/latest\n',
    'author': 'HugeBrain16',
    'author_email': 'joshtuck373@gmail.com',
    'maintainer': 'HugeBrain16',
    'maintainer_email': 'joshtuck373@gmail.com',
    'url': 'https://github.com/HugeBrain16/cmdtools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
