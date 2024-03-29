---
title: Code
---

## 7z

Create archive w/ no compression and encrypted filenames.

```bash
$ 7z a -p -bt -mx=0 -mhe=on archive.7z file1 file2 file3</code>
````

## bdfr

Bulk archive a subreddit.

> Two separate operations shown below.

```bash
$ bdfr clone ~/save_dir/ --subreddit unixporn --log ~/save_dir/log.log --sort top --time all --make-hard-links --file-scheme "{DATE}_{POSTID}_{UPVOTES}"

$ bdfr clone ~/save_dir/ --subreddit unixporn --log ~/save_dir/log.log --make-hard-links --folder-scheme "{DATE}_{TITLE}_{POSTID}_{UPVOTES}" --file-scheme "{UPVOTES}_{DATE}_{REDDITOR}_{POSTID}
```

## ffmpeg

Convert APE to FLAC.

```bash
$ fmpeg -i INPUT.ape OUTPUT.flac
```

Convert all m4a to FLAC and preserve filenames.

```bash
$ for f in *.m4a; do ffmpeg -i "$f" "${f%.m4a}".flac; done
```

Merge multiple files into one without re-encoding.

> Specific format for CONCAT.txt file

```bash
$ cat CONCAT.txt
file '/path/to/file1'
file '/path/to/file2'

$ ffmpeg -f concat -safe 0 -i CONCAT.txt -c copy output.mp4
```

## git

Managing multiple usernames.

> 1. Setup ```~/.ssh/config```  using e.g. ```Host github.com-user1``` and ```Host github.com-user2```. ([source](https://www.howtogeek.com/devops/how-to-fix-git-using-the-wrong-ssh-key-account/))

> 2. Setup remote origins to use the above dummy hosts, e.g. ```git remote set-url origin git@github.com-user1:user1/reponame.git```. ([source](https://stackoverflow.com/questions/2432764/how-do-i-change-the-uri-url-for-a-remote-git-repository))

## md5sum

List duplicate files in directory. ([source](https://unix.stackexchange.com/questions/277697/whats-the-quickest-way-to-find-duplicated-files/277707#277707))

```bash
$ find . ! -empty -type f -exec md5sum {} + | sort | uniq -w32 -dD
```

Create file with md5 checksums for all FLAC in directories (one-deep).

```bash
$ for dir in *; do if [ -d $dir -a ! -h $dir ]; then cd -- "$dir"; echo "Generating md5sum for '$dir'"; md5sum *.flac > checksum.md5; cd .. ; fi; done;
```

## mises.py

Scrape pdfs from Mises Institute's digital library.

> Requires beautifulsoup.

> Update range of forloop as needed.

> For epub, use url ```book_type=537``` and change ```pdf``` to ```epub``` in script.

```python
#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime
import os.path
import re
import requests

url = "https://mises.org/library/books?book_type=539"

def surname_forename(text):
    if "Jr." in text:
        surname = text.split()[-2]
        forename = "".join(text.split()[0:-2]) + text.split()[-1]
    else:
        surname = text.split()[-1]
        forename = text.rsplit(" ", 1)[0]
    return surname + forename

def restrict_filename(text):
    return "".join(t for t in text if t.isalnum())

def scrape_page(soup):
    entries = soup.find_all("div", {"class": re.compile("^result-*")})
    for entry in entries:
        scrape_entry(entry)

def scrape_entry(entry):
    title = entry.find("h2", {"class": "teaser-title"}).get_text()
    author = entry.find("span", {"class": "author"}).get_text()
    date = entry.find("span", {"class": "date"}).get_text()
    pdf = entry.find("a", {"type": re.compile(r"pdf")})["href"]

    title = restrict_filename(title)
    author = surname_forename(author)
    author = restrict_filename(author)
    date = datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")

    download_entry(title, author, date, pdf)

def download_entry(title, author, date, pdf):
    filename =  author + "_" + title + "_" + date + ".pdf"
    if os.path.isfile(filename):
        print("Already downloaded " + filename)
    else:
        print("Downloading " + filename)
        dl = requests.get(pdf)
        with open(filename, 'wb') as f:
            f.write(dl.content)

for p in range(1,57):
    # adjust max page range above as necessary
    req = requests.get(url + "&page=" + str(p))
    soup = BeautifulSoup(req.content, "lxml")
    print("Scraping page " + str(p))
    scrape_page(soup)
```

## pacman

Find install location of package.

```bash
$ pacman -Fql <PACKAGENAME> | grep -E "^usr/bin.+"
```

## podcast-dl

Download audio w/ metadata from RSS feed.

```bash
$ npx podcast-dl --url <rss url> --episode-template "{{release_date}} {{title}}" --archive archive.archive --include-meta --include-episode-meta --out-dir "."
```

## rsync

Mirror directory to another location and log to file.

> Requires backslashes at end of directories.

> Remove --dry-run to execute; '--delete' used to mirror directory contents.

```bash
$ rsync --dry-run --archive --human-readable --itemize-changes --verbose --exclude="lost+found" --delete FILES_TO_COPY/ WHERE_TO_COPY_TO/ | tee ~/DATE_rsync.log
```

## shnsplit

Split and tag flac FLAC via cuesheet.

> Requires cuesheet.sh, trash-cli to delete pregap file, and no more than 1 flac file and 1 cue file in directory.

```bash
$ shnsplit -f *.cue -t %n_%t -o flac *.flac; if [ -f "00_pregap.flac" ]; then trash 00_pregap.flac; fi; cuetag.sh *.cue [0-9]*.flac
```

The above, but recursively through subdirectories.

```bash
$ for d in */ ; do cd "$d"; pwd; shnsplit -f *.cue -t %n_%t -o flac *.flac; if [ -f "00_pregap.flac" ]; then trash 00_pregap.flac; fi; cuetag.sh *.cue [0-9]*.flac; cd ..; done
```

## wget

Download numerical increments.

```bash
$ wget https://domain.tld/path/to/files/file{1..100}.filetype
```

Download numerical & alphabetical increments.

```bash
#! /bin/bash
# Downloads file01a.ext, file01b.ext... file12f.ext, etc.
HREF="protocol://domain.tld/path/to/files/file"
TENS=0
ONES=0
LETTER=A
EXT=".EXT"
URL="$URL$TENS$ONES$LETTER$EXT"
print $URL
for (( i = 0; i<= 9; i++ ))
  do
    for (( j = 0; j<= 9; j++ ))
      do
        for letter in {a..z}
          do
            URL="$HREF$i$j$letter$EXT"
            echo $URL
            wget $URL
          done
      done
  done
```

Download specific filetype/extensions.

```bash
$ wget --directory-prefix=path/to/save --no-directories --recursive --level=1 --span-hosts --domains=https://domain.tld --accept ext1,ext2,ext3 https://domain.tld/path/to/files
```

## yt-dlp

Download video with metadata file.

> use ```--batch-file FILE``` to use a text file with urls

```bash
$ yt-dlp --add-metadata --write-info-json --restrict-filenames --output "%(title)s_%(upload_date)s_%(id)s.%(ext)s" http://video.url/id
```
