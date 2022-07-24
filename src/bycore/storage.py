from datetime import datetime
from .managers import (
    FileManager,
    NetworkManager,
)


class AbstractStorage(object):

    def __init__(self):
        super().__init__()

    def initialize(self):
        raise NotImplementedError("initialize() is not implemented!")

    def get_all(self):
        raise NotImplementedError("get_all() is not implemented!")


class Storage(AbstractStorage):

    def __init__(self, filename, url):
        """
        :param filename: Default storage file name
        :type filename: str
        :param url: Bypass server URL
        :type url: str
        """

        super(Storage, self).__init__()

        if not filename:
            raise ValueError('Default storage file name must by provided')

        if not url:
            raise ValueError('Bypass server URL must by provided')

        self.__default_storage_file_name = filename
        self.__bypass_server_url = url
        self.__data = None
        self.__file_manager = None
        self.__network_manager = None
        self.__acc_created_at = None
        self.__last_log_in_at = None
        self.__pass_phrase = None
        self.__nickname = None

    @property
    def data(self):
        return self.__data

    @property
    def nickname(self):
        return self.__nickname

    @nickname.setter
    def nickname(self, value):
        if not self.__nickname:
            self.__nickname = value
            self.save()

    @property
    def pass_phrase(self):
        return self.__pass_phrase

    @pass_phrase.setter
    def pass_phrase(self, value):
        if not self.__pass_phrase:
            self.__pass_phrase = value
            self.save()

    def initialize(self):
        self.__network_manager = NetworkManager(
            file=self.__default_storage_file_name,
            url=self.__bypass_server_url
        )
        self.__file_manager = FileManager(
            file=self.__default_storage_file_name
        )
        _all = self.__file_manager.load()
        # self.__last_log_in_at = _all.get('LAST_LOG_IN_AT', datetime.now())
        self.__acc_created_at = _all.get('ACC_CREATED_At', datetime.now())
        self.__data = _all.get('DATA', [])
        self.__nickname = _all.get('NICKNAME', '')
        self.__pass_phrase = _all.get('PASS_PHRASE', '')

        self.__last_log_in_at = datetime.now()
        self.save()

    def get_all(self):
        return self.__data['DATA']

    def add_new(self, new_entry):
        self.__data.append(new_entry)
        self.save()

    def delete_one(self, entry):
        self.__data.remove(entry)
        self.save()

    def save(self):
        combined = {
            'NICKNAME': self.__nickname,
            'PASS_PHRASE': self.__pass_phrase,
            'ACC_CREATED_At': self.__acc_created_at,
            'LAST_LOG_IN_AT': self.__last_log_in_at,
            'DATA': self.__data
        }

        self.__file_manager.save(combined)

    def sync(self):
        response = self.__network_manager.save()
        if response and response.status_code == 200:
            for i in self.__data:
                if not i.is_synced:
                    i.is_synced = True

            self.save()

        return response
