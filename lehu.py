# coding=utf-8
import click
from core.api import LehuPicker
from core.utils import load_data, print_head

@click.command()
@click.option('--data', default=None, help='Name of data file.')
@click.option('-f', is_flag=True, help='Override existing files.')
def do_download(data, f):
    data = load_data(data)
    picker = LehuPicker()
    for item in data:
        print_head(item['caption'])
        filelist = picker.get_filelist(item['code'])
        for file in filelist:
            picker.download_file(file[0], item['dir'], file[1], f)

if __name__ == '__main__':
    do_download()
