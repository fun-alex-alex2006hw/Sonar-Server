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

from sqlalchemy import Column
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import Unicode

from models.BaseModels import DatabaseObject


class Fingerprint(DatabaseObject):

    ''' This class contains the resources that make up a fingerprint '''

    name = Column(Unicode(128), nullable=False)
    resources = relationship("Resource",
                             backref=backref("fingerprint", lazy="joined"),
                             cascade="all,delete,delete-orphan")

    def to_dict(self):
        return {
            u'name': self.name,
            u'fingerprints': [unicode(resource) for resource in self.resources]
        }

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name.encode('ascii', 'ignore')

    def __len__(self):
        return len(self.resources)
