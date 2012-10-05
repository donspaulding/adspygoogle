#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests to cover AdWordsSanityCheck."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

import mock
from adspygoogle import AdWordsClient
from adspygoogle.common.Errors import ValidationError


class AdWordsSanityCheckTest(unittest.TestCase):
  """Tests for AdWordsSanityCheck."""

  def setUp(self):
    """Prepare unittest."""
    self.client = AdWordsClient(headers={'authToken': ' ',
                                         'userAgent': ' ',
                                         'developerToken': ' '})

  def testGetBulkMutateJobService_notAllowed(self):
    self.assertRaises(ValidationError, self.client.GetBulkMutateJobService,
                      version='v201209')

  def testGetBulkMutateJobService_allowed(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetBulkMutateJobService(version='v201206')
      self.assertEquals('BulkMutateJobService', service._service_name)

  def testGetBudgetService(self):
    with mock.patch('adspygoogle.SOAPpy.WSDL.Proxy'):
      service = self.client.GetBudgetService()
      self.assertEquals('BudgetService', service._service_name)


if __name__ == '__main__':
  unittest.main()
