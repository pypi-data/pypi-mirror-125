# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.db.models import Manager

from lino.api import dd, rt, _
from lino.modlib.restful.serializers import get_serializer_for_model

from .utils import ESResolver

class SearchDocumentMixin:
    pass

class SearchDocumentManagerMixin(Manager):
    pass

if dd.is_installed('elastic') and settings.SITE.use_elasticsearch:
    try:
        from elasticsearch_django.models import SearchDocumentMixin
        from elasticsearch_django.models import SearchDocumentManagerMixin
        from elasticsearch_django.models import execute_search
        from elasticsearch_django.settings import get_client
        from elasticsearch_dsl import Search

        search = Search(using=get_client())

    except ImportError:
        pass

class ElasticSearchableManager(SearchDocumentManagerMixin):
    def get_search_queryset(self, index='_all'):
        return self.get_queryset()


class ElasticSearchable(dd.Model, SearchDocumentMixin):

    class Meta:
        abstract = True

    objects = ElasticSearchableManager()

    ES_indexes = [('global', )]
    """Set of elastic search indexes, (when installed)."""

    def as_search_document(self, index):
        serializer = self.build_document(index)
        if serializer is None:
            return {}
        data = serializer(self).data
        data.update(model='rt.models.' + self._meta.app_label + '.' + self.__class__.__name__)
        return data

    def build_document(self, index):
        for i in self.ES_indexes:
            if i[0] == index:
                models = ESResolver.get_models_by_index(index)
                if len(models) == 1:
                    assert models[0] == self.__class__
                    return get_serializer_for_model(self.__class__)
                elif len(i) == 1:
                    return get_serializer_for_model(self.__class__)
                else:
                    options = i[1]
                    child = options.get('child', None)
                    if child is not None:
                        child_serializer = get_sesializer_for_model(eval('rt.models.' + child))
                        return get_serializer_for_model(self.__class__, {
                            'extra_fields': {
                                child.split('.')[0].lower() + '_set': child_serializer
                            }
                        })


class ElasticSearch(dd.VirtualTable):

    @classmethod
    def get_data_rows(cls, ar):
        index = 'discussion'
        query = ar.quick_search
        query_dict = {
            'query': {
                'query_string': {
                    'query': query
                }
            }
        }
        search.update_from_dict(query_dict)
        sq = execute_search(search, save=False)
        print('^'*80)
        print(sq.hits)
        # print(sq.hits[0])

        objs = []

        # for m in ESResolver.get_models_by_index(index):
        #     print('~'*80)
        #     print(m)
        #     for obj in m.objects.from_search_query(sq):
        #         print('>'*80)
        #         print(obj.search_score)
        #         objs.append(obj)
        #
        # objs = sorted(objs, key=lambda obj: obj.search_score)
        # print('='*80)
        # print(objs)
        # # for obj in objs:
        # #     yield obj
        # return objs
