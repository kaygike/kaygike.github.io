#!/usr/bin/env python3

# Standard
import datetime
import os
import pathlib
import shutil
# External
import frontmatter
import markdown
# Internal
from modules import config

def build_template(env, data):
    """Return full rendered HTML from template and page data."""
    template = env.get_template(config.TEMPLATE)
    content = template.render(
        site = config.SITE_NAME,
        desc = config.SITE_DESC,
        title = data.get('page_title'),
        nav = config.NAV,
        toc = data.get('toc'),
        body = data.get('html'),
        template = config.TEMPLATE,
        now = datetime.datetime.now()
    )
    return content


def copy_includes_to_public_dir():
    """Copy CSS file from INCLUDES_DIR to PUBLISH_DIR."""
    inc_css = os.path.join(config.INCLUDES_DIR, config.CSS_FILE)
    pub_css = os.path.join(config.PUBLISH_DIR, config.CSS_FILE)
    shutil.copyfile(inc_css, pub_css)

def get_page_data():
    """Yield dxnry of contents in *.md files in PAGES_DIR."""
    for inode in pathlib.Path(config.PAGES_DIR).iterdir():
        if inode.is_dir():
            print(config.PAGES_DIR, 'subdirectories not supported.')
            break

        with open(inode, 'r', encoding='utf-8') as f:
            data = f.read()
            fm = frontmatter.loads(data)
            md = markdown.Markdown(extensions=[
                                                'meta',
                                                'toc',
                                                'codehilite',
                                                'fenced_code'
                                             ]
            )        
            dxnry = {
                        'html': md.convert(data),
                        'inode': inode,
                        'page_title': fm.get('title', inode),
                        'toc': md.toc,
                    }
            yield dxnry

def write_html_to_file(data, render):
    """Write content to file in PUBLISH_DIR."""
    inode = data.get('inode')
    fname = pathlib.Path(inode).stem + ".html"
    fpath = config.PUBLISH_DIR + os.path.basename(fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(render)
