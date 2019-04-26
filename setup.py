from setuptools import setup, find_packages

from aurora import __version__

setup(name='aurora',
      version=__version__,
      packages=find_packages(),
      entry_points={
          'console_scripts': ['aurora = aurora.cli:cli']
      })
