---
title: About
---

## Sitemap

* [Books](books.html) - Book synopses, written to enhance the author's retention.
* [Code](code.html) - Programming code and scripts, mostly for Linux environments.
* [Other](other.html) - Whatever doesn't fit elsewhere.
* [Quotes](quotes.html) - Quotes of interest from various writers and orators.
* [Text](text.html) - Short essays or writings on miscellaneous topics.

## Tech Stack

Webpages are edited in plain text using [Markdown](https://en.wikipedia.org/wiki/Markdown) syntax.

A small [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) script is run to recursively convert the Markdown files to HTML using [Pandoc](https://en.wikipedia.org/wiki/Pandoc). A custom Pandoc [Template](https://pandoc.org/MANUAL.html#templates) is used to define the HTML structure, and all accompanying CSS and images were made from scratch.

All files are committed to a [Git](https://en.wikipedia.org/wiki/Git) repository, and the HTML files generated via Pandoc are served directly from there.
