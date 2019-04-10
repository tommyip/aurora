from setuptools import setup, find_packages

from icarus import __version__

setup(name='icarus',
      version=__version__,
      packages=find_packages(),
      entry_points={
          'console_scripts': ['icarus = icarus.cli:cli']
      })
