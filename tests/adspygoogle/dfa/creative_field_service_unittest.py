#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unit tests to cover CreativeFieldService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_12
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import SERVER_V1_14
from tests.adspygoogle.dfa import TEST_VERSION_V1_12
from tests.adspygoogle.dfa import TEST_VERSION_V1_13
from tests.adspygoogle.dfa import TEST_VERSION_V1_14
from tests.adspygoogle.dfa import VERSION_V1_12
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import VERSION_V1_14


class CreativeFieldServiceTestV1_14(unittest.TestCase):

  """Unittest suite for CreativeFieldService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = True
  service = None
  creative_field_id = '0'
  creative_field_value_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeFieldService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      advertiser = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]
      creative_field_search_criteria = {'advertiserIds': [advertiser['id']]}
      results = self.__class__.service.GetCreativeFields(
          creative_field_search_criteria)[0]
      if results['records']:
        for creative_field in results['records']:
          self.__class__.service.DeleteCreativeField(creative_field['id'])
      self.__class__.advertiser_id = advertiser['id']

  def testGetCreativeField(self):
    """Test whether we can fetch a creative field by id"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    creative_field_id = self.__class__.creative_field_id
    self.assert_(isinstance(self.__class__.service.GetCreativeField(
        creative_field_id), tuple))

  def testSaveCreativeField(self):
    """Test whether we can save a creative field"""
    creative_field = {
        'name': 'Field #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'id' : '-1'
    }
    creative_field = self.__class__.service.SaveCreativeField(
        creative_field)
    self.__class__.creative_field_id = creative_field[0]['id']
    self.assert_(isinstance(creative_field, tuple))

  def testGetCreativeFields(self):
    """Test whether we can fetch creative fields by criteria."""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    search_criteria = {
        'ids': [self.__class__.creative_field_id]
    }
    self.__class__.creative_field_id = self.__class__.service.GetCreativeFields(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeField(self):
    """Test whether we can delete a creative field"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    self.assertEqual(self.__class__.service.DeleteCreativeField(
        self.__class__.creative_field_id), None)
    self.__class__.creative_field_id = '0'

  def testGetCreativeFieldValue(self):
    """Test whether we can fetch a creative field value by id"""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    creative_field_value_id = self.__class__.creative_field_value_id
    self.assert_(isinstance(self.__class__.service.GetCreativeFieldValue(
        creative_field_value_id), tuple))

  def testSaveCreativeFieldValue(self):
    """Test whether we can save a creative field value"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    creative_field_value = {
        'name': 'FieldValue #%s' % Utils.GetUniqueName(),
        'creativeFieldId': self.__class__.creative_field_id,
        'id' : '-1'
    }
    creative_field_value = self.__class__.service.SaveCreativeFieldValue(
        creative_field_value)
    self.__class__.creative_field_value_id = creative_field_value[0]['id']
    self.assert_(isinstance(creative_field_value, tuple))

  def testGetCreativeFieldValues(self):
    """Test whether we can fetch creative field values by criteria."""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    search_criteria = {
        'ids': [self.__class__.creative_field_value_id]
    }
    self.__class__.creative_field_value_id = \
        self.__class__.service.GetCreativeFieldValues(search_criteria)[0][
            'records'][0]['id']

  def testDeleteCreativeFieldValue(self):
    """Test whether we can delete a creative field value"""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    self.assertEqual(self.__class__.service.DeleteCreativeFieldValue(
        self.__class__.creative_field_value_id), None)
    self.__class__.creative_field_value_id = '0'


class CreativeFieldServiceTestV1_13(unittest.TestCase):

  """Unittest suite for CreativeFieldService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = True
  service = None
  creative_field_id = '0'
  creative_field_value_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeFieldService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      advertiser = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]
      creative_field_search_criteria = {'advertiserIds': [advertiser['id']]}
      results = self.__class__.service.GetCreativeFields(
          creative_field_search_criteria)[0]
      if results['records']:
        for creative_field in results['records']:
          self.__class__.service.DeleteCreativeField(creative_field['id'])
      self.__class__.advertiser_id = advertiser['id']

  def testGetCreativeField(self):
    """Test whether we can fetch a creative field by id"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    creative_field_id = self.__class__.creative_field_id
    self.assert_(isinstance(self.__class__.service.GetCreativeField(
        creative_field_id), tuple))

  def testSaveCreativeField(self):
    """Test whether we can save a creative field"""
    creative_field = {
        'name': 'Field #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'id' : '-1'
    }
    creative_field = self.__class__.service.SaveCreativeField(
        creative_field)
    self.__class__.creative_field_id = creative_field[0]['id']
    self.assert_(isinstance(creative_field, tuple))

  def testGetCreativeFields(self):
    """Test whether we can fetch creative fields by criteria."""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    search_criteria = {
        'ids': [self.__class__.creative_field_id]
    }
    self.__class__.creative_field_id = self.__class__.service.GetCreativeFields(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeField(self):
    """Test whether we can delete a creative field"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    self.assertEqual(self.__class__.service.DeleteCreativeField(
        self.__class__.creative_field_id), None)
    self.__class__.creative_field_id = '0'

  def testGetCreativeFieldValue(self):
    """Test whether we can fetch a creative field value by id"""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    creative_field_value_id = self.__class__.creative_field_value_id
    self.assert_(isinstance(self.__class__.service.GetCreativeFieldValue(
        creative_field_value_id), tuple))

  def testSaveCreativeFieldValue(self):
    """Test whether we can save a creative field value"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    creative_field_value = {
        'name': 'FieldValue #%s' % Utils.GetUniqueName(),
        'creativeFieldId': self.__class__.creative_field_id,
        'id' : '-1'
    }
    creative_field_value = self.__class__.service.SaveCreativeFieldValue(
        creative_field_value)
    self.__class__.creative_field_value_id = creative_field_value[0]['id']
    self.assert_(isinstance(creative_field_value, tuple))

  def testGetCreativeFieldValues(self):
    """Test whether we can fetch creative field values by criteria."""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    search_criteria = {
        'ids': [self.__class__.creative_field_value_id]
    }
    self.__class__.creative_field_value_id = \
        self.__class__.service.GetCreativeFieldValues(search_criteria)[0][
            'records'][0]['id']

  def testDeleteCreativeFieldValue(self):
    """Test whether we can delete a creative field value"""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    self.assertEqual(self.__class__.service.DeleteCreativeFieldValue(
        self.__class__.creative_field_value_id), None)
    self.__class__.creative_field_value_id = '0'


class CreativeFieldServiceTestV1_12(unittest.TestCase):

  """Unittest suite for CreativeFieldService using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  client.debug = True
  service = None
  creative_field_id = '0'
  creative_field_value_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeFieldService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      advertiser = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]
      creative_field_search_criteria = {'advertiserIds': [advertiser['id']]}
      results = self.__class__.service.GetCreativeFields(
          creative_field_search_criteria)[0]
      if results['records']:
        for creative_field in results['records']:
          self.__class__.service.DeleteCreativeField(creative_field['id'])
      self.__class__.advertiser_id = advertiser['id']

  def testGetCreativeField(self):
    """Test whether we can fetch a creative field by id"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    creative_field_id = self.__class__.creative_field_id
    self.assert_(isinstance(self.__class__.service.GetCreativeField(
        creative_field_id), tuple))

  def testSaveCreativeField(self):
    """Test whether we can save a creative field"""
    creative_field = {
        'name': 'Field #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'id' : '-1'
    }
    creative_field = self.__class__.service.SaveCreativeField(
        creative_field)
    self.__class__.creative_field_id = creative_field[0]['id']
    self.assert_(isinstance(creative_field, tuple))

  def testGetCreativeFields(self):
    """Test whether we can fetch creative fields by criteria."""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    search_criteria = {
        'ids': [self.__class__.creative_field_id]
    }
    self.__class__.creative_field_id = self.__class__.service.GetCreativeFields(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeField(self):
    """Test whether we can delete a creative field"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    self.assertEqual(self.__class__.service.DeleteCreativeField(
        self.__class__.creative_field_id), None)
    self.__class__.creative_field_id = '0'

  def testGetCreativeFieldValue(self):
    """Test whether we can fetch a creative field value by id"""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    creative_field_value_id = self.__class__.creative_field_value_id
    self.assert_(isinstance(self.__class__.service.GetCreativeFieldValue(
        creative_field_value_id), tuple))

  def testSaveCreativeFieldValue(self):
    """Test whether we can save a creative field value"""
    if self.__class__.creative_field_id == '0':
      self.testSaveCreativeField()
    creative_field_value = {
        'name': 'FieldValue #%s' % Utils.GetUniqueName(),
        'creativeFieldId': self.__class__.creative_field_id,
        'id' : '-1'
    }
    creative_field_value = self.__class__.service.SaveCreativeFieldValue(
        creative_field_value)
    self.__class__.creative_field_value_id = creative_field_value[0]['id']
    self.assert_(isinstance(creative_field_value, tuple))

  def testGetCreativeFieldValues(self):
    """Test whether we can fetch creative field values by criteria."""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    search_criteria = {
        'ids': [self.__class__.creative_field_value_id]
    }
    self.__class__.creative_field_value_id = \
        self.__class__.service.GetCreativeFieldValues(search_criteria)[0][
            'records'][0]['id']

  def testDeleteCreativeFieldValue(self):
    """Test whether we can delete a creative field value"""
    if self.__class__.creative_field_value_id == '0':
      self.testSaveCreativeFieldValue()
    self.assertEqual(self.__class__.service.DeleteCreativeFieldValue(
        self.__class__.creative_field_value_id), None)
    self.__class__.creative_field_value_id = '0'


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeFieldServiceTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeFieldServiceTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeFieldServiceTestV1_12))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_14:
    suites.append(makeTestSuiteV1_14())
  if TEST_VERSION_V1_13:
    suites.append(makeTestSuiteV1_13())
  if TEST_VERSION_V1_12:
    suites.append(makeTestSuiteV1_12())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
