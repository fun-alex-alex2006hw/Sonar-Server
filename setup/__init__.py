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


import os
import logging
import hashlookup

from tornado.options import options
from models.Wordlist import Wordlist
from models.WordlistIndex import WordlistIndex
from models import dbsession
from libs.ValidationError import ValidationError


# EXPORTS
from setup.bootstrap import boot_strapper


def add_wordlist():
    if options.name is None:
        logging.critical("You must provide a name with --name")
        os._exit(1)
    if options.path is None:
        logging.critical("You must provide a path with --path")
        os._exit(1)
    try:
        wordlist = Wordlist(name=options.name, path=options.path)
        dbsession.add(wordlist)
        dbsession.commit()
    except ValidationError as error:
        logging.error("Failed to add wordlist: %s" % error)


def __determine_algorithm(wordlist_path, index_path):
    ''' Determine the algorithm by cracking passwords'''
    for key, Clazz in hashlookup.algorithms.iteritems():
        logging.debug("Attempting to discover: %s" % key)
        hsh = Clazz(options.pw_test).hexdigest()
        table = hashlookup.LookupTable(algorithm=key,
                                       index_file=index_path,
                                       wordlist_file=wordlist_path,
                                       verbose=options.debug)
        results = table[hsh]  # Returns a dict
        logging.debug("Results for %s were %r" % (key, results))
        if results[hsh] is not None and results[hsh] == options.pw_test:
            logging.debug("Deterimed algorithm of index '%s' to be '%s'" % (
                index_path, key))
            return key
    raise ValidationError("could not determine algorithm")


def __create_index(path):
    ''' Adds a given index to the database '''
    try:
        wordlist = Wordlist.by_name(options.name)
        if wordlist is None:
            raise ValidationError("Wordlist with name '%s' does not exist" % (
                options.name
            ))
        algorithm_key = options.algorithm
        if algorithm_key is None:
            algorithm_key = __determine_algorithm(wordlist.path, path)
        if algorithm_key is not None:
            idx = WordlistIndex(wordlist_id=wordlist.id,
                                algorithm=algorithm_key,
                                path=path)
            dbsession.add(idx)
            dbsession.commit()
    except ValidationError as error:
        logging.error("Failed to add index '%s', %s" % (path, error))


def add_index():
    ''' Add an index for a given wordlist, based on cli parameters '''
    if options.path is None:
        logging.critical("You must provide a path with --path")
        os._exit(1)
    if options.name is None:
        logging.critical("You must provide the wordlist name with --name")
        os._exit(1)
    if os.path.isfile(options.path):
        __create_index(options.path)
    elif os.path.isdir(options.path):
        logging.debug("The %s path is a directory ..." % options.path)
        for count, idx in enumerate(os.listdir(options.path)):
            idx_path = os.path.join(options.path, idx)
            if os.path.isfile(idx_path):
                logging.info("Adding index #%d at '%s'" % (count, idx_path))
                __create_index(idx_path)
