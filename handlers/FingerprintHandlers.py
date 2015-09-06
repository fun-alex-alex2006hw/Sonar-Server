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

import json

from handlers.BaseHandlers import APIBaseHandler
from libs.JsonAPI import json_api_method
from models.Fingerprint import Fingerprint
from models.Resource import Resource


class FingerprintHandler(APIBaseHandler):

    @json_api_method
    def get(self):
        resp = [fingerprint.to_dict() for fingerprint in Fingerprint.all()]
        self.write(json.dumps(resp))

    @json_api_method
    def put(self):
        fingerprint = Fingerprint(name=self.get_argument('name', ''))
        for data in self.api_request['resources']:
            resource = Resource(data=data)
            fingerprint.resources.append(resource)
            self.dbsession.add(resource)
        self.dbsession.add(fingerprint)
        self.dbsession.commit()
