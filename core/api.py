# coding=utf-8
import requests
from lxml import etree
from urlparse import urljoin
import os

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

    def post_form(self, tree, url, data, post_kw=None, parse=True, **kwargs):
        """ Post data to url with `input` fields in tree
        :param tree: element tree of current page
        :param url: where to post
        :param data: dict, what to post
        :param post_kw: a function to extract post `key-value`s
        :param parse: parse to an etree object or not
        :param kwargs: other key args passed to `requests.post`
        :return: a parsed etree object
        """
        input_elements = tree.xpath(r'//input')
        if post_kw is None:
            post_kw = lambda x: (x.get('id'), x.get('value'))
        post_data = dict(map(post_kw, input_elements))
        post_data.update(data)
        req_post = self.post(url, data=post_data, **kwargs)
        if parse is True:
            return etree.HTML(req_post.text)
        return req_post

    def get_and_post(self, url, data, post_kw=None, parse=True, **kwargs):
        """ Get a page and post data to url from it
        :param url: page to get
        :param data: page to post
        :param post_kw: a function to extract post `key-value`s
        :param parse: parse to an etree object or not
        :param kwargs: other key args passed to `requests.post`
        :return: a parsed etree object
        """
        tree = etree.HTML(self.get(url).text)
        return self.post_form(tree, url, data, post_kw, parse, **kwargs)


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
        tree = self.get_and_post(self.pick_url, {'code': code})
        file_info = lambda x: (urljoin(self.index_url, x.get('href')), x.text)
        return map(file_info, tree.cssselect('div.picklist a'))

    def download_file(self, url, path, file_name, force=False):
        """ Download a file from url and save to path
        :param url: where to download
        :param path: where to save the file, create if not exists
        :param file_name: name of file
        :param force: set False to ignore existed files, default False
        """
        response = self.get(url, stream=True)
        utils.download_file(response, path, file_name, force)


class LehuUploader(LehuBase):
    """ Uploader """

    def __init__(self):
        super(LehuUploader, self).__init__()
        self.upload_url = urljoin(self.index_url, 'uploadfile.aspx')

    def upload_file(self, code, file_path, file_name):
        """ Upload a file to specified upload code
        :return: result of uploading, True / error message
        :param code: where to upload
        :param file_path: path of to-upload file
        :param file_name: name of to-upload file
        """
        # Get etree of upload page
        tree = self.get_and_post(self.upload_url, {'code': code})

        # Find the actual url to upload
        upload_action = tree.xpath(r'//form[@id="form1"]/@action')
        if not upload_action:
            raise Exception(u'Wrong upload code or unknown error.')
        upload_url = urljoin(self.index_url, upload_action[0])

        # Prepare post file
        full_path = os.path.join(file_path, file_name)
        file_field_name = tree.xpath(r'//input[@type="file"]/@name')[0]
        file_field_data = (file_name, open(full_path, 'rb'), 'text/plain')
        files = {file_field_name: file_field_data}

        # Prepare extra data
        post_kw = lambda x: (x.get('name'), x.get('value', ''))
        data = {
            'autorename': 'on',
            # why `maxsize` should not be removed here ???
            # it should have been added in `self.post_form()` with same value
            'maxsize': tree.xpath(r'//input[@id="maxsize"]/@value')[0],
        }

        # Upload and check
        tree = self.post_form(tree, upload_url, data, post_kw, files=files)
        result = tree.xpath(r'//td[@width="74%"]')[0].text.strip()
        return result == u'上传成功！' or result
