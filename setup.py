# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil
shutil.copy('README.md', 'simpleplot/README.md')

dir_setup = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_setup, 'simpleplot', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

setup(name='simpleplot',
      version=__version__,
      description='Simple plot line and scatter plot functions. Built around matplotlib.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['simpleplot'],
      package_data={'simpleplot': ['README.md']}
     )
