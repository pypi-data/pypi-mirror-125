# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['avgangstider']

package_data = \
{'': ['*'],
 'avgangstider': ['static/*',
                  'static/css/*',
                  'static/fonts/Din/*',
                  'templates/*']}

install_requires = \
['flask>=1.1,<2.0', 'requests>=2.22,<3.0']

extras_require = \
{'gunicorn': ['gunicorn>=20.0,<21.0']}

setup_kwargs = {
    'name': 'avgangstider',
    'version': '0.1.2',
    'description': 'Avgangstider fra EnTur',
    'long_description': None,
    'author': 'Martin Høy',
    'author_email': 'marhoy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
