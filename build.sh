#!/bin/bash

pandoc \
--from=markdown \
--to=html \
--output=index.html \
--toc=true \
--include-in-header=header.html \
--include-after-body=footer.html \
--css=style.css \
--metadata \
title="toc" \
index.md 
