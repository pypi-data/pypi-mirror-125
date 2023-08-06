# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sentinel_value']
setup_kwargs = {
    'name': 'sentinel-value',
    'version': '0.0.10',
    'description': 'Sentinel Values - unique objects akin to None, True, False',
    'long_description': 'sentinel-value\n==============\n\n|pypi badge| |build badge| |docs badge|\n\n**Warning!**\n\n**The code is at the early development stage, and may be unstable. Use with caution.**\n\nLinks\n-----\n\n- Read the Docs: https://sentinel-value.readthedocs.io\n- GitHub repository: https://github.com/vdmit11/sentinel-value\n- Python package: https://pypi.org/project/sentinel-value/\n\n\n.. |pypi badge| image:: https://img.shields.io/pypi/v/sentinel-value.svg\n  :target: https://pypi.org/project/sentinel-value/\n  :alt: Python package version\n\n.. |build badge| image:: https://github.com/vdmit11/sentinel-value/actions/workflows/build.yml/badge.svg\n  :target: https://github.com/vdmit11/sentinel-value/actions/workflows/build.yml\n  :alt: Tests Status\n\n.. |docs badge| image:: https://readthedocs.org/projects/sentinel-value/badge/?version=latest\n  :target: https://sentinel-value.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n',
    'author': 'Dmitry Vasilyanov',
    'author_email': 'vdmit11@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vdmit11/sentinel-value',
    'py_modules': modules,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
