# coding=utf-8
from core.api import LehuPicker
from core.utils import load_data, print_head

def test_picker():
    data = load_data()
    picker = LehuPicker()
    for item in data:
        print_head(item['caption'])
        filelist = picker.get_filelist(item['code'])
        for file in filelist:
            picker.download_file(file[0], item['dir'], file[1])

test_picker()
