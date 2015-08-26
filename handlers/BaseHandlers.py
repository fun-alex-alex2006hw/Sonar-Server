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


import hmac
import json
import logging
import os
import time

from tornado.escape import utf8
from tornado.options import options
from tornado.web import HTTPError, RequestHandler, decode_signed_value

from libs.APIConstants import SESSION_EXPIRES
from libs.ValidationError import ValidationError
from models.User import User


class BaseHandler(RequestHandler):

    ''' User handlers extend this class '''

    csp = {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "connect-src": ["'self'"],
        "frame-src": ["'none'"],
        "frame-ancestors": ["'none'"],
        "child-src": ["'none'"],
        "img-src": ["'self'"],
        "media-src": ["'none'"],
        "form-action": ["'self'", "http://export.highcharts.com/"],
        "reflected-xss": ["block"],
        "font-src": [
            "'self'",
            "https://fonts.googleapis.com",
            "https://fonts.gstatic.com"
        ],
        "object-src": ["'none'"],
        "style-src": [
            "'self'",
            "'unsafe-inline'",  # Not ideal, but used a lot by Highcharts
            "https://fonts.googleapis.com",
        ],
    }

    def initialize(self):
        self.config = options
        self._session = None
        self._user = None

    def get_current_user(self):
        ''' Get current user object from database '''
        if self.session is not None:
            if self._user is None:
                self._user = User.by_id(self.session['user_id'])
            return self._user
        return None

    @property
    def session(self):
        ''' Lazily get the session  data '''
        if self._session is None:
            self._session = self.get_session()
        return self._session

    def start_session_for(self, user):
        ''' Starts a new session '''
        session = {
            'user_id': user.id,
            'expires': int(time.time()) + SESSION_EXPIRES,
        }
        return session

    def get_session(self):
        ''' Decrypt, deserialze session object, check the timestamp too '''
        try:
            data = self.request.headers.get('X-ALL-IS-DUST', None)
            if data is not None:
                session = json.loads(decode_signed_value(
                    secret=self.application.settings["cookie_secret"],
                    name="session",
                    value=data))
                if time.time() <= session['expires']:
                    return session
            else:
                logging.debug("Unauthenticated, no session data")
        except:
            logging.exception("Failed to deserialze session data")
        return None

    def set_default_headers(self):
        ''' Set clickjacking/xss headers '''
        self.set_header("Server", "COME-AT-ME-BRO")
        self.add_header("X-Frame-Options", "DENY")
        self.add_header("X-XSS-Protection", "1; mode=block")
        self.add_header("X-Content-Type-Options", "nosniff")
        self._refresh_csp()

    def add_content_policy(self, src, policy):
        ''' Add to the existing CSP header '''
        if not src.endswith('-src'):
            src += '-src'
        if src in self.csp:
            self.csp[src].add(policy)
            self._refresh_csp()
        else:
            raise ValueError("Invalid content source")

    def clear_content_policy(self, src):
        ''' Clear a content source in the existing CSP header '''
        if not src.endswith('-src'):
            src += '-src'
        if src in self.csp:
            self.csp[src] = []
            self._refresh_csp()
        else:
            raise ValueError("Invalid content source")

    def _refresh_csp(self):
        ''' Rebuild the Content-Security-Policy header '''
        _csp = []
        for src, policies in self.csp.iteritems():
            if len(policies):
                _csp.append("%s %s; " % (src, " ".join(policies)))
        csp = ''.join(_csp)
        self.set_header("Content-Security-Policy", csp)

    def set_xsrf_token(self):
        self.set_cookie("_xsrf", os.urandom(18).encode('base64').strip())

    def get(self):
        ''' Placeholder, incase child class does not impl this method '''
        pass

    def post(self):
        ''' Placeholder, incase child class does not impl this method '''
        pass

    def put(self):
        ''' Log odd behavior, this should never get legitimately called '''
        logging.warn("%s attempted to use PUT method", self.request.remote_ip)

    def delete(self):
        ''' Log odd behavior, this should never get legitimately called '''
        logging.warn("%s attempted to use DELETE method",
                     self.request.remote_ip)

    def head(self):
        ''' Ignore it '''
        logging.warn("%s attempted to use HEAD method", self.request.remote_ip)

    def options(self):
        ''' Log odd behavior, this should never get legitimately called '''
        logging.warn("%s attempted to use OPTIONS method",
                     self.request.remote_ip)

    def check_xsrf_cookie(self):
        '''
        Overloaded to avoid bullshit with the way cookies are handled.
        '''
        token = (self.get_argument("_xsrf", None) or
                 self.request.headers.get("X-Xsrftoken") or
                 self.request.headers.get("X-Csrftoken"))
        token = token.replace('"', '')
        if not token or len(token) < 5:
            raise HTTPError(403, "'_xsrf' argument missing from POST")
        _, token, _ = self._decode_xsrf_token(token)
        _, expected_token, _ = self._get_raw_xsrf_token()
        if not hmac.compare_digest(utf8(token), utf8(expected_token)):
            raise HTTPError(403, "XSRF cookie does not match POST argument")


class APIBaseHandler(BaseHandler):

    '''
    This is a nice little wrapper to make it easier for classes to handle and
    respond to JSON requests in the Backbone.js format.
    '''

    def initialize(self):
        self.set_header("Content-type", "application/json")
        self.config = options
        self._session = None
        self._user = None
        # This is our anti-json hijacking header, it should be in GETs
        if self.request.headers.get("X-SONAR", None) is None:
            # No header? Drop dat request
            raise HTTPError(403, "Missing header X-SONAR")
        try:
            if len(self.request.body):
                self.api_request = json.loads(self.request.body)
            else:
                self.api_request = None
        except ValidationError as error:
            self.set_status(500)
            self.write({"error": str(error)})
        except:
            logging.exception("%sException while parsing request body: %r",
                              "\nURL: %s\n" % self.request.uri,
                              self.request.body)

    def get_argument(self, name, default=None):
        '''
        Instead of pulling from the body or GET parameters, we pull from the
        JSON body of the request, and expose an identical API. If there was no
        request body, we just return `None', falling back to calling super()
        or pulling arguments from the URI could introduce security problems.
        '''
        if self.api_request is not None:
            return self.api_request.get(name, default)

    def get_uri_argument(self, name, default=None):
        ''' If we really need to pull normal arguments '''
        return super(APIBaseHandler, self).get_argument(name, default)
