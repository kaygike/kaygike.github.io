#!/bin/bash
#
# Convert pages/*.md to /*.html using custom stylesheet & template

# List of filenames (without extension)
declare -a arr=("index" "books" "code" "other" "quotes" "text")

for i in "${arr[@]}"
do
    echo "Generating $i.html"
    pandoc \
    --from=markdown \
    --to=html \
    --output=$i.html \
    --toc=true \
    --highlight-style=kate \
    --css=include/style.css \
    --template=include/html-template.pandoc \
    --metadata \
    title="$i" \
    pages/$i.md
done
