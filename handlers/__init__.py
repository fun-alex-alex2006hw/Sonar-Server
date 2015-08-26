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


import logging

from os import urandom
from tornado import netutil
from tornado.web import Application, StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options
from handlers.PublicHandlers import LoginAPIHandler, AppHandler
from handlers.ErrorHandlers import NotFoundHandler
from handlers.AdminHandlers import UserAPIHandler
from handlers.UserHandlers import SettingsAPIHandler



# Application setup
__VERSION = 'v0.0.1'
__HANDLERS = [

    # Main app
    (r'/', AppHandler),

    # Session management
    (r'/session', LoginAPIHandler),
    (r'/session/(.*)', LoginAPIHandler),

    # Settings for the current user
    (r'/me', SettingsAPIHandler),
    (r'/me/(.*)', SettingsAPIHandler),

    # Users - Admins only
    (r'/users', UserAPIHandler),
    (r'/users/(.*)', UserAPIHandler),

    # Static Handlers - Serves static CSS, JS, etc
    (r'/static/(.*\.(css|js|png|jpg|jpeg|gif|eot|svg|ttf|woff|woff2|otf))',
        StaticFileHandler, {'path': 'static/'}),

]


if options.debug:
    # Serves the unminified JavaScript client files and a .map
    JSCLIENT_MAP = (r'/static/(.*\.map)', StaticFileHandler,
                    {"path": "static/"})
    JSCLIENT_DEBUG = (r'/jsclient/app/(.*\.js)', StaticFileHandler,
                      {"path": "jsclient/app"})
    __HANDLERS.append(JSCLIENT_MAP)
    __HANDLERS.append(JSCLIENT_DEBUG)


# Catch-all handler must come last
__HANDLERS.append((r'(.*)', NotFoundHandler,))


__SONAR = Application(
    handlers=__HANDLERS,
    version=__VERSION,

    # Randomly generated secret key, if you forget to disable debug mode
    # then you're living in a state of sin, and deserve what you get.
    cookie_secret=urandom(32).encode('hex') if not options.debug else "debug",

    # Request that does not pass @authorized will be
    # redirected here
    forbidden_url='/#login',

    # Requests that does not pass @authenticated  will be
    # redirected here
    login_url='/#login',

    # Admin ip whitelist, affects @restrict_ip_address
    admin_ips=options.admin_ips,

    # Template directory
    template_path='templates/',

    # Enable XSRF forms
    xsrf_cookies=True,

    # Debug mode
    debug=options.debug,
)


def start_server():
    ''' Main entry point for the application '''
    sockets = netutil.bind_sockets(options.listen_port)
    server = HTTPServer(__SONAR, xheaders=options.x_headers)
    server.add_sockets(sockets)
    io_loop = IOLoop.instance()
    try:
        io_loop.start()
    except KeyboardInterrupt:
        logging.warn("Keyboard interrupt, shutdown everything!")
    finally:
        io_loop.stop()
