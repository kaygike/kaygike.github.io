## CMDs

### 7z

Create archive w/ no compression and encrypted filenames.

```bash
$ 7z a -p -bt -mx=0 -mhe=on archive.7z file1 file2 file3</code>
````

### bdfr

Bulk archive a subreddit.

> Two separate operations shown below.

```bash
$ bdfr clone ~/save_dir/ --subreddit unixporn --log ~/save_dir/log.log --sort top --time all --make-hard-links --file-scheme "{DATE}_{POSTID}_{UPVOTES}"

$ bdfr clone ~/save_dir/ --subreddit unixporn --log ~/save_dir/log.log --make-hard-links --folder-scheme "{DATE}_{TITLE}_{POSTID}_{UPVOTES}" --file-scheme "{UPVOTES}_{DATE}_{REDDITOR}_{POSTID}
```

### ffmpeg

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

### git

Managing multiple usernames.

> 1. Setup ```~/.ssh/config```  using e.g. ```Host github.com-user1``` and ```Host github.com-user2```. ([source](https://www.howtogeek.com/devops/how-to-fix-git-using-the-wrong-ssh-key-account/))

> 2. Setup remote origins to use the above dummy hosts, e.g. ```git remote set-url origin git@github.com-user1:user1/reponame.git```. ([source](https://stackoverflow.com/questions/2432764/how-do-i-change-the-uri-url-for-a-remote-git-repository))

### md5sum

List duplicate files in directory. ([source](https://unix.stackexchange.com/questions/277697/whats-the-quickest-way-to-find-duplicated-files/277707#277707))

```bash
$ find . ! -empty -type f -exec md5sum {} + | sort | uniq -w32 -dD
```

Create file with md5 checksums for all FLAC in directories (one-deep).

```bash
$ for dir in *; do if [ -d $dir -a ! -h $dir ]; then cd -- "$dir"; echo "Generating md5sum for '$dir'"; md5sum *.flac > checksum.md5; cd .. ; fi; done;
```

### pacman

Find install location of package.

```bash
$ pacman -Fql <PACKAGENAME> | grep -E "^usr/bin.+"
```

### podcast-dl

Download audio w/ metadata from RSS feed.

```bash
$ npx podcast-dl --url <rss url> --episode-template "{{release_date}} {{title}}" --archive archive.archive --include-meta --include-episode-meta --out-dir "."
```

### rsync

Mirror directory to another location and log to file.

> Requires backslashes at end of directories.

> Remove --dry-run to execute; '--delete' used to mirror directory contents.

```bash
$ rsync --dry-run --archive --human-readable --itemize-changes --verbose --exclude="lost+found" --delete FILES_TO_COPY/ WHERE_TO_COPY_TO/ | tee ~/DATE_rsync.log
```

### shnsplit

Split and tag flac FLAC via cuesheet.

> Requires cuesheet.sh, trash-cli to delete pregap file, and no more than 1 flac file and 1 cue file in directory.

```bash
$ shnsplit -f *.cue -t %n_%t -o flac *.flac; if [ -f "00_pregap.flac" ]; then trash 00_pregap.flac; fi; cuetag.sh *.cue [0-9]*.flac
```

The above, but recursively through subdirectories.

```bash
$ for d in */ ; do cd "$d"; pwd; shnsplit -f *.cue -t %n_%t -o flac *.flac; if [ -f "00_pregap.flac" ]; then trash 00_pregap.flac; fi; cuetag.sh *.cue [0-9]*.flac; cd ..; done
```

### wget

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

### yt-dlp

Download video with metadata file.

> use ```--batch-file FILE``` to use a text file with urls

```bash
$ yt-dlp --add-metadata --write-info-json --restrict-filenames --output "%(title)s_%(upload_date)s_%(id)s.%(ext)s" http://video.url/id
```

## Bookmarks

### 'awesome' lists

* [cli](https://github.com/agarrharr/awesome-cli-apps)
* [datahoarding](https://github.com/simon987/awesome-datahoarding)
* [python libs](https://github.com/vinta/awesome-python)
* [self-hosted](https://github.com/awesome-selfhosted/awesome-selfhosted)
* [tui](https://github.com/rothgar/awesome-tuis)

### Literature

* [anna's archive](https://annas-archive.org)
* [libgen](https://libgen.is)

### Magnets

* [bitsearch](https://bitsearch.to)
* [bt4g](https://bt4gprx.com)
* [btdigg](https://btdig.com)
* [snowfl](https://snowfl.com)

## Scripts

### mises.py

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


## Writing

### Excel best practices

Below are five (5) core tenets for using Excel or other spreadsheet software, in no particular order:

#### Comprehensibility

> The quicker your workbook can be comprehended by others, the better.

For comprehensibility, you should document what’s happening on each worksheet and try to avoid using excessively complex formulas. This might mean you use “helper” columns or rows to accomplish your task across multiple cells instead of using a long formula that’s difficult to audit.

Your worksheets should be ordered by importance from left-to-right, going from a table of contents sheet (if necessary), to output sheets (executive summary), to input sheets (which drive the model), to calculation sheets (which do the heavy lifting). Also, reset all worksheets to the A1 cell and select the leftmost worksheet before closing the workbook.

Fonts should have monospace numbers so periods and commas align within each column. This probably also requires you to select certain cell formatting to keep everything aligned. Eventually, the bottom of this article will provide details on how to keep the periods, commas, and parenthesis aligned for dollar amounts, integers, and percentages.

```
  10,000.00
  (4,000.00)
    (300.00)
   5,700.50
      25.50%     
```

#### Compatability

> Models should function regardless of software settings – or specify the needs

The model should work regardless of the version of Excel or its settings.

Generally speaking, it’s fine to use newer functions instead of legacy ones to preserve compatibility. One of the main settings that may break a model when shared with another user, for example, is that the creator has Iterative Calculation enabled whereas the other does not. This is of particular interest for the core financial statements, where the projected pro forma Balance Sheets carry a cash & equivalents value which increases (usually at the risk-free rate) on the Income Statement, while the Income Statement generates returns based on the Balance Sheet. The Income Statement is (in part) being generated by the Balance Sheet, and the Balance Sheet is (in part) being driven by the Income Statement.

The Iterative Calculation setting can usually resolve these circular references, but if another user doesn’t have that setting enabled, then the pro forma statements won’t balance. Unfortunately, in such a case, the best available workaround is to write a macro which resolves the circular reference, but then the other user needs to run code which they may not have audited.

Given these constraints, the creator needs to either clearly specify the software setting required for the model to function, or convince the other user to run the (unaudited) macro.

#### Internal Consistency

> Do similar things the same way.

For legibility, perform similar actions using the same method or styling each time.

```
  Do this:      Not this:
  ____A____     ____A_____
1| =1         1| =1
2| =A1 + 1    2| =A1 + 1
3| =A2 + 1    3| =A2 * 1.5
4| =A3 + 1    4| =2 + 2
5| =A4 + 1    5| =sqrt(25)
```

#### Function over Form

> Emphasize accuracy over beauty.

It’s always better to have an ugly working model than a beautiful broken model, and text colors should help identify inputs, outputs, and dependencies.

* Black text should be used for plain text, formulas, and cell references on the same worksheet. It shouldn’t need to be modified, as it simply outputs or calculates results.

* Blue text indicates an input or hard-coded data. It indicates a value which may be changed as an input to the model.

* Green text indcates a cell reference on a different sheet in the same workbook. It simply pulls data inputted or calculated on another sheet.

* Red text indicates a cell reference in a different workbook. It pulls data from another file, indicating dependency on another workbook.

#### Separate Input from Output

> Clearly distinguish which cells drive the model.

Ideally, inputs and outputs should appear on separate worksheets so there is no confusion as to which cells drive the model and which cells are its result.

