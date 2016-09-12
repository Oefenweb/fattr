# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from subprocess import check_output


def readme():
  with open('README.md') as f:
    return f.read()

# This is needed because vboxvfs lacks support for symbolic / hard links and therefore make source fails
try:
  on_vagrant = (check_output(['dmidecode', '-s', 'bios-version']).strip() == 'VirtualBox')
  if on_vagrant:
    import os
    del os.link
except OSError:
  print 'Could not find dmidecode'
  pass

setup(name='fattr',
      version='0.0.1',
      author='Mischa ter Smitten',
      author_email='mtersmitten@oefenweb.nl',
      maintainer='Mischa ter Smitten',
      maintainer_email='mtersmitten@oefenweb.nl',
      url='http://www.oefenweb.nl/',
      download_url='https://github.com/Oefenweb/fattr',
      license='MIT',
      description='Save and restore file attributes from a directory tree',
      long_description=readme(),
      packages=find_packages(exclude=['test']),
      scripts=['bin/fattr'],
      platforms=['GNU/Linux'])
