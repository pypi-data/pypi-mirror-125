# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_locations',
 'simple_locations.management',
 'simple_locations.management.commands',
 'simple_locations.migrations']

package_data = \
{'': ['*'],
 'simple_locations': ['fixtures/*',
                      'locale/fr/LC_MESSAGES/*',
                      'static/css/*',
                      'static/images/*',
                      'static/javascripts/*',
                      'static/uni_form/*',
                      'templates/simple_locations/*',
                      'templates/simple_locations/admin/*']}

install_requires = \
['django-mptt>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'simple-locations',
    'version': '2.78',
    'description': "The common location package for Catalpa's projects",
    'long_description': None,
    'author': 'Joshua Brooks',
    'author_email': 'josh.vdbroek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
