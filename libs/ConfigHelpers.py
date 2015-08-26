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
from datetime import datetime

from tornado.options import options


SKIP_GROUPS = ['allisdust.py', './allisdust.py', 'debug', 'hashlookup']


def save_config():
    logging.info("Saving current config to: %s" % options.config)
    with open(options.config, 'w') as fp:
        fp.write("##########################")
        fp.write(" Sonar Server  Config File ")
        fp.write("##########################\n")
        fp.write("# Last updated: %s\n" % datetime.now())
        for group in options.groups():
            if group.lower() in SKIP_GROUPS or group == '':
                continue
            fp.write("\n# [ %s ]\n" % group.title())
            for key, value in options.group_dict(group).iteritems():
                if isinstance(value, basestring):
                    # Str/Unicode needs to have quotes
                    fp.write(u'%s = "%s"\n' % (key, value))
                else:
                    # Int/Bool/List use __str__
                    fp.write('%s = %s\n' % (key, value))
