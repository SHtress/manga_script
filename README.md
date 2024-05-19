# manga_script
Script for preparing parts and chapters from mangalib.me.

## Why it exists:
I start using PocketBook 617 for reading books and manga.
To get manga i use [mangalib.me](mangalib.me) and ["Mangalib: Download all chapters"](https://greasyfork.org/en/scripts/399534-mangalib-download-all-chapters/code) script. 
But downloaded chapters sorted wrong which is uncomfortable for reading.

To solve this problem i created this small script.
Also this script will fix all other problem that i will encounter(like .gif pages that not supported by my e-book)

## Sort and renames chapters:
* Add leading zeros for chapter names
* Convert images to jpeg if they not jpeg or png
* Change spaces to underscores
* Change names from rus to eng

## Deps:
* Pillow
* termcolor
