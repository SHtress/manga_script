import requests
import os
import argparse

def download_page(dirname, number, url):
    with open('{}/{}.jpg'.format(dirname, number), 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)
            return

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

        print('download page %d successfully' % number)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    name, _ = os.path.abspath(args.filename).rsplit('.', 1)

    if not os.path.exists(name):
        os.makedirs(name)

    with open(args.filename) as file:
        for number, line in enumerate(file):
            download_page(name, number,line)


if __name__ == '__main__':
    result = main()