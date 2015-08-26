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


import getpass
import os
import sys

from tornado.options import options

from libs.ConsoleColors import INFO, PROMPT, R, W, WARN, bold
from models import dbsession
from models.Permission import Permission
from models.User import ADMIN_PERMISSION, User


def boot_strapper():
    # Fills the database with some startup data.
    _password = ""

    if options.setup.startswith('dev'):
        admin_user = u'admin'
        _password = 'nimda123'
    else:
        admin_user = unicode(raw_input(PROMPT + "Admin username: "))
        sys.stdout.write(PROMPT + "New Admin ")
        sys.stdout.flush()
        _password1 = getpass.getpass()
        sys.stdout.write(PROMPT + "Confirm New Admin ")
        sys.stdout.flush()
        _password2 = getpass.getpass()
        if _password1 == _password2 and 12 <= len(_password1):
            _password = _password1
        else:
            print(WARN +
                  'Error: Passwords did not match, or were less than 12 chars')
            os._exit(1)

    user = User(name=admin_user, password=_password)
    dbsession.add(user)
    dbsession.flush()
    admin_permission = Permission(name=ADMIN_PERMISSION, user_id=user.id)
    user.permissions.append(admin_permission)
    dbsession.add(admin_permission)
    dbsession.add(user)
    dbsession.commit()

    # Display Details
    if options.setup.startswith('dev'):
        environ = bold + R + "Developement boot strap" + W
        details = ", default admin password is '%s'." % _password
    else:
        environ = bold + "Production boot strap" + W
        details = '.'
    print INFO + '%s completed successfully%s' % (environ, details)
