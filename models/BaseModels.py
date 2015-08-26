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


import re
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.types import BigInteger, DateTime, Integer, String

from models import dbsession


class _DatabaseObject(object):

    ''' All game objects inherit from this object '''

    @declared_attr
    def __tablename__(self):
        ''' Converts name from camel case to snake case '''
        name = self.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])',
                   lambda letter: "_" + letter.group(0).lower(), name[1:]
                   )
        )

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid4()))
    created = Column(DateTime, default=datetime.now)

    @classmethod
    def all(cls):
        ''' Returns a list of all objects in the database '''
        return dbsession.query(cls).all()

    @classmethod
    def by_id(cls, _id):
        ''' Returns a the object with id of _id '''
        return dbsession.query(cls).filter_by(id=_id).first()

    @classmethod
    def by_uuid(cls, _uuid):
        return dbsession.query(cls).filter_by(uuid=_uuid).first()


class _BigDatabaseObject(object):

    ''' All game objects inherit from this object '''

    @declared_attr
    def __tablename__(self):
        ''' Converts name from camel case to snake case '''
        name = self.__name__
        return (
            name[0].lower() +
            re.sub(r'([A-Z])',
                   lambda letter: "_" + letter.group(0).lower(), name[1:]
                   )
        )
    id = Column(BigInteger, primary_key=True)


# Create an instance called "BaseObject"
DatabaseObject = declarative_base(cls=_DatabaseObject)
BigDatabaseObject = declarative_base(cls=_BigDatabaseObject)
