# -*- coding: utf-8 -*-
'''
@author: moloch

Copyright 2015

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


import bcrypt
from sqlalchemy import Column, desc
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import String, Unicode

from models import dbsession
from models.BaseModels import DatabaseObject
from models.Permission import Permission  # Fix mapper

# Constants
ADMIN_PERMISSION = u'admin'


class User(DatabaseObject):

    ''' User definition '''

    _name = Column(Unicode(16), unique=True, nullable=False)
    _password = Column("password", String(64))

    permissions = relationship("Permission",
                               backref=backref("user", lazy="select"),
                               cascade="all,delete,delete-orphan")

    @classmethod
    def all_users(cls):
        ''' Return all non-admin user objects '''
        return filter(
            lambda user: user.has_permission(
                ADMIN_PERMISSION) is False, cls.all()
        )

    @classmethod
    def by_name(cls, name):
        return dbsession.query(cls).filter_by(
            _name=unicode(name)
        ).first()

    @property
    def permission_names(self):
        ''' Return a list with all permissions accounts granted to the user '''
        return [permission.name for permission in self.permissions]

    def has_permission(self, permission):
        ''' Return True if 'permission' is in permissions_names '''
        return True if permission in self.permission_names else False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = unicode(value[:16])

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.hashpw(value, bcrypt.gensalt())

    def validate_password(self, attempt):
        return self.password == bcrypt.hashpw(attempt, self.password)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<User - name: %r>' % (self.name,)

    def to_dict(self):
        return {
            "id": self.uuid,
            "created": str(self.created),
            "name": self.name,
            "is_admin": ADMIN_PERMISSION in self.permission_names,
            "jobs": [job.uuid for job in self.jobs],
            "organizations": [org.uuid for org in self.organizations],
        }
