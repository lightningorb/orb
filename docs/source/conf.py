# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-11 07:13:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-05 07:58:41
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
from orb.misc.monkey_patch import fix_annotations

fix_annotations()

sys.path.insert(0, os.path.abspath("../../"))
sys.path.insert(0, os.path.abspath("../../orb/lnd"))
sys.path.insert(0, os.path.abspath("../../orb/lnd/grpc_generated/v0_15_0_beta"))

for p in (Path("../../third_party")).glob("*"):
    sys.path.append(os.path.abspath(p.as_posix()))

# -- Project information -----------------------------------------------------

project = "orb"
copyright = "2022, lnorb.com"
author = "lnorb.com"

# The full version, including alpha/beta/rc tags
release = open("../../VERSION").read().strip()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinxcontrib.asciinema",
    "sphinxcontrib.mermaid",
]

sphinxcontrib_asciinema_defaults = {
    "theme": "python",
    "cols": 120,
    "idle_time_limit": 0.6,
    "rows": 20,
    "preload": 1,
    "autoplay": 1,
    "font-size": "15px",
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# html_extra_path = ["static"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster"
# html_theme = "karma_sphinx_theme"
# html_theme = "sphinxawesome_theme"
# html_theme = "karma_sphinx_theme"
# html_permalinks_icon = "<span>#</span>"
# html_permalinks_icon = "<span>#</span>"

html_theme = "python_docs_theme"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["custom.css"]
html_favicon = "_static/orb_transparent_small.png"
coverage_show_missing_items = True

html_theme_options = {}

html_show_sphinx = False

rst_prolog = """
.. |br| raw:: html

  <br/>
"""
