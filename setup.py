from setuptools import find_packages, setup

from aurora import __version__


with open('README.md') as f:
    long_description = f.read()

setup(name='aurora',
      version=__version__,
      packages=find_packages(),
      install_requires=[
          'jinja2>=2.10',
          'mistune>=0.8.4',
          'docopt>=0.6.2',
      ],
      entry_points={
          'console_scripts': ['aurora = aurora.cli:cli']
      },
      author='Thomas Ip',
      author_email='hkmp7tommy@gmail.com',
      description='Aurora is a minimalist, blog-aware static site generator.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      keywords='blog static-site-generator jinja2 markdown',
      url='https://github.com/tommyip/aurora',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
      ])
