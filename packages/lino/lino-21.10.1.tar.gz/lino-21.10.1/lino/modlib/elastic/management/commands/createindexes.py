# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand

from lino.modlib.elastic.utils import ESResolver

class Command(BaseCommand):

    def handle(self, *args, **options):
        ESResolver.resolve_es_indexes()
        ESResolver.write_indexes()
