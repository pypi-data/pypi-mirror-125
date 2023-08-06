# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import requests
import json
from pathlib import Path
from urllib import parse

from django.apps import apps
from django.core.management import call_command

from lino.core.utils import get_models

class ESResolver:

    _resolved_indexes = None
    _resolved_json_indexes = None

    _indexes_file = Path(__file__).parent / 'search/indexes.json'

    @classmethod
    def get_models_by_index(cls, index, format_json=False):
        if format_json:
            return cls._resolved_json_indexes[index]['models']
        return cls._resolved_indexes[index]['models']

    @classmethod
    def write_indexes(cls, filename=None):
        if cls._resolved_json_indexes is None:
            cls.resolve_es_indexes()
        if filename is None:
            filename = cls._indexes_file
        with open(filename, 'w') as f:
            json.dump(cls._resolved_json_indexes, f)

    @classmethod
    def read_indexes(cls, filename=None):
        if filename is None:
            filename = cls._indexes_file
        obj = None
        with open(filename, 'r') as f:
            obj = json.load(f)

        cls._resolved_json_indexes = obj
        return cls._resolved_json_indexes

    @classmethod
    def get_index_build(cls):
        if cls._resolved_indexes is None:
            cls.resolve_es_indexes()
        return cls._resolved_indexes

    @classmethod
    def get_indexes(cls):
        return cls.get_index_build().keys()

    @classmethod
    def resolve_es_indexes(cls, fmt_json=False):
        if cls._resolved_indexes is None:
            idxs = dict()
            idxs_json = dict()
            for m in get_models():
                if hasattr(m, 'ES_indexes') and m.ES_indexes is not None:
                    indexes = [i[0] for i in m.ES_indexes]
                    for index in indexes:
                        if index not in idxs:
                            idxs[index] = {'models': []}
                            idxs_json[index] = {'models': []}
                        idxs_json[index]['models'].append(m._meta.app_label + "." + m.__name__)
                        idxs[index]['models'].append(m)

            cls._resolved_indexes = idxs
            cls._resolved_json_indexes = idxs_json
        if fmt_json:
            return cls._resolved_json_indexes
        return cls._resolved_indexes

    @classmethod
    def create_index_mapping_file(cls, url): # url => es_instance_url
        if parse.urlparse(url).scheme == "":
            url = 'http://' + url

        d = Path(__file__).parent / 'search/mappings'
        for index in cls.get_indexes():
            working_url = parse.urljoin(url, index)
            requests.put(working_url)
            file = d / (index + '.json')
            if file.exists():
                mode = 'w'
            else:
                mode = 'x'
            with open(file, mode) as f:
                resp = requests.get(working_url + '/_mapping')
                f.write(resp.content.decode())

    @classmethod
    def populate_search_indexes_on_init(cls):
        for index in cls.get_indexes():
            call_command('create_search_index', index)
            call_command('update_search_index', index)
