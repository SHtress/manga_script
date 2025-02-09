# manga_script
Script for preparing parts and chapters from mangalib.me.

## Why it exists:
I start using PocketBook 617 for reading books and manga.
~~To get manga i use [mangalib.me](mangalib.me) and ["Mangalib: Download all chapters"](https://greasyfork.org/en/scripts/399534-mangalib-download-all-chapters/code) script.
But downloaded chapters sorted wrong which is uncomfortable for reading.~~
For getting manga i use this script combined with browser-extension.

Also this script will fix all other problem that i will encounter(like .gif pages that not supported by my e-book)

## Features:
* Add leading zeros for chapter names
* Convert images to jpeg if they not jpeg or png
* Change spaces to underscores
* Rotate and resize pages for suitable orientation and resolution
* Download pages by group of urls made by browser-extension

## Deps:
* Pillow
* termcolor
* fpdf
