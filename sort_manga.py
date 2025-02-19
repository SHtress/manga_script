import os, shutil
import argparse
import re
from termcolor import colored
from PIL import Image
from fpdf import FPDF
 
SRC_PATTERN = r'(?P<name>.*) Том (?P<part>\d+) Глава (?P<chapter>\d+)(?P<chapter_float>\.\d+)?( \[mangalib\.me\])?'
DST_PATTERN = '{}_Part_{}_chapter_{}{}'
PARSED_PATTERN = r'.+_Part_\d+_chapter_\d+(.\d+)?'

SUPPORTED_EXTENSION = ('png', 'jpeg', 'jpg', )
CONVERTABLE_EXTENSION = ('gif', 'png', 'jpeg', 'jpg' )
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

        if re.match(PARSED_PATTERN, src) or parsed is None:
            print(colored(f'Already parsed {src}', 'red'))
            pages = os.path.abspath(src)
        else:
            dst = f'{dirname}/{get_destintaion(parsed)}'

            try:
                os.rename(src, dst)
            except FileExistsError:
                print(colored(f'Already parsed {src}', 'red'))
                raise

            print(colored(dst, 'green'))
            pages = os.path.abspath(dst)
        process_pages(pages)


def get_destintaion(parsed):
    part = parsed.group('part')
    chapter = parsed.group('chapter')
    chapter_float = parsed.group('chapter_float')

    dst = DST_PATTERN.format(parsed.group('name'), part.zfill(4), chapter.zfill(4), chapter_float or '.0')
    dst = re.sub(r'\s+', '_', dst)
    return dst


def process_pages(pages):
    if not os.path.isdir(pages):
        return

    page_list = []
    for page in os.listdir(pages):
        page_src = f"{pages}/{page}"
        name, ext = page.rsplit('.', 1)
        page_dst = f"{pages}/{name.zfill(2)}.{ext}"
        try:
            os.rename(page_src, page_dst)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

        if ext in CONVERTABLE_EXTENSION:
            new_dst = f'{pages}/{name.zfill(2)}{PAGE_EXTENSION}'
            Image.open(page_dst).convert('RGB').save(new_dst)
            os.remove(page_dst)
            print(colored(f'Convert {name.zfill(4)}.{ext} to {name.zfill(4)}{PAGE_EXTENSION}', 'white'))
            page_dst = new_dst
        else:
            print(colored(f'Can\' convert {name.zfill(4)}.{ext}', 'red'))
            continue

        page_list.append(page_dst)

    for page in page_list:
        image_rotation(page)

    convert_to_pdf(pages, page_list)


def image_rotation(image):
    im1 = Image.open(image)
    width, height = im1.size
    if width > height:
        im2 = im1.transpose(Image.ROTATE_270)
        os.remove(image)
        im2.save(image)


def convert_to_pdf(folder, imagelist):
    pdf = FPDF()
    for image in sorted(imagelist):
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)  # 210 and 297 are the dimensions of an A4 size sheet.
    pdf.output(os.path.dirname(folder) + '/' + os.path.basename(folder)  + '.pdf', "F")
    shutil.rmtree(folder)  # remove garbage

    print("PDF generated successfully!")


if __name__ == '__main__':
    result = main()
