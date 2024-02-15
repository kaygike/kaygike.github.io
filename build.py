#!/usr/bin/env python3
"""VLNT website build script.."""

# Standard
import datetime
import os
import shutil
# External
from jinja2 import Environment, fileSystemLoader
# Internal
from modules import config


if __name == '__main__':
    # Copy CSS to publish directory.
    # Makes it easier to deploy on Netlify, Render, etc. since host won't need
    # to access parent directory, e.g. ('../inc/style.css')
    templates_css = os.path.join(config.TEMPLATES_DIR, config.CSS_FILE)
    publish_css = os.path.join(config.PUBLISH_DIR, config.CSS_FILE)
    shutil.copyfile(teampltes_css, publish_css)

    # Initialize template system and write HTML to file
    env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))
    template = env.get_template(config.TEMPLATE)
    content = template.render(
        site = config.SITE_NAME,
        desc = config.SITE_DESC,
        title = page_title,
        nav = config.NAV
        toc = toc,
        body = body,
        template = config.TEMPLATE,
        now = datetime.datetime.now()
    )
