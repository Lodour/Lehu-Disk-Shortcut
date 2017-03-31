# coding=utf-8
import requests
from lxml import etree
from urlparse import urljoin

import utils


class LehuBase(requests.Session):
    """ Basic class for `disk.lehu.shu.edu.cn` """

    def __init__(self, index_url=None):
        """ Construct method
        :param index_url: url of index page of Lehu Net-Disk 
        """
        super(LehuBase, self).__init__()

        # Set url of index page and parse it to an element tree
        self.index_url = index_url or 'http://disk.lehu.shu.edu.cn/'
        self.index_tree = etree.HTML(self.get(self.index_url).text)
        self.index_hrefs = self.index_tree.xpath(r'//a')

    def post_form(self, tree, url, data):
        """ Post data to url with `input` fields in tree
        :param tree: element tree of current page
        :param url: where to post
        :param data: dict, what to post
        :return: a requests.post object
        """
        input_elements = tree.xpath(r'//input')
        post_kw = lambda x: (x.get('id'), x.get('value'))
        post_data = dict(map(post_kw, input_elements))
        post_data.update(data)
        return self.post(url, post_data)

    def get_and_post(self, url, data):
        """ Get a page and post data to url from it
        :param url: page to get
        :param data: page to post
        :return: a requests.post object
        """
        tree = etree.HTML(self.get(url).text)
        return self.post_form(tree, url, data)


class LehuPicker(LehuBase):
    """ Picker """

    def __init__(self):
        super(LehuPicker, self).__init__()
        self.pick_url = urljoin(self.index_url, 'pick.aspx')

    def get_filelist(self, code):
        """ Get available file list of specified code
        :param code: pick code
        :return: list of (file_name, download_url)
        """
        req_fileList = self.get_and_post(self.pick_url, {'code': code})
        tree = etree.HTML(req_fileList.text)
        file_info = lambda x: (urljoin(self.index_url, x.get('href')), x.text)
        return map(file_info, tree.cssselect('div.picklist a'))

    def download_file(self, url, path, file_name, force=False):
        """ Download a file from url and save to path
        :param url: where to download
        :param path: whereto save the file, create if not exists
        :param file_name: name of file
        :param force: set False to ignore existed files, default False
        """
        response = self.get(url, stream=True)
        utils.download_file(response, path, file_name, force)
