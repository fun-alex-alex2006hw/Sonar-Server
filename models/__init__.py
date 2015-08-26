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


import time
import logging

from tornado.options import options
from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from libs.DatabaseConnection import DatabaseConnection
from libs.ConsoleColors import R, BLU, W, bold


# Since this will result in basically *everything* in the databse getting
# logged to stdout/text we only allow it to be enabled if --debug is also used.
if options.debug and options.sql_log:

    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)

    # This benchmarks the amount of time spent quering the database
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters,
                              context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters,
                             context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        color = R if total > 0.01 else BLU
        logging.debug("Total query time: %s%s%f%s" % (bold, color, total, W))


db_connection = DatabaseConnection(database=options.sql_database,
                                   hostname=options.sql_host,
                                   port=options.sql_port,
                                   username=options.sql_user,
                                   password=options.sql_password,
                                   dialect=options.sql_dialect)

# Setup the database session
engine = create_engine(str(db_connection))
_Session = sessionmaker(bind=engine)
dbsession = _Session(autoflush=True)
