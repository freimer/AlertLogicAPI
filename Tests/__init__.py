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

__version__ = '0.0.4'
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
        print('setUp AlertLogicAPITester')
        if 'customer_id' not in self.info:
            print('Loading / input for Alert Logic info')
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.alertlogic.json')) as f:
                self.info.update(json.load(f))
            if 'customer_id' not in self.info:
                self.info['customer_id'] = input('Enter Alert Logic Customer ID: ')
            if 'apikey' not in self.info:
                self.info['apikey'] = getpass.getpass('Enter API Key: ')
            if 'data_center' not in self.info:
                self.info['data_center'] = input('Enter Data Center [US, Ashburn, UK]: ')
            if 'verify_path' not in self.info:
                self.info['verify_path'] = input('Enter SSL Verify Path: ')
        else:
            print('Skipping load / input for Alert Logic info')
        self.client = AlertLogicAPI.Client(
            customer_id=self.info['customer_id'],
            apikey=self.info['apikey'],
            data_center=self.info['data_center'],
            verify_path=self.info['verify_path'])
        print('Created AlertLogic Client')


class GetProtectedHost(AlertLogicAPITester):
    def runTest(self):
        protectedhost_id = input('Enter Protected Host ID: ')
        print('Retrieving Protected Host')
        host = self.client.get_protected_host(protectedhost_id)


class GetProtectedHosts(AlertLogicAPITester):
    def runTest(self):
        hosts = self.client.get_protected_hosts(os_type='windows', offset=0, limit=2)
        print(json.dumps(hosts, indent=2))
