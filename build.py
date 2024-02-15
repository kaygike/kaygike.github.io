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
    css_basename = os.path.basename(config.CSS_PATH)
    destination = os.path.join(config.PUBLISH_DIR, css_basename)
    shutil.copyfile(config.CSS_PATH, destination)

    # Initialize template system and write HTML to file
    env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))
    template = env.get_template(config.TEMPLATE)
    content = template.render(
        site = config.SITE_NAME,
        desc = config.SITE_DESC,
        title = page_title,
        toc = toc,
        body = body,
        template = config.TEMPLATE,
        now = datetime.datetime.now()
    )
