# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.test import RequestFactory
from django.test import TestCase

# Local application / specific library imports
from machina.apps.conversation.utils import get_client_ip


class TestIpAddressExtractor(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_can_determine_the_ip_address_with_the_http_x_forwarded_for_header(self):
        # Setup
        request = self.factory.get('/')
        parameters = request.META.copy()
        parameters['HTTP_X_FORWARDED_FOR'] = '10.13.108.124'
        request.META = parameters
        # Run
        ip_address = get_client_ip(request)
        # Check
        self.assertEqual(ip_address, '10.13.108.124')

    def test_can_determine_the_ip_address_with_the_remote_addr_header(self):
        # Setup
        request = self.factory.get('/')
        parameters = request.META.copy()
        parameters['HTTP_X_FORWARDED_FOR'] = None
        parameters['REMOTE_ADDR'] = '10.13.108.124'
        request.META = parameters
        # Run
        ip_address = get_client_ip(request)
        # Check
        self.assertEqual(ip_address, '10.13.108.124')