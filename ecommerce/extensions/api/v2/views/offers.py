from __future__ import unicode_literals

import hashlib

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from oscar.core.loading import get_model
from rest_framework import viewsets

from ecommerce.extensions.api.serializers import ConditionalOfferSerialitzer

ConditionalOffer = get_model('offer', 'ConditionalOffer')
Condition = get_model('offer', 'Condition')
Benefit = get_model('offer', 'Benefit')
Range = get_model('offer', 'Range')


class OfferViewSet(viewsets.ModelViewSet):
    queryset = ConditionalOffer.objects.filter(offer_type=ConditionalOffer.SITE)
    serializer_class = ConditionalOfferSerialitzer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            # create Range
            #   - name same as Product name
            #   - get courses from Program ID on Course Catalog
            # create Benefit
            # create Condition
            # create ConditionalOffer
            pass

    def get_program(self, program_uuid):
        cache_key = 'program_{uuid}'.format(uuid=program_uuid)
        cache_key = hashlib.md5(cache_key).hexdigest()
        program = cache.get(cache_key)
        if not program:
            api = self.request.site.siteconfiguration.course_catalog_api_client
            program = api.programs(program_uuid).get()
            cache.set(cache_key, program, settings.PROGRAM_CACHE_TIMEOUT)
        return program

    def create_range(self, program_uuid):
        """ Create an Oscar Range for the program. """
        pass
