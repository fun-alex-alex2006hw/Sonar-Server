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
import logging

import bcrypt
from tornado.options import options

from handlers.BaseHandlers import APIBaseHandler, BaseHandler
from libs.APIConstants import BAD_REQUEST
from libs.SecurityHelpers import authenticated
from models.User import ADMIN_PERMISSION, User


class AppHandler(BaseHandler):

    def get(self):
        '''  Serves the single page app '''
        self.set_xsrf_token()
        self.render("app.html")


class LoginAPIHandler(APIBaseHandler):

    def get(self):
        '''
        This can be used by the client to test if their session is valid
        '''
        user = self.get_current_user()
        if user is not None:
            self.write({"valid": True})
        else:
            self.write({"valid": False})

    @authenticated
    def put(self):
        ''' This method extends an existing session '''
        user = self.get_current_user()
        session = self.get_session()
        encrypted_session = self.create_signed_value(name="session",
                                                     value=json.dumps(session))
        self.write({
            "username": user.name,
            "password": None,
            "data": encrypted_session,
            "expires": int(session['expires']),
            "is_admin": user.has_permission(ADMIN_PERMISSION),
            "debug": options.debug,
        })

    def post(self):
        ''' Login and create a new session '''
        user = User.by_name(self.get_argument('username', ''))
        password = str(self.get_argument('password', ''))
        if user is not None:
            # Each of these methods writes it own response
            if user.validate_password(password):
                self.login_success(user)
            else:
                self.login_failure()
        else:
            # To prevent a timing attack to enumerate users, since hashing
            # takes non-zero time, we only we normally only hash if we got a
            # user from the db, we just hash whatever we got anyways before
            # telling the client the auth failed.
            bcrypt.hashpw(password, bcrypt.gensalt())
            self.login_failure()

    def login_failure(self):
        ''' Failed authentication attempt '''
        logging.info("Failed authentication attempt from %s",
                     self.request.remote_ip)
        self.set_status(BAD_REQUEST)
        self.write({"error": "Incorrect username and/or password."})

    def login_success(self, user):
        '''
        Create a session and return it to the client, sessions are *not*
        cookies, instead we use a an encrypted/hmac'd JSON blob that we hand to
        the client. The client includes this encrypted/hmac'd blob in a header
        `X-SONAR` on all requests (including GETs). The only cookie we
        assign is the `_xsrf` cookie, which is a redundent anti-CSRF token.
        '''
        logging.info("Successful authentication request for %s", user.name)
        session = self.start_session_for(user)
        if user.has_permission(ADMIN_PERMISSION):
            session['menu'] = 'admin'
        else:
            session['menu'] = 'user'
        session['name'] = user.name
        encrypted_session = self.create_signed_value(name="session",
                                                     value=json.dumps(session))
        # We put some data in here so the client can know when the session
        # expires and what the user's name is, etc -but we never trust it.
        # Server-side we only trust values from the encrypted session `data`
        self.write({
            "username": user.name,
            "password": None,
            "data": encrypted_session,
            "expires": int(session['expires']),
            "is_admin": user.has_permission(ADMIN_PERMISSION),
            "debug": options.debug,
        })
