#!/usr/bin/env python3
"""VLNT website build script.."""

# Standard
import datetime
import os
import pathlib
import shutil
# External
from jinja2 import Environment, FileSystemLoader
import markdown
# Internal
from modules import config


if __name__ == '__main__':
    # Copy CSS to publish directory.
    # Makes it easier to deploy on Netlify, Render, etc. since host
    # won't need to access parent directory, e.g. ('../inc/style.css')
    publish_css = os.path.join(config.PUBLISH_DIR, config.CSS_FILE)
    shutil.copyfile(config.CSS_FILE, publish_css)

    # Initialize template system and write HTML to file
    env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))

    # Iterate through *.md files in pages/ and render HTML
    pages = pathlib.Path(config.PAGES_DIR)
    for inode in pages.iterdir():
        if inode.is_dir():
            print(config.PAGES_DIR, 'subdirectories not supported.')
        else:
            md = markdown.markdown(**CONTENT**, extensions=['meta'])

            template = env.get_template(config.TEMPLATE)
            content = template.render(
                site = config.SITE_NAME,
                desc = config.SITE_DESC,
                title = page_title,
                nav = config.NAV,
                toc = toc,
                body = body,
                template = config.TEMPLATE,
                now = datetime.datetime.now()
            )
