# Copyright 2008-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Intelligent search functionality.

Requires Elasticsearch to be installed.
"""

import os
import subprocess
from pathlib import Path

from django.conf import settings

from lino.api import ad

class Plugin(ad.Plugin):

    needs_plugins = ['lino.modlib.restful', 'elasticsearch_django']

    ES_url = 'localhost:9200' # running a docker instance locally
    """URL to the elasticsearch instance"""

    mappings_dir = Path(__file__).parent / 'search/mappings'

    debian_dev_server = False

    def on_init(self):
        super().on_init()
        from lino.modlib.elastic.utils import ESResolver
        sarset = {
            'connections': {
                'default': self.ES_url,
            },
            'indexes': ESResolver.read_indexes(),
            'settings': {
                'chunk_size': 500,
                'page_size': 15,
                'auto_sync': True,
                'strict_validation': False,
                'mappings_dir': self.mappings_dir,
                'never_auto_sync': [],
            }
        }
        self.site.update_settings(SEARCH_SETTINGS=sarset)

    def on_site_startup(self, site):
        from .utils import ESResolver
        # settings.SEARCH_SETTINGS['indexes'] = ESResolver.resolve_es_indexes(),
        # self.site.django_settings['SEARCH_SETTINGS']['indexes'] = ESResolver.read_indexes(),

        ESResolver.create_index_mapping_file(self.ES_url)
        ESResolver.populate_search_indexes_on_init()

    def get_requirements(self, site):
        yield 'elasticsearch-django'
