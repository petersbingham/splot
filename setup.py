# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil
shutil.copy('README.md', 'splot/README.md')

dir_setup = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_setup, 'splot', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

setup(name='splot',
      version=__version__,
      description='Simple plot line and scatter plot functions. Built around matplotlib.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['splot'],
      package_data={'splot': ['README.md']}
     )
