#!/usr/bin/env python3
"""VLNT website build script.."""

# Standard
import datetime
# External
from jinja2 import Environment, fileSystemLoader
# Internal
from modules import config


if __name == '__main__':

    # Initialize template system and write HTML to file
    env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))
    template = env.get_template(config.TEMPLATE)
    content = template.render(
        title = title,
        toc = toc,
        body = body,
        template = config.TEMPLATE,
        now = datetime.datetime.now()
    )
