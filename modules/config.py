#!/usr/bin/env python3
"""Module for configuration variables."""

# Standard
import os
# External
import yaml


# Read YAML config file
with open('config.yml', encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

# Assign variables
SITE_NAME = cfg.get('site_name', 'site_name')
SITE_DESC = cfg.get('site_desc', '')
CSS_FILE = cfg.get('css_file', 'templates/style.css')
PAGES_DIR = cfg.get('pages_dir', 'pages/')
PUBLISH_DIR = cfg.get('publish_dir', 'public/')
TEMPLATES_DIR = cfg.get('templates_dir', 'templates/')

NAV = cfg.get('nav', '')

# Make directories if they don't exist
for path in [PUBLISH_DIR, TEMPLATES_DIR]:
    if not os.path.isdir(path):
        os.makedirs(path)
