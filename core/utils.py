# coding=utf-8
import os
import sys
import json
from colorama import init, Fore, Style

init(autoreset=True)


def download_file(response, path, file_name, force=False):
    """ Download a file and save to path/filename
    :param response: requests.response with stream = True
    :param path: where to save the file, create if not exists
    :param file_name: name of file
    :param force: set False to ignore existed files
    :return: None
    """
    # Create folder if not exists
    if not os.path.exists(path):
        os.mkdir(path)

    # Get length of file
    file_length = int(response.headers.get("Content-Length"))
    size_info = '[%d KB]' % (file_length >> 10)

    # Check if file is already exists
    # And with same size
    save_path = os.path.join(path, file_name)
    down_flag = 'Download'
    if not force and os.path.exists(save_path):
        file_length_old = os.path.getsize(save_path)
        if file_length == file_length_old:
            info = 'Existed : %s %s' % (file_name, size_info)
            print Style.DIM + Fore.GREEN + info
            return
        down_flag = 'Update  '

    # Download file
    progress, chunk_size, info = 0.0, 1 << 15, 'Unhandled exception.'
    try:
        with open(save_path, 'wb') as f:
            prefix = Fore.GREEN + '%s: %s' % (down_flag, file_name)
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                progress += 100. * len(chunk) / file_length
                info = '\r%s %s [%3.1f%%]' % (prefix, size_info, progress)
                sys.stdout.write(info)
                sys.stdout.flush()
    except KeyboardInterrupt:
        # Press Ctrl + C to cancel job
        prefix = Fore.YELLOW + 'Canceled: %s' % file_name
        info = '\r%s %s [%3.1f%%]' % (prefix, size_info, progress)
        os.remove(save_path)
    except Exception as e:
        # An error occurred
        prefix = Fore.RED + 'Warning : %s' % file_name
        info = '\r%s %s [%3.1f%%]\n\t  %s' % (prefix, size_info, progress, e)
        os.remove(save_path)
    finally:
        # Okay when nothing was caught
        sys.stdout.write(info)
        sys.stdout.flush()
        print


def load_data(file_name=None):
    """ Load data from file
    :param file_name: name of data file
    :return: data to download
    """
    # Prepare file path
    file_name = file_name or 'data.json'

    # Load data
    with open(file_name, 'r') as f:
        data = json.load(f)
    return filter(lambda x: x.get('caption'), data)


def print_head(item):
    """ Print Head Info 
    :param item: item to pull
    :rtype: None
    """
    print Fore.CYAN + '>>> %s' % item['caption'] + Style.DIM + Fore.CYAN + ' %s' % item['dir']
