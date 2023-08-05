# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diskcsvsort', 'diskcsvsort.cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'diskcsvsort',
    'version': '0.1.1',
    'description': 'Sort huge csv files.',
    'long_description': "# Disk CSV Sort\n\n[![Supported Versions](https://img.shields.io/badge/python-3.10%2B-blue)](https://shields.io/)\n\n## Description\n\nSort huge CSV files using disk space and RAM together.\n\nFor now support only CSV files with **header**.\n\n## Usage\n\n### For example\n\n---\n\n#### CSV file with movies\n\n| name              | year |\n|-------------------|------|\n| Batman Begins     | 2005 |\n| Blade Runner 2049 | 2017 |\n| Dune              | 2021 |\n| Snatch            | 2000 |\n\nSort this CSV file that stored in `movies.csv` by `year` and `name`.\n\n**Note**: _order of columns is matter during sorting._\n\n---\n\n### Using diskcsvsort package\n```python\nfrom pathlib import Path\nfrom diskcsvsort import CSVSort\n\ncsvsort = CSVSort(\n    src=Path('movies.csv'),\n    key=lambda row: (int(row['year']), row['name']),\n)\ncsvsort.apply()\n\n```\n\n### Using diskcsvsort CLI\n\n    python -m diskcsvsort movies.csv --by year:int --by name:str\n\n**Note**: columns `year` and `name` will be converted to `int` and `str`, respectively.\n\n#### Available types:\n - str\n - int\n - float\n - datetime\n - date\n - time\n\n#### Types usage:\n- str: `column:str` \n- int: `column:int` \n- float: `column:float` \n- datetime: `column:datetime(%Y-%m-%d %H:%M:%S)`\n- date: `column:datetime(%Y-%m-%d)`\n- time: `column:datetime(%H:%M:%S)`\n\n\n## Algorithm\nTODO\n\n\n## Metrics\nTODO\n",
    'author': 'volodymyrb',
    'author_email': 'volodymyr.borysiuk0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VolodymyrBor/diskcsvsort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
