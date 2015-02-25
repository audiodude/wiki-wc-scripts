# Scripts for counting the number of words on wikipedia

## You will need

* An [XML dump](http://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia) of the articles of English wikipedia. You want pages-articles.xml.bz2.
* The scripts in this project
* A bunch of disk space
* An Amazon AWS account

## Steps

0. Download your wikipedia XML article dump and extract it.
0. Run the following command to create a stripped version of the dump with just the article text and no punctuation or markup: `echo enwiki-20141106-pages-articles.xml | ./grab_articles.py | ./process_wiki.pl > enwiki_words.txt`
0. Upload `mapper.py`, `reducer.py` and the `enwiki_words.txt` to an AWS Elastic Map Reduce.
0. Run the map reduce

## Output file
The output file will contain entries like "apple\t79077", where "\t" is a tab
character. This means that the token "apple" appears 79,077 times in the
English wikipedia dump you processed.
