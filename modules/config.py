#!/usr/bin/env python3
"""Module for configuration variables."""

# Standard
import os
# External
from jinja2 import Environment, FileSystemLoader
import yaml


# Read YAML config file
with open('config.yml', encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

# Assign variables
CSS_FILE = cfg.get('css_file', 'style.css')
INCLUDES_DIR = cfg.get('includes_dir', 'includes/')
NAV = cfg.get('nav', '')
PAGES_DIR = cfg.get('pages_dir', 'pages/')
PUBLISH_DIR = cfg.get('publish_dir', 'public/')
SITE_DESC = cfg.get('site_desc', '')
SITE_NAME = cfg.get('site_name', 'site_name')
TEMPLATE = cfg.get('template', 'page.html')
TEMPLATES_DIR = cfg.get('templates_dir', 'templates/')

ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Make directories if they don't exist
for path in [PUBLISH_DIR, TEMPLATES_DIR]:
    if not os.path.isdir(path):
        os.makedirs(path)
