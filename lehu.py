# coding=utf-8
import click
from core.api import LehuPicker
from core.utils import load_data, print_head

def do_download(file_name, force):
    data = load_data(file_name)
    picker = LehuPicker()
    for item in data:
        print_head(item['caption'])
        filelist = picker.get_filelist(item['code'])
        for file in filelist:
            picker.download_file(file[0], item['dir'], file[1], force)

@click.command()
@click.option('--data', default=None, help='Name of data file.')
@click.option('-f', is_flag=True, help='Override existing files.')
def main(data, f):
    do_download(data, f)


if __name__ == '__main__':
    main()
