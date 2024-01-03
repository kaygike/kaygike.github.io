## Commands


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
* [MagnetDL](https://www.magnetdl.com)
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


### Vocabulary

Words worth remembering. IPAs via dictionary.com.

**bureaucratic tapeworm**, n., _byoor-uh-krat-ik teyp-wurm_

> Unelected career official; statist parasite.

**dendroid**, adj., _den-droid_

> Resembling a tree in form and branching structure.

**noxious**, adj., _nok-shuhs_

> Morally harmful or pernicious; corrupting.

**panacea**, n., _pan-uh-see-uh_

> Hypothetical remedy for all ills or diseases.

**proprietorial**, adj., _pruh-prahy-tawr-ee-uhl_

> Of or pertaining to ownership.

**pyrrhic**, adj., _pir-ik_

> Of or relating to Pyrrhus, especially relating to victories won by incurring terrible losses.

**shibboleth**, n., _shib-uh-lith_

> A favorite word or saying of a sect or political group.

> A manner of speaking that is distinctive of a particular group.

**sisyphean**, adj., _sis-uh-fee-uhn_

> Of or relating to Sisyphus.

> Endless and unavailing, as labor or a task.


### Statistics

```
Figure: Jews, the US, and the World
,--------------------------------------------------------.
|    6,900,000 Jews in Israel |  45.4% |        |   0.09% |
|    6,000,000 Jews in US     |  39.5% |  1.8%  |   0.08% |
|    2,300,000 Jews elsewhere |  15.1% |        |   0.03% |
|-----------------------------|---------        |---------|
|   15,200,000 Jews worldwide | 100.0% |        |   0.19% |
|------------------------------------------------         |
|  332,100,000 people in US            | 100.0% |         |
|-----------------------------------------------|---------|
|7,840,000,000 people worldwide                 | 100.00% |
'---------------------------------------------------------'
```
* [Census: US & world population](https://www.census.gov/popclock/)
* [World Bank: Israel & world population](https://data.worldbank.org/indicator/SP.POP.TOTL?end=2021&start=2021&view=chart&year=2021)
* [JNS: Jewish population](https://www.jns.org/jewish-world-population-rises-to-15-2-million-45-3-live-in-israel/)


```
                                              .---------------,
Figure: Demographics of US Jews               | Jews | All US |
,-------------------------------------------------------------|
| Being Jewish is very important              |  42% |        |
| Married to another Jew                      |  55% |        |
| Spouse is same race/ethnicity               |  89% |  89.9% |
| Spouse is same sex                          |   3% |   0.4% |
| All or most of close friends are Jew        |  29% |        |
| Feel "a great deal" of belonging to Jews    |  48% |        |
| Have "a lot" in common with Muslims         |   4% |        |
| Have "a lot" in common with Protestants     |   3% |        |
| Have "a lot" in common with Evangelicals    |   2% |        |
| Have lived in Israel or been more than once |  26% |        |
| Are very or somewhat attached to Israel     |  58% |        |
| Believe God gave Israel to the Jews         |  32% |        |
| Identify with or lean Democrat              |  71% |        |
| Identify as White, non-Hispanic             |  96% |        |
| Have a postgraduate degree                  |  28% |  11.0% |
| Are gay                                     |  4%  |   2.1% |
| Are bisexual                                |  5%  |   3.1% |
| Live in housholds earning $200,000 or more  |  23% |   4.0% |
'-------------------------------------------------------------'
```
* [Pew: Jewish identity and belief](https://www.pewresearch.org/religion/2021/05/11/jewish-identity-and-belief/)
* [Gallup: Jewish LGBT identification](https://news.gallup.com/poll/329708/lgbt-identification-rises-latest-estimate.aspx)
* [NBC: US LGBT identification](https://www.nbcnews.com/feature/nbc-out/nearly-1-million-u-s-households-composed-same-sex-couples-n1240340)
* [Census: Race and marriage in US](https://www.census.gov/library/stories/2018/07/interracial-marriages.html)


## External

### American Ideology

"American Ideology" by Hoppe is an excerpt from a 2019 speech by Hans-Hermann Hoppe entitled, "On the American Ideology and its Proponents and Beneficiaries," as translated from German by Ohad Osterreicher.

The full essay can be read at [LewRockwell.com](https://www.lewrockwell.com/2019/04/hans-hermann-hoppe/on-the-american-ideology-and-its-proponents-and-beneficiaries/).

***

According to the official, USA approved belief system, we are all equally intelligent and reasonable people, who are confronted with the same “harsh reality” and are bound to the same facts and truths. Of course, it is true, that even in the age of the American empire, in the USA, people do not live in the best of all worlds. There are many more problems to be solved. Though with the American system of a democratic state, humanity has found the perfect institutional framework which makes the next step in the direction of a perfect world possible; and if only would the American system of democracy takeover worldwide, would the way to perfection be clear, smooth and free.

The single legitimate form of government is democracy. All other forms of government are worse, and any government is better than none. Democratic states like the USA are of the people, by the people and for the people. In democracies no one rules over the other; instead, the people rule over themselves and are thus free. Taxes in democratic states are therefore contributions and payments for governmentally provided services; accordingly, tax avoiders are thieves, who take without paying. To provide shelter for fleeing thieves is thus an act of aggression against the people, from whom they are trying to escape.

Though there are still other forms of governments around the world. There are monarchies, dictatorships, theocracies, and there are feudal landowners, tribes, and warlords. And for this reason, democratic states often must necessarily deal with non-democratic states. Eventually, all states must be converted to the American ideal, because only democracy allows for a peaceful and continual change for the better.

Democratic states like the USA and its European allies are inherently peaceful and do not wage war against each other. If they must fight any wars all at, then these are preventive wars of defense and liberation against aggressive and undemocratic states, that is, just wars. All countries and territories that are presently in war with or occupied by American troops or its European allies – Afghanistan, Pakistan, Iraq, Libyan, Syrian, Sudan, Somalia and Yemen – were therefore guilty of aggression and their war waging and occupation on behalf of the democratic West were an act of self-defense and liberation. However, there is still much to be done. Especially Russia and China still pose a huge threat and must be liberated, in order to make the world finally safe.

Private property, markets, and profits are useful institutions, but a democratic state must ensure that with the appropriate legislation, private property and profits are acquired and used in a socially responsible manner and that markets function efficiently. Moreover, markets and profit-seeking entrepreneurs cannot produce public goods and are thus incapable of satisfying any social needs. And they cannot take care of the truly needy. Only the state can take care of social needs and the less fortunate. The state alone can, through the finance of public goods and aid to the poor, increase the public welfare, and diminish poverty and the number of the needy, if completely not eliminate.

Especially the state has to put the private vice of greed of the pursuit of profit under control. Greed and the pursuit of profit were the leading causes of the most recent large financial crisis. Reckless financiers generated an irrational exuberance among the public, which ultimately had to crash into reality. The market was wrecked, and only the state stood ready to save the day. Only the state, through appropriate regulation and supervision of the banking industry and financial markets, can prevent such a thing from happening again. Banks and companies went bankrupt, yet the state and its central banks held ground and protected the money and jobs of the workers.

Advised by the leading and best-paid economists in the world, states and especially the USA have discovered the causes of economic crises and realized that in order to get out of an economic mess, the people must simultaneously consume more as well as invest more. Every cent under the mattress is a cent withheld from consumption and investment, which in turn impairs future consumption and investment expenditure. In a recession, spending must first of all and under all circumstances be increased; and when the people do not spend enough of their own money, the state has to do it instead. Prudently, states have this option, for their central banks can produce any necessary liquidity. If billions of Dollars or Euros are not enough, then trillions will do; and if trillions do not meet the goal, then surely quadrillions will. Only massive state expenditure can prevent an otherwise unavoidable economic meltdown. In particular, unemployment is the result of low consumption: people who do not have enough money to buy consumer goods; this problem must be remedied by providing them with higher wages or higher unemployment benefits.

When the last financial crisis is finally overcome, the democratic state can and must devote itself once more to the really urgent remaining problems of humanity: the battle against inequality, the elimination of all unjust discrimination, and the control of the global environment and the global climate in particular.

In principle, all people are equal. Differences are only apparent, shallow and meaningless: some people are white, some brown, some black, some are big, others are small; some are fat and others thin; some are male, and some are female; some speak English and others Polish or Chinese as mother tongue. These are accidental human traits. It is a coincidence that some people possess these and some do not. But accidental traits like these have no influence whatsoever on and do not correlate with mental properties like motivation, time preference or intellectual abilities, and they do not contribute to the explanation of economic and social success, especially of income and wealth. Mental and psychic properties have no physical, biological or ethical basis and are limitlessly malleable. In this regard is everyone, except for a few pathological individual cases, equal to the other, and every nation has made in the course of history a contribution to civilization of equal value or would have done so, if only it would have gotten the same chance. Seemingly obvious differences are solely the result of different external circumstances and education. All differences in income and achievements between Whites, Asians, and Blacks, women and men, Latins, Anglos-Saxons and Thais as well as Christians, Hindus, Protestants, and Moslems would disappear, if only equality of opportunity would be established. If instead it will be discovered, that all these different accidental groups are unequally represented in and distributed across different levels of income, wealth, or professional status, some are richer and more successful than others, then this demonstrates unjust discrimination; and such discrimination must be counterbalanced through appropriate, targeted affirmative action on behalf of the state, in which the discriminators have to compensate the unjustly discriminated.

And the studies of the leading and best paid social scientists have clearly shown, who, above all, are the discriminators. The people in question are first and foremost white heterosexual males and the institution of the traditional, patriarchal organized family. It is, therefore, most notably this group of people and this institution which must compensate all other groups and apologize to all other forms of social organization.

But this would not do. The reparations to all disadvantaged, to all victims of inequality and discrimination, require likewise strong governmental support of multiculturalism. The highly developed and white male dominated countries of the Western world have obtained their wealth at the expense of the inhabitants of all other regions of the world and are caught in a disastrous and prejudiced particularism and nationalism. This situation lends itself to be overcome through the promotion and systematic incentivization of immigration of people from different, foreign countries and cultural environments, in order to ensure that the foreign immigrants could finally unleash their full human potential and simultaneously replace the Western parochialism with an authentic cultural diversity.

And with the victory over the disastrous particularism and nationalism through a systematic policy of multiculturalism is one finally able to turn to the crucial stride toward a solution to the undoubtedly biggest global, borderless and world-encompassing problem of climate change. Divergent particularistic and nationalistic interests have thus far lead to the fact that the production and the consumption of non-renewable energy sources were left mostly unregulated and worldwide uncoordinated. And that is why, as the leading and best-paid climate researchers have undoubtedly proven, is the whole globe threatened by unimaginable catastrophes: floods, strong and sudden rising sea levels and the emergence of fatal ecological disequilibria and instabilities. Only through a worldwide, concentrated action by all states, and ultimately the establishment of a supranational world government under the leadership of the USA and an enforced systematic regulation of any production and consumption activities, can this life-threatening danger be avoided. "The common good comes before the individual good" – this is above all, what the problem of climate change shows, and it is on the states and especially on the USA to permanently implement this principle.

