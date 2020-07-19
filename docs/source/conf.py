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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from distutils.version import LooseVersion
import os
import sys
sys.path.append(os.path.abspath("./_ext"))

import sphinx_material
from recommonmark.transform import AutoStructify

FORCE_CLASSIC = os.environ.get("SPHINX_MATERIAL_FORCE_CLASSIC", False)
FORCE_CLASSIC = FORCE_CLASSIC in ("1", "true")


# -- Project information -----------------------------------------------------

project = 'Zendesk data pipeline'
html_title = "Zendesk data pipeline"
copyright = '2020, Michal Švarc'
author = 'Michal Švarc'
# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['extract_config', 'data_catalog']

# path to the config file of the project
config_file = '../pipeline/config/config.json'
data_catalog_file = '../pipeline/config/data_catalog.yaml'
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


autosummary_generate = True
autoclass_content = "class"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinx_material'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- HTML theme settings ------------------------------------------------

html_show_sourcelink = True
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

extensions.append("sphinx_material")
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
html_css_files = [
    'styles/custom.css',
]
# material theme options (see theme.conf for more information)
html_theme_options = {
    # "base_url": "http://bashtage.github.io/sphinx-material/",
    # "repo_url": "https://github.com/bashtage/sphinx-material/",
    "repo_name": "Zendesk data pipeline",
    "google_analytics_account": "UA-XXXXX",
    "html_minify": False,
    "html_prettify": True,
    "css_minify": True,
    "logo_icon": "&#xe869",
    "repo_type": "github",
    "globaltoc_depth": 2,
    "color_primary": "blue",
    "color_accent": "cyan",
    #"touch_icon": "images/apple-icon-152x152.png",
    "theme_color": "#2196f3",
    "master_doc": False,
    "nav_links": [
        {"href": "index", "internal": True, "title": "Zendesk data pipeline"}
    ],
    # "heroes": {
    #     "index": "A responsive Material Design theme for Sphinx sites.",
    #     "customization": "Configuration options to personalize your site.",
    # },
    # "version_dropdown": True,
    # "version_json": "_static/versions.json",
    # "version_info": {
    #     "Release": "https://bashtage.github.io/sphinx-material/",
    #     "Development": "https://bashtage.github.io/sphinx-material/devel/",
    #     "Release (rel)": "/sphinx-material/",
    #     "Development (rel)": "/sphinx-material/devel/",
    # },
    "table_classes": ["plain"],
}

if FORCE_CLASSIC:
    print("!!!!!!!!! Forcing classic !!!!!!!!!!!")
    html_theme = "classic"
    html_theme_options = {}
    html_sidebars = {"**": ["globaltoc.html", "localtoc.html", "searchbox.html"]}

language = "en"
html_last_updated_fmt = ""

todo_include_todos = True
#html_favicon = "images/favicon.ico"

html_use_index = True
html_domain_indices = True

nbsphinx_execute = "always"
nbsphinx_kernel_name = "python3"