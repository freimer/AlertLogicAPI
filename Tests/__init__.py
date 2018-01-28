# Copyright 2018 Frederick Reimer.
#
# This file is part of the AlertLogicAPI Python Package.
#
# AlertLogicAPI  Python Package is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# AlertLogicAPI  Python Package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# AlertLogicAPI Python Package.  If not, see <http://www.gnu.org/licenses/>.

__version__ = '0.0.6'
__author__ = 'Fred Reimer <freimer@freimer.org>'
__copyright__ = "Frederick Reimer"
__license__ = "GPL v3"

import unittest
import json
import os
import os.path
import getpass
import AlertLogicAPI


class AlertLogicAPITester(unittest.TestCase):
    info = {}

    def setUp(self):
        """Setup with AlertLogic account information

        """
        if 'customer_id' not in self.info:
            with open(os.path.expanduser('~/.alertlogic.json')) as f:
                self.info.update(json.load(f))
            if 'customer_id' not in self.info:
                self.info['customer_id'] = input('Enter Alert Logic Customer ID: ')
            if 'apikey' not in self.info:
                self.info['apikey'] = getpass.getpass('Enter API Key: ')
            if 'data_center' not in self.info:
                self.info['data_center'] = input('Enter Data Center [US, Ashburn, UK]: ')
            if 'verify_path' not in self.info:
                self.info['verify_path'] = input('Enter SSL Verify Path: ')
        self.client = AlertLogicAPI.Client(
            customer_id=self.info['customer_id'],
            apikey=self.info['apikey'],
            data_center=self.info['data_center'],
            verify_path=self.info['verify_path'])


# class GetProtectedHost(AlertLogicAPITester):
#     def runTest(self):
#         """Test get_protected_host method of AlertLogicAPI.Client
#
#         """
#         protectedhost_id = input('Enter Protected Host ID: ')
#         host = self.client.get_protected_host(protectedhost_id)
#         self.assertIsInstance(host, dict)
#
#
class GetProtectedHosts(AlertLogicAPITester):
    def runTest(self):
        """Test get_protected_hosts method of AlertLogicAPI.Client

        """
        hosts = self.client.get_protected_hosts(os_type='windows', offset=0, limit=2)
        self.assertIsInstance(hosts, list)


class UpdateProtectedHost(AlertLogicAPITester):
    @staticmethod
    def _get_tags(host: dict) -> list:
        tags = []
        if 'tags' in host:
            for tag in host['tags']:
                tags.append(tag['name'])
        return tags

    def runTest(self):
        """Test the update_protected_host method of AlertLogicAPI.Client

        This retrieves the first windows host, lists the tags, adds a tag, updates the host, then retrieves the host
        again to confirm the change, then resets the existing tags.

        """
        host = self.client.get_protected_hosts(type='host', offset=0, limit=1, os_type='windows')[0]
        tags = self._get_tags(host)
        tags.append('AlertLogicAPITester.UpdateProtectedHost')
        host = self.client.update_protected_host(protectedhost_id=host['id'], tags=tags)
        tags = self._get_tags(host)
        self.assertIn('AlertLogicAPITester.UpdateProtectedHost', tags, 'tag not successfully added')
        tags.remove('AlertLogicAPITester.UpdateProtectedHost')
        host = self.client.update_protected_host(protectedhost_id=host['id'], tags=tags)
        tags = self._get_tags(host)
        self.assertNotIn('AlertLogicAPITester.UpdateProtectedHost', tags, 'tag not successfully removed')


class GetKeypairs(AlertLogicAPITester):
    def runTest(self):
        """Test get_keypairs method of AlertLogicAPI.Client

        """
        keypairs = self.client.get_keypairs()
        self.assertIsInstance(keypairs, list)


class CreateKeypair(AlertLogicAPITester):
    def runTest(self):
        """Test create_keypair method of AlertLogicAPI.Client

        """
        keypair = self.client.create_keypair(
            name='test-cert',
            host='0.0.0.0',
            certificate_path=os.path.expanduser('~/test-cert.pem'),
            private_key_path=os.path.expanduser('~/test-cert.enckey'),
            private_key_password=self.info['private_key_password']
        )
        self.assertIsInstance(keypair, dict)


class DeleteKeypair(AlertLogicAPITester):
    def runTest(self):
        """Test delete_keypair method of AlertLogicAPI.Client

        """
        keypair = self.client.create_keypair(
            name='test-cert',
            host='0.0.0.0',
            certificate_path=os.path.expanduser('~/test-cert.pem'),
            private_key_path=os.path.expanduser('~/test-cert.key')
        )
        self.assertIsInstance(keypair, dict)
        self.client.delete_keypair(keypair_id=keypair['id'])
