#!/usr/bin/env python3
"""VLNT website build script."""

# Internal
from modules import config
from modules import fn


if __name__ == '__main__':
    # Copy CSS file from 'includes' dir to 'public' dir
    # (So hosts won't need to access parent directory)
    fn.copy_includes_to_public_dir()

    # Render markdown files to HTML via jinja
    for data in fn.get_page_data():
        render = fn.build_template(config.ENV, data)
        fn.write_html_to_file(data, render)
