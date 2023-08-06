# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from rest_framework import serializers

def get_choice_list_field_serializer():
    class ChoiceListField(serializers.Field):
        def to_representation(self, value):
            print('*'*80)
            print(value)
            return value.text

        def to_internal_value(self, data):
            pass

    return ChoiceListField
