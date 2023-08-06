# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_prometheus_sd',
 'netbox_prometheus_sd.api',
 'netbox_prometheus_sd.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netbox-plugin-prometheus-sd',
    'version': '0.1.0rc1',
    'description': 'A Netbox plugin to provide Netbox entires to Prometheus HTTP service discovery',
    'long_description': None,
    'author': 'Felix Peters',
    'author_email': 'felix.peters@breuninger.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
