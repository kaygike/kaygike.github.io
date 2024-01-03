#!/bin/bash
#
# Concatenate *.md files in pages/ then build index.html with
# - table of contents
# - code syntax highlighting
# - header.html prefix and footer.html suffix
# - custom stylesheet



pandoc \
--from=markdown \
--to=html \
--output=index.html \
--toc=true \
--highlight-style=kate \
--include-in-header=include/header.html \
--include-after-body=include/footer.html \
--css=include/style.css \
--metadata \
title="Kaygike" \
pages/index.md
