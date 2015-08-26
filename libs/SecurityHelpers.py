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


import functools
import logging


def authenticated(method):
    ''' Checks to see if a user has been authenticated '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.session is not None:
            return method(self, *args, **kwargs)
        else:
            logging.debug("Unauthenticated request from %s; %r" % (
                self.request.remote_ip, self.get_current_user()))
            self.redirect(self.application.settings['login_url'])
    return wrapper


def restrict_ip_address(method):
    ''' Only allows access to ip addresses in a provided list '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.request.remote_ip in self.application.settings['admin_ips']:
            return method(self, *args, **kwargs)
        else:
            self.redirect(self.application.settings['forbidden_url'])
    return wrapper


def authorized(permission):
    ''' Checks user's permissions '''

    def func(method):

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.session is not None:
                user = self.get_current_user()
                if user is not None and user.has_permission(permission):
                    return method(self, *args, **kwargs)
            self.redirect(self.application.settings['forbidden_url'])
        return wrapper
    return func
