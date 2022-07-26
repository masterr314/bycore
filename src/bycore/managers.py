import os
import sys
import re
import pickle
from os.path import exists
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class Manager(object):

    def __init__(self):
        super().__init__()

    def load(self):
        raise NotImplementedError('load() is not implemented!')

    def save(self, data):
        raise NotImplementedError('save() is not implemented!')


class FileManager(Manager):

    def __init__(self, file):
        super(FileManager, self).__init__()

        if not file or not re.search("\\.bypass$", file):
            raise ValueError('File extension should be .bypass')

        self.__file = file

    def load(self):
        """Load data from .bypass file to the app"""
        if exists(self.__file):
            return pickle.load(open(self.__file, "rb"))
        else:
            self.save({})
            return {}

    def save(self, data):
        """Save data to .bypass file locally"""
        pickle.dump(data, open(self.__file, "wb"))


class NetworkManager(Manager):

    def __init__(self, file, url):
        super(NetworkManager, self).__init__()

        if not file or not re.search("\\.bypass$", file):
            raise ValueError('File extension should be .bypass')

        self.__file = file

        if not url:
            raise ValueError('Bypass server URL must be provided')

        self.__url = url

    def load(self):
        """Load .bypass file to Bypass-server"""
        pass

    def save(self, data=None):
        """Save .bypass file to Bypass-server

        :returns: Response object
        :rtype: :class:`Response`
        """
        endpoint = data.get('endpoint', None)
        if exists(self.__file) and endpoint:
            files = {'file': open(self.__file, 'rb')}
            res = requests.post(self.__url + endpoint, files=files, json=data if data else {})
            return res

    def ping(self, data):
        endpoint = data.get('endpoint', None)
        if endpoint:
            return requests.post(self.__url + endpoint)
