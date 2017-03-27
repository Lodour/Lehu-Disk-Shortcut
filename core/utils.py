# coding=utf-8
import os
import progressbar
import requests.packages.urllib3


def download_file(response, path, filename):
    """ Download a file and save to path/filename
    Args:
        response: requests.response with stream = True
        path: whereto save the file, create if not exists
        file_name: name of file
    """
    # Get length of file
    file_length = int(response.headers.get("Content-Length"))

    # Create folder if not exists
    if not os.path.exists(path):
        os.mkdir(path)
    save_path = os.path.join(path, file_name)

    # Download file
    with open(save_path, 'wb') as f:
        widgets = ['Progress: ',
                   progressbar.Percentage(), ' ',
                   progressbar.Bar(marker='#', left='[', right=']'), ' ',
                   progressbar.ETA(), ' ',
                   progressbar.FileTransferSpeed()]
        pbar = progressbar.ProgressBar(widgets=widgets,
                                       maxval=file_length).start()
        for chunk in response.iter_content(chunk_size=1):
            if chunk:
                f.write(chunk)
                f.flush()
            pbar.update(len(chunk) + 1)
        pbar.finish()
