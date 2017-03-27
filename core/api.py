# coding=utf-8
import requests
from lxml import etree
from urlparse import urljoin

import utils

class LehuBase(requests.Session):
    """ Basic class for disk.lehu.shu.edu.cn """

    def __init__(self, index_url=None):
        super(LehuBase, self).__init__()

        # Set url of index page and parse it to an element tree
        self.index_url = index_url or 'http://disk.lehu.shu.edu.cn/'
        self.index_tree = etree.HTML(self.get(self.index_url).text)
        self.index_hrefs = self.index_tree.xpath(r'//a')

    def post_form(self, tree, url, data):
        """ Post data to url with `input` fields in tree
        Args:
            tree: element tree of current page
            url: where to post
            data: dict, what to post
        Returns:
            requests.post
        """
        input_elements = tree.xpath(r'//input')
        post_kw = lambda x: (x.get('id'), x.get('value'))
        post_data = map(post_kw, input_elements)
        post_data = dict(post_data)
        post_data.update(data)
        return self.post(url, post_data)

    def get_and_post(self, url, data):
        """ Get a page and post data to url from it
        Args:
            url: page to get
            data: page to post
        Returns:
            requests.post
        """
        tree = etree.HTML(self.get(url).text)
        return self.post_form(tree, url, data)


class LehuPicker(LehuBase):
    """ Picker """

    def __init__(self):
        super(LehuPicker, self).__init__()
        self.pick_url = urljoin(self.index_url, 'pick.aspx')

    def get_filelist(self, code):
        """ Get available file list of specificied code
        Args:
            code: pick code
        Returns:
            list of (file_name, download_url)
        """
        req_filelist = self.get_and_post(self.pick_url, {'code': code})
        tree = etree.HTML(req_filelist.text)
        file_info = lambda x: (urljoin(self.index_url, x.get('href')), x.text)
        return map(file_info, tree.cssselect('div.picklist a'))

    def download_file(self, url, path, file_name):
        """ Download a file from url and save to path
        Args:
            url: where to download
            path: whereto save the file, create if not exists
            file_name: name of file
        """
        response = self.get(url, stream=True)
        utils.download_file(response, path, file_name)



