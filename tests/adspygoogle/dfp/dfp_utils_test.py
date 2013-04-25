#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""Unit tests to cover DfpUtils."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock
from adspygoogle import DfpClient
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import DfpUtils


class DfpUtilsTest(unittest.TestCase):

  """Unittest suite for DfpUtils."""

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in DfpUtils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in DfpUtils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testGetAllEntitiesByStatement(self):
    client = mock.Mock()
    line_item_service = mock.Mock()
    rval = 'Line items for everyone!'

    def VerifyExpectedCall(arg):
      self.assertEqual({'values': None,
                        'query': 'ORDER BY name LIMIT 500 OFFSET 0'}, arg)
      return [{'results': [rval]}]

    client.GetLineItemService.return_value = line_item_service
    line_item_service._service_name = 'LineItemService'
    line_item_service.GetLineItemsByStatement.side_effect = VerifyExpectedCall

    line_items = DfpUtils.GetAllEntitiesByStatement(
        client, 'LineItem', 'ORDER BY name')
    self.assertEqual([rval], line_items)

  def testGetAllEntitiesByStatementWithLimit(self):
    """Test whether GetAllEntitiesByStatement() fails when LIMIT is provided."""
    headers = {
        'email': ' ',
        'password': ' ',
        'applicationName': ' ',
        'authToken': ' '
    }
    client = DfpClient(headers=headers)
    self.failUnlessRaises(
        ValidationError, DfpUtils.GetAllEntitiesByStatement,
        client, 'User', 'ORDER BY name LIMIT 1')

  def testGetAllEntitiesByStatementWithService(self):
    line_item_service = mock.Mock()
    rval = 'Line items for everyone!'

    def VerifyExpectedCall(arg):
      self.assertEqual({'values': None,
                        'query': 'ORDER BY name LIMIT 500 OFFSET 0'}, arg)
      return [{'results': [rval]}]

    line_item_service._service_name = 'LineItemService'
    line_item_service.GetLineItemsByStatement.side_effect = VerifyExpectedCall

    line_items = DfpUtils.GetAllEntitiesByStatementWithService(
        line_item_service, 'ORDER BY name')
    self.assertEqual([rval], line_items)


if __name__ == '__main__':
  unittest.main()
