#!/usr/bin/env python
from setuptools import setup

setup(name='LibraryOfMind', version='0.1',
      description='A tools to shared your mind',

      author='Alan Tetich',
      author_email='alan.tetich@gmail.com',
      license='GPLv3+',
      keywords='mind keys rows share',
      url='http://github.com/alien3211/lom',

      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: X11 Applications :: GTK',
                   'Intended Audience :: Education',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Topic :: Education',
                   'Topic :: Multimedia :: Graphics :: Presentation',
                   'Topic :: Multimedia :: Video :: Capture'],

      long_description="""
      LibraryOfMind is a useful tool for save and share your mind, links, row etc. 
      """,

      scripts=['LibraryOfMind'],
      packages=['LibraryOfMind'],
      data_files=[('share/applications', ['data/libraryofmind.desktop']),
                  ('share/doc/screenkey', ['README.rst', 'NEWS.rst'])],
)
