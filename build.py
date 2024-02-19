#!/usr/bin/env python3
"""VLNT website build script.."""

# Standard
import datetime
import os
import pathlib
import pprint
import shutil
# External
from jinja2 import Environment, FileSystemLoader
import frontmatter
import markdown
# Internal
from modules import config


if __name__ == '__main__':
    # Copy CSS file from 'includes' dir to 'public' dir
    # (So hosts won't need to access parent directory)
    inc_css = os.path.join(config.INCLUDES_DIR, config.CSS_FILE)
    pub_css = os.path.join(config.PUBLISH_DIR, config.CSS_FILE)
    shutil.copyfile(inc_css, pub_css)

    # Initialize template system and write HTML to file
    env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))

    # Iterate through *.md files in pages/ and render HTML
    pages = pathlib.Path(config.PAGES_DIR)
    for inode in pages.iterdir():
        if inode.is_dir():
            print(config.PAGES_DIR, 'subdirectories not supported.')
        else:
            with open(inode, 'r', encoding='utf-8') as f:
                # Read *.md frontmatter and content
                data = f.read()
                fm = frontmatter.loads(data)
                mdown = markdown.markdown(data, extensions=['meta'])
                
                page_title = fm.get('title', inode)
                pprint.pprint(page_title)

                template = env.get_template(config.TEMPLATE)
                content = template.render(
                    site = config.SITE_NAME,
                    desc = config.SITE_DESC,
                    title = page_title,
                    nav = config.NAV,
                    #toc = toc,
                    body = mdown,
                    template = config.TEMPLATE,
                    now = datetime.datetime.now()
                )


                fname = pathlib.Path(inode).stem + ".html"
                fpath = config.PUBLISH_DIR + os.path.basename(fname)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
