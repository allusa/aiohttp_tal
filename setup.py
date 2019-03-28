#!/usr/bin/env python
import os
from distutils.core import setup


version = '0.1-dev'


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='aiohttp-tal',
      version=version,
      description=("TAL template renderer for aiohttp.web "
                   "(http server for asyncio)"),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Development Status :: 5 - Production/Stable',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: AsyncIO',
      ],
      author='Aleix Llusà Serra',
      author_email='timbaler@timbaler.cat',
      url='https://github.com/allusa/aiohttp_tal/',
      license='GPLv3+',
      packages=['aiohttp_tal'],
      python_requires='>=3.5.3',
      install_requires=[
        'aiohttp>=3.2.0',
        'chameleon',
        ],
      extras_require={
        'test': [
            'sphinx',
            'pytest-aiohttp',
            'pytest-cov',
            'pytest-flake8',
            'flake8-isort',
          ],
      },
      data_files=['README.rst', 'CHANGES.txt', 'LICENSE'],
      include_package_data=True
      )
