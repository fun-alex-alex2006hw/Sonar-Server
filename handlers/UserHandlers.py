# -*- coding: utf-8 -*-
'''
@author: moloch

 Copyright 2013

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


from handlers.BaseHandlers import APIBaseHandler
from libs.JsonAPI import json_api_method
from libs.SecurityHelpers import authenticated
from libs.ValidationError import ValidationError
from models import dbsession


class SettingsAPIHandler(APIBaseHandler):

    ''' Change settings related to the current user '''

    @authenticated
    def get(self):
        user = self.get_current_user()
        self.write(user.to_dict())

    @authenticated
    @json_api_method
    def put(self):
        '''
        Edit the current user's settings, if there is a UUID given as a
        Backbone parameter we ignore it and use whatever is in the session.
        '''
        if self.get_argument("password", None) is not None:
            self.change_password()

    def change_password(self):
        ''' Change a password '''
        user = self.get_current_user()
        old_password = self.get_argument('old_password', '')
        new_password = self.get_password()
        if user.validate_password(old_password):
            user.password = new_password
            dbsession.add(user)
            dbsession.commit()
            self.clear_all_cookies()
            self.redirect('/login')
        else:
            raise ValidationError("Old password is invalid")

    def get_password(self):
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        if password1 != password2:
            raise ValidationError("New passwords do not match")
        elif len(password1) < 12 and not self.config.debug:
            raise ValidationError("New password is too short")
        else:
            return password1
