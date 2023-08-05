# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weni',
 'weni.analytics_api',
 'weni.auth',
 'weni.channel_stats',
 'weni.grpc.billing',
 'weni.grpc.channel',
 'weni.grpc.classifier',
 'weni.grpc.core',
 'weni.grpc.core.management',
 'weni.grpc.core.management.commands',
 'weni.grpc.flow',
 'weni.grpc.org',
 'weni.grpc.statistic',
 'weni.grpc.user',
 'weni.template_message',
 'weni.templates',
 'weni.utils']

package_data = \
{'': ['*']}

install_requires = \
['django-csp>=3.7,<4.0',
 'django-environ>=0.7.0,<0.8.0',
 'django-templates-macros>=0.2,<0.3',
 'djangogrpcframework>=0.2.1,<0.3.0',
 'elastic-apm>=6.4.0,<7.0.0',
 'flower>=0.9,<0.10',
 'mozilla-django-oidc>=2.0.0,<3.0.0',
 'weni-protobuffers>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'weni-rp-apps',
    'version': '1.0.2',
    'description': 'Weni apps for Rapidpro Platform',
    'long_description': None,
    'author': 'jcbalmeida',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
