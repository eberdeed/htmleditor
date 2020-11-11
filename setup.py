#!/usr/bin/python3

""" A setup utility for the HTML editor.
"""
import distutils
from distutils.core import setup
from glob import glob

resfilelist = glob('htmleditor/resources/*.*')
uifilelist = glob('uifiles/*.*')
docfilelist = glob('docs/*.*')
if ('docs/docgen.py' in docfilelist):
    docfilelist.remove('docs/docgen.py')
docfilelist.append("README")
docfilelist.append('htmleditor-2.0_writeup.odt')
docfilelist.append('htmleditor-2.0_writeup.pdf')
licenselist = glob('LGPL/*.*')
    
setup(name='htmleditor',
      version='2.0',
      description='HTML Editor',
      author='Edward Charles Eberle',
      author_email='eberdeed@eberdeed.net',
      url='www.eberdeed.net',
      packages=['pyhtmleditor'],
      package_dir={'pyhtmleditor' : 'pyhtmleditor'},
      package_data={'pyhtmleditor' : ['*.*']},
      data_files=([('/usr/share/htmleditor/resources', resfilelist),
                  ('/usr/bin', ['htmleditor.py']),
                  ('htmleditor-2.0', ['README', 'uifiles.bsh', 'CHANGELOG',
                  'htmleditor-2.0_writeup.odt',
                  'htmleditor-2.0_writeup.pdf']),
                  ('htmleditor-2.0/uifiles', uifilelist),
                  ('/usr/share/doc/htmleditor-2.0-doc', docfilelist),
                  ('/usr/share/doc/htmleditor-2.0-doc/LGPL', licenselist)])
     )
