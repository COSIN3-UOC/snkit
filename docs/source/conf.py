# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from unittest.mock import MagicMock

from sphinx.apidoc import main as run_apidoc

__location__ = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(__location__, "..", "..", "src"))

# mock modules which we can avoid installing for docs-building
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


mock_modules = [
    "geopandas",
    "numpy",
    "pandas",
    "shapely",
    "shapely.errors",
    "shapely.geometry",
    "shapely.ops",
]
sys.modules.update((mod_name, Mock()) for mod_name in mock_modules)


# -- Project information

project = "snkit"
copyright = "2019, Tom Russell"
author = "Tom Russell"

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = ""

try:
    from smif import __version__

    version = __version__
except ImportError:
    pass
else:
    release = version

# -- Generate API docs pages for autodoc
output_dir = os.path.join(__location__, "api")
module_dir = os.path.join(__location__, "..", "..", "src", "snkit")
templates_dir = os.path.join(__location__, "_templates")

run_apidoc(
    [
        "sphinx-apidoc",
        "-M",
        "-o",
        output_dir,
        module_dir,
        "--force",
    ]
)

# -- General configuration

# Extra styles, found in _static
def setup(app):
    app.add_stylesheet("theme_tweaks.css")


# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "m2r2",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output

# Output file base name for HTML help builder.
htmlhelp_basename = "snkitdoc"


# -- Options for LaTeX output

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "snkit.tex", "snkit Documentation", "Tom Russell", "manual"),
]


# -- Options for manual page output

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "snkit", "snkit Documentation", [author], 1)]


# -- Options for Texinfo output

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "snkit",
        "snkit Documentation",
        author,
        "snkit",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# -- Options for Epub output

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration
