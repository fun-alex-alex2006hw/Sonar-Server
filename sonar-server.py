#!/usr/bin/env python
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
import os
import sys

import tornado.log
from tornado.options import Error, define, options

from libs.ConfigHelpers import save_config


def start():
    ''' Starts the application '''
    from handlers import start_server
    logging.info("Starting application server")
    start_server()


def setup():
    ''' Creates/bootstraps the database '''
    from setup import boot_strapper
    from setup.create_database import create_tables, engine, metadata
    logging.info('Creating the database ...')
    create_tables(engine, metadata, options.log_sql)
    logging.info('Bootstrapping the database ...')
    boot_strapper()


def parse_config_options():
    ''' Load up all of the cli and config file options '''
    app_root = os.path.abspath(__file__)
    os.chdir(os.path.dirname(app_root))
    tornado.log.enable_pretty_logging()
    try:
        options.parse_command_line()
        if os.path.isfile(options.config):
            logging.debug("Parsing config file `%s`",
                          os.path.abspath(options.config))
            options.parse_config_file(options.config)
        options.parse_command_line()  # CLI takes precedence
    except Error as error:
        logging.critical(str(error))
        sys.exit()


def main():
    '''
    Call functions in the correct order based on CLI params. It's important
    that we import and call stuff after proccessing all of the tornado.options,
    if you try to import something that uses tornado.options before we parse it
    you'll end up with lots of undefined variables!
    '''
    parse_config_options()
    if options.save:
        save_config()
    if options.setup is not None:
        setup()
    elif options.start:
        start()


###############################################################################
#                          Application Settings
###############################################################################
define("debug",
       default=False,
       group="debug",
       help="enable debugging mode",
       type=bool)


# Server configuration settings
define("listen_port",
       default=8888,
       group="server",
       help="run instances starting the given port",
       type=int)

define("x_headers",
       default=False,
       group="server",
       help="honor x-forwarded-for and x-real-ip",
       type=bool)

define("admin_ips",
       multiple=True,
       default=['127.0.0.1', '::1'],
       group="server",
       help="whitelist of ip addresses that can access the admin ui")


# Database settings
define("sql_dialect",
       default="mysql",
       group="database",
       help="define the type of database (mysql|postgres|sqlite)")

define("sql_database",
       default="sonar",
       group="database",
       help="the sql database name")

define("sql_host",
       default="127.0.0.1",
       group="database",
       help="database sever hostname")

define("sql_port",
       default=3306,
       group="database",
       help="database tcp port",
       type=int)

define("sql_user",
       default="sonar",
       group="database",
       help="database username")

define("sql_password",
       default="ranos",
       group="database",
       help="database password, if applicable")

define("sql_log",
       default=False,
       group="debug",
       help="log SQL queries for debugging")


# Execution modes
define("start",
       default=False,
       help="start the server",
       type=bool)

define("setup",
       default=None,
       help="setup a database (prod|devel)")

define("save",
       default=False,
       help="save the current configuration to file",
       type=bool)

define("config",
       default="files/all-is-dust.cfg",
       help="sonar configuration file")

define("wordlist",
       default=False,
       help="add a wordlist to the database",
       group="hashlookup",
       type=bool)

define("index",
       default=False,
       help="add an index to the database",
       group="hashlookup",
       type=bool)


if __name__ == '__main__':
    main()
