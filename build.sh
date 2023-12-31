#!/bin/bash

pandoc \
--from=markdown \
--to=html \
--output=index.html \
--toc=true \
--highlight-style=kate \
--include-in-header=header.html \
--include-after-body=footer.html \
--css=style.css \
--metadata \
title="toc" \
index.md 
