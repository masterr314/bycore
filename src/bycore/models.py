import uuid
from datetime import datetime


class Entry(object):

    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid4())


class Password(Entry):

    def __init__(
            self,
            service_name,
            login,
            encrypted_password,
            short_name,
            path='/other/other',
            description=None,
            created_at=datetime.now(),
            last_updated_at=datetime.now(),
            is_synced=False
    ):
        super(Password, self).__init__()

        self.service_name = service_name
        self.login = login
        self.short_name = short_name
        self.password = encrypted_password
        self.path = path

        if description:
            self.description = description
        else:
            self.description = f"Password for {login}, service is {service_name}"

        self.created_at = created_at
        self.last_updated_at = last_updated_at
        self.is_synced = is_synced

    def get_dict_of_fields(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'login': self.login,
            'password': self.password,
            'short_name': self.short_name,
            'path': self.path,
            'description': self.description,
            'create_at': str(self.created_at),
            'last_updated_at': str(self.last_updated_at),
            'is_synced': self.is_synced,
        }

    def __str__(self):
        return self.description

    def __repr__(self):
        return f"<Password {self.id}>"
