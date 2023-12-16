## cmds

### 7z
create archive w/ no compression and encrypted filenames
```
$ 7z a -p -bt -mx=0 -mhe=on archive.7z file1 file2 file3</code>
````

### bdfr
bulk archive a subreddit

> note: two separate operations shown below
```
$ bdfr clone ~/save_dir/ --subreddit unixporn --log ~/save_dir/log.log --sort top --time all --make-hard-links --file-scheme "{DATE}_{POSTID}_{UPVOTES}"

$ bdfr clone ~/save_dir/ --subreddit unixporn --log ~/save_dir/log.log --make-hard-links --folder-scheme "{DATE}_{TITLE}_{POSTID}_{UPVOTES}" --file-scheme "{UPVOTES}_{DATE}_{REDDITOR}_{POSTID}
```

### ffmpeg
convert ape to flac
```
$ fmpeg -i INPUT.ape OUTPUT.flac
```

convert all m4a to flac and preserve filenames
```
$ for f in *.m4a; do ffmpeg -i "$f" "${f%.m4a}".flac; done
```

merge multiple files into one without re-encoding

> note: specific format for CONCAT.txt file

```
$ cat CONCAT.txt
file '/path/to/file1'
file '/path/to/file2'

$ ffmpeg -f concat -safe 0 -i CONCAT.txt -c copy output.mp4
```

### git
managing multiple usernames

> 1. setup ```~/.ssh/config```  using e.g. ```Host github.com-user1``` and ```Host github.com-user2``` ([source](https://www.howtogeek.com/devops/how-to-fix-git-using-the-wrong-ssh-key-account/))

> 2. setup remote origins to use the above dummy hosts, e.g. ```git remote set-url origin git@github.com-user1:user1/reponame.git``` ([source](https://stackoverflow.com/questions/2432764/how-do-i-change-the-uri-url-for-a-remote-git-repository))


### md5sum
list duplicate files in directory ([source](https://unix.stackexchange.com/questions/277697/whats-the-quickest-way-to-find-duplicated-files/277707#277707))
```
$ find . ! -empty -type f -exec md5sum {} + | sort | uniq -w32 -dD
```

create file with md5 checksums for all flac in directories (one-deep)
```
$ for dir in *; do if [ -d $dir -a ! -h $dir ]; then cd -- "$dir"; echo "Generating md5sum for '$dir'"; md5sum *.flac > checksum.md5; cd .. ; fi; done;
```

### pacman
find install location of package
```
$ pacman -Fql <PACKAGENAME> | grep -E "^usr/bin.+"
```

### podcast-dl
download audio w/ metadata from rss feed
```
$ npx podcast-dl --url <rss url> --episode-template "{{release_date}} {{title}}" --archive archive.archive --include-meta --include-episode-meta --out-dir "."
```

### rsync
mirror directory to another location and log to file

> NOTE: requires backslashes at end of directories

> note: remove --dry-run to execute; '--delete' used to mirror directory contents

```
$ rsync --dry-run --archive --human-readable --itemize-changes --verbose --exclude="lost+found" --delete FILES_TO_COPY/ WHERE_TO_COPY_TO/ | tee ~/DATE_rsync.log
```


### shnsplit
split and tag flac file via cuesheet

> note: requires cuesheet.sh, trash-cli to delete pregap file, and no more than 1 flac file and 1 cue file in directory

```
$ shnsplit -f *.cue -t %n_%t -o flac *.flac; if [ -f "00_pregap.flac" ]; then trash 00_pregap.flac; fi; cuetag.sh *.cue [0-9]*.flac
```

the above, but recursively through subdirectories
```
$ for d in */ ; do cd "$d"; pwd; shnsplit -f *.cue -t %n_%t -o flac *.flac; if [ -f "00_pregap.flac" ]; then trash 00_pregap.flac; fi; cuetag.sh *.cue [0-9]*.flac; cd ..; done
```

### wget
download numerical increments
```
$ wget https://domain.tld/path/to/files/file{1..100}.filetype
```

download numerical & alphabetical increments
```
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

download specific filetype/extensions
```
$ wget --directory-prefix=path/to/save --no-directories --recursive --level=1 --span-hosts --domains=https://domain.tld --accept ext1,ext2,ext3 https://domain.tld/path/to/files
```

### yt-dlp
download video with metadata file
```
$ yt-dlp --add-metadata --write-info-json --restrict-filenames --output "%(title)s_%(upload_date)s_%(id)s.%(ext)s" http://video.url/id
```

## bookmarks

### 'awesome' lists
* [cli](https://github.com/agarrharr/awesome-cli-apps)
* [datahoarding](https://github.com/simon987/awesome-datahoarding)
* [python libs](https://github.com/vinta/awesome-python)
* [self-hosted](https://github.com/awesome-selfhosted/awesome-selfhosted)
* [tui](https://github.com/rothgar/awesome-tuis)

