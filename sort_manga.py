import os
import argparse
import re
from termcolor import colored
from PIL import Image
 
 
SRC_PATTERN = r'(?P<name>.*) Том (?P<part>\d+) Глава (?P<chapter>\d+)(?P<chapter_float>\.\d+)? \[mangalib\.me\]'
DST_PATTERN = '{}_Part_{}_chapter_{}{}'
PARSED_PATTERN = r'.+_Part_\d+_chapter_\d+(.\d+)?'

SUPPORTED_EXTENSION = ('png', 'jpeg', 'jpg')
PAGE_EXTENSION = '.jpeg'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirname')
    
    args = parser.parse_args()
    dirname = os.path.abspath(args.dirname)
    
    pattern = re.compile(SRC_PATTERN)
    
   
    for filename in os.listdir(dirname):
        src =f"{dirname}/{filename}"
        parsed = pattern.match(filename)
        
        if re.match(PARSED_PATTERN, src):
            print(colored(f'Already parsed {src}', 'red'))
            continue
        
        if parsed is not None:
            part = parsed.group('part')
            chapter = parsed.group('chapter')  
            chapter_float = parsed.group('chapter_float')  
            
            dst = DST_PATTERN.format(parsed.group('name'), part.zfill(2), chapter.zfill(3), chapter_float or '.0')
            dst = re.sub(r'\s+', '_', dst)
            dst = f'{dirname}/{dst}'
            
            try:            
                os.rename(src, dst)
            except FileExistsError:
                print(colored(f'Already parsed {src}', 'red'))
                raise
                
            print(colored(dst, 'green'))
            pages = os.path.abspath(dst)
            process_pages(pages)
            
        else:
            print(colored(f'Can\'t parse {filename}', 'red'))
            

def process_pages(pages):
    for page in os.listdir(pages):
        page_src = f"{pages}/{page}"
        name, ext = page.split('.')
        page_dst = f"{name.zfill(2)}.{ext}"
        page_dst = f"{pages}/{page_dst}"
        try:
            os.rename(page_src, page_dst)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
            
        if ext not in SUPPORTED_EXTENSION:
            Image.open(page_dst).convert('RGB').save(f'{pages}/{name.zfill(2)}{PAGE_EXTENSION}')
            os.remove(page_dst)
            print(colored(f'Convert {name.zfill(2)}.{ext} to {name.zfill(2)}{PAGE_EXTENSION}', 'white'))
     
    
if __name__ == '__main__':
    result = main()