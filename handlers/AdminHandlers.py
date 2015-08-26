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
from libs.APIConstants import BAD_REQUEST
from libs.SecurityHelpers import authenticated, authorized, restrict_ip_address
from libs.ValidationError import ValidationError
from models import dbsession
from models.Permission import Permission
from models.User import ADMIN_PERMISSION, User


class UserAPIHandler(APIBaseHandler):

    @authenticated
    @authorized(ADMIN_PERMISSION)
    @restrict_ip_address
    def get(self, uuid=None):
        ''' Get a specific user or all users '''
        if uuid is None:
            response = json.dumps([user.to_dict() for user in User.all()])
        else:
            user = User.by_uuid(uuid)
            if user is not None:
                response = user.to_dict()
            else:
                self.set_status(BAD_REQUEST)
                response = {"error": "User not found"}
        self.write(response)

    @authenticated
    @authorized(ADMIN_PERMISSION)
    @restrict_ip_address
    def post(self, uuid=None):
        ''' Create a new user '''
        try:
            username = self.get_username()
            password = self.get_password()
            new_user = self.create_user(username, password)
            if self.get_argument('is_admin', False):
                self._make_admin(new_user)
            self.write(new_user.to_dict())
        except ValidationError as error:
            self.set_status(BAD_REQUEST)
            self.write({'error': str(error)})

    @authenticated
    @authorized(ADMIN_PERMISSION)
    @restrict_ip_address
    def put(self, uuid=None):
        ''' Edit existing users '''
        try:
            if uuid is None:
                raise ValidationError("Missing uuid parameter")
            user = User.by_uuid(uuid)
            if user is None:
                raise ValidationError("User not found")
            if self.get_argument("is_admin", False) is True:
                self._make_admin(user)
            if self.get_argument("password", None) is not None:
                self._change_user_password(user)
            if self.get_argument("name", None) is not None:
                self._change_user_name(user)
        except ValidationError as error:
            self.set_status(BAD_REQUEST)
            self.write({"error": str(error)})

    def create_user(self, username, password):
        new_user = User(name=username, password=password)
        dbsession.add(new_user)
        dbsession.commit()
        return new_user

    def _make_admin(self, user):
        admin_permission = Permission(name=ADMIN_PERMISSION, user_id=user.id)
        user.permissions.append(admin_permission)
        dbsession.add(admin_permission)
        dbsession.add(user)
        dbsession.commit()

    def _change_user_name(self, user):
        user.name = self.get_username()
        dbsession.add(user)
        dbsession.commit()

    def _change_user_password(self, user):
        user.password = self.get_password()
        dbsession.add(user)
        dbsession.commit()

    def get_username(self):
        _username = self.get_argument('name', '')
        if User.by_name(_username) is not None:
            raise ValidationError("Username already exists")
        elif len(_username) < 3:
            raise ValidationError("Username is too short, must be 3+ chars")
        return _username

    def get_password(self):
        password = self.get_argument('password', '')
        if len(password) < 12:
            raise ValidationError("Password is too short, must be 12+ chars")
        else:
            return password
