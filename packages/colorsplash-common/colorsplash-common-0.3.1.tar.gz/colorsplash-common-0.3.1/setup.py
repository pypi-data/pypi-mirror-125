# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colorsplash_common']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.19.3,<2.0.0']

setup_kwargs = {
    'name': 'colorsplash-common',
    'version': '0.3.1',
    'description': 'A common set of classes for the ColorSplash project python components',
    'long_description': "# colorsplash-common\n\n## Description\n\ncolorsplash-common (CSC) is a component of the overarching ColorSplash web application that can be found at https://thurau.io/colorsplash/. ColorSplash allows users to browse royalty free images that have colors within a certain Euclidean distance of a provided HEX code. CSC is a python library hosted on PyPi to allow common features to be included as dependencies within the other python componenets.\n\nYou can see other components of this project in the following Github repos\n- [ColorSplashPhotoRetrieval](https://github.com/DanielThurau/ColorSplashPhotoRetrieval)\n- [ColorSplashPhotoProcessor](https://github.com/DanielThurau/ColorSplashPhotoProcessor)\n- [ColorSplashColorDetector](https://github.com/DanielThurau/ColorSplashColorDetector)\n- [thurau.io](https://github.com/DanielThurau/thurau.io)\n\n## Motivation\n\nA friend was facing issues when trying to create social media posts for an ecommerce company we recently launched. She had developed a branding guide and had chosen what colors she wanted to include in the website, logos, and eventual marketing material. But when it was time to make marketing posts, trying to apply that style guide was difficult. For all the tools on the internet she used, none were able to query royalty free images that were close to the HEX color codes she had selected. This project was born to remedy this issue.\n\nI wanted to provide a clean minimal interface on a website that would have a form for a HEX code, and query a REST API that would return royalty free images that had a subset of colors within close to the original HEX code.\n\n## Tech Used\n\nCSC is a very simple python library that tightly couples integration with the various DynamoDB tables in the project. It uses boto3 as the client library.\n\n## Installation\n\n### Cloning The Project\n\nYou can either fork the repo or clone it directly with\n\n```shell\n$ git clone https://github.com/DanielThurau/colorsplash-common.git\n$ cd colorsplash-common\n```\n\n### Developing\n\nThis project uses [poetry](https://python-poetry.org/) to build, test, and publish.\n\nTo install dependencies run\n\n```shell\n$ poetry install\n```\n\nTo run the unit tests run\n\n```shell\n$ poetry run pytest\n```\n\n\n## Usage\n\nCSC is hosted on PyPi so you can use any tool that integrates with PyPi to bring it in as a dependency. The easiest way is with pip. For example\n\n```shell\n$ pip install colorsplash-common\n```\n\n// TODO link a Github gist showing the use of the library\n\n## Contribute\n\nIf you'd like to contribute, fork the project and submit a Pull Request.\n\n## License\n\nSee LICENSE.md\n\n> MIT License\n>\n> Copyright (c) 2021 Daniel Thurau",
    'author': 'Daniel Thurau',
    'author_email': 'daniel.n.thurau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://thurau.io/colorsplash/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
