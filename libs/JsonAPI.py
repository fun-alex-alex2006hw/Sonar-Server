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

from libs.ValidationError import ValidationError

# Session expires in `x` seconds
SESSION_EXPIRES = 3600  # 1 hr

# HTTP 400
BAD_REQUEST = 400
FAILED_REQUEST = 500
FORBIDDEN = 403  # Not authenticated
NOT_AUTHORIZED = 418
NOT_FOUND = 404


def json_api_method(method):

    '''
    A simple method wrapper that catches ValidationError(s) and returns them to
    the client in a consistent JSON error format. Removes the need to have lots
    of try/except blocks in the class methods.
    '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except (ValueError, NameError):
            logging.exception("Failed to parse API request")
            self.set_status(BAD_REQUEST)
            self.write({"errors": ["Cannot parse request"]})
            self.finish()
        except ValidationError as error:
            self.set_status(BAD_REQUEST)
            self.write({"errors": [str(error)]})
            self.finish()
    return wrapper
