#!/usr/bin/env python3
"""VLNT website build script.."""

# External
from jinja2 import Environment, FileSystemLoader
# Internal
from modules import config
from modules import fn


if __name__ == '__main__':
    # Copy CSS file from 'includes' dir to 'public' dir
    # (So hosts won't need to access parent directory)
    fn.copy_includes_to_public_dir()

    # Initialize template system and write HTML to file
    env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))

    # Render markdown files to HTML via jinja
    for data in fn.get_page_data():
        render = fn.build_template(env, data)
        fn.write_html_to_file(data, render)
