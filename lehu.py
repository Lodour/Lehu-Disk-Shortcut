# coding=utf-8
import click
from core.api import LehuPicker, LehuUploader
from core.utils import load_data, print_head


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--data', default=None, help='Name of data file.')
@click.option('-f', is_flag=True, help='Override existing files.')
def pull(data, f):
    """ Execute download action.
    :param data: Path of the data file
    :param f: Should override existing files or not 
    """
    data = load_data(data)
    picker = LehuPicker()
    for item in data:
        print_head(item)
        file_list = picker.get_filelist(item['code'])
        for file in file_list:
            picker.download_file(file[0], item['dir'], file[1], f)


@click.group()
def cli2():
    pass


@cli2.command()
@click.option('--code', help='Upload code.')
@click.option('--path', help='Path to upload file.')
@click.option('--name', help='Name of upload file.')
def push(code, path, name):
    """ Execute upload action.
    :param code: where to upload
    :param path: path to upload file
    :param name: name of upload file
    """
    uploader = LehuUploader()
    print uploader.upload_file(code, path, name)


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
