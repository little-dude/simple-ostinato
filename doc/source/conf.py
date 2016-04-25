# -*- coding: utf-8 -*-
#
import sys
import os
import shlex
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks'
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'simple-ostinato'
copyright = u'2016, Corentin Henry'
author = u'Corentin Henry'
version = '0.0.1'
release = '0.0.1'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
htmlhelp_basename = 'simple-ostinatodoc'
intersphinx_mapping = {'https://docs.python.org/': None}
