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

"""Unit tests to cover AdvertiserGroupService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import SERVER_V1_14
from tests.adspygoogle.dfa import SERVER_V1_15
from tests.adspygoogle.dfa import TEST_VERSION_V1_13
from tests.adspygoogle.dfa import TEST_VERSION_V1_14
from tests.adspygoogle.dfa import TEST_VERSION_V1_15
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import VERSION_V1_14
from tests.adspygoogle.dfa import VERSION_V1_15


class AdvertiserGroupServiceTestV1_14(unittest.TestCase):

  """Unittest suite for AdvertiserGroupService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  service = None
  advertiser_group1 = None
  advertiser_group2 = None
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testDeleteAdvertiserGroup(self):
    """Test whether we can delete advertiser group."""
    if self.__class__.advertiser_group2 is None:
      self.testSaveAdvertiserGroup()
    self.assertEqual(self.__class__.service.DeleteAdvertiserGroup(
        self.__class__.advertiser_group2['id']), None)

  def testGetAdvertiserGroup(self):
    """Test whether we can fetch advertiser group."""
    if self.__class__.advertiser_group1 is None:
      self.testSaveAdvertiserGroup()
    self.assert_(isinstance(self.__class__.service.GetAdvertiserGroup(
        self.__class__.advertiser_group1['id']), tuple))

  def testGetAdvertiserGroups(self):
    """Test whether we can fetch advertiser groups."""
    search_criteria = {
        'sortOrder': {
            'fieldName': 'id',
            'descending': 'false'
        }
    }
    self.assert_(isinstance(self.__class__.service.GetAdvertiserGroups(
        search_criteria), tuple))

  def testSaveAdvertiserGroup(self):
    """Test whether we can create an advertiser group."""
    advertiser_group = {
        'name': 'AdvertiserGroup #%s' % Utils.GetUniqueName()
    }
    advertiser_group = self.__class__.service.SaveAdvertiserGroup(
        advertiser_group)
    self.__class__.advertiser_group1 = advertiser_group[0]
    self.assert_(isinstance(advertiser_group, tuple))

    advertiser_group = {
        'name': 'AdvertiserGroup #%s' % Utils.GetUniqueName()
    }
    advertiser_group = self.__class__.service.SaveAdvertiserGroup(
        advertiser_group)
    self.__class__.advertiser_group2 = advertiser_group[0]
    self.assert_(isinstance(advertiser_group, tuple))

  def testAssignAdvertisersToAdvertiserGroup(self):
    """Test whether we can assign advertisers to an advertiser group."""
    if self.__class__.advertiser_group1 is None:
      self.testSaveAdvertiserGroup()
    self.assertEqual(self.__class__.service.AssignAdvertisersToAdvertiserGroup(
        self.__class__.advertiser_group1['id'], [self.__class__.advertiser_id]),
        None)


class AdvertiserGroupServiceTestV1_13(unittest.TestCase):

  """Unittest suite for AdvertiserGroupService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  service = None
  advertiser_group1 = None
  advertiser_group2 = None
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testDeleteAdvertiserGroup(self):
    """Test whether we can delete advertiser group."""
    if self.__class__.advertiser_group2 is None:
      self.testSaveAdvertiserGroup()
    self.assertEqual(self.__class__.service.DeleteAdvertiserGroup(
        self.__class__.advertiser_group2['id']), None)

  def testGetAdvertiserGroup(self):
    """Test whether we can fetch advertiser group."""
    if self.__class__.advertiser_group1 is None:
      self.testSaveAdvertiserGroup()
    self.assert_(isinstance(self.__class__.service.GetAdvertiserGroup(
        self.__class__.advertiser_group1['id']), tuple))

  def testGetAdvertiserGroups(self):
    """Test whether we can fetch advertiser groups."""
    search_criteria = {
        'sortOrder': {
            'fieldName': 'id',
            'descending': 'false'
        }
    }
    self.assert_(isinstance(self.__class__.service.GetAdvertiserGroups(
        search_criteria), tuple))

  def testSaveAdvertiserGroup(self):
    """Test whether we can create an advertiser group."""
    advertiser_group = {
        'name': 'AdvertiserGroup #%s' % Utils.GetUniqueName()
    }
    advertiser_group = self.__class__.service.SaveAdvertiserGroup(
        advertiser_group)
    self.__class__.advertiser_group1 = advertiser_group[0]
    self.assert_(isinstance(advertiser_group, tuple))

    advertiser_group = {
        'name': 'AdvertiserGroup #%s' % Utils.GetUniqueName()
    }
    advertiser_group = self.__class__.service.SaveAdvertiserGroup(
        advertiser_group)
    self.__class__.advertiser_group2 = advertiser_group[0]
    self.assert_(isinstance(advertiser_group, tuple))

  def testAssignAdvertisersToAdvertiserGroup(self):
    """Test whether we can assign advertisers to an advertiser group."""
    if self.__class__.advertiser_group1 is None:
      self.testSaveAdvertiserGroup()
    self.assertEqual(self.__class__.service.AssignAdvertisersToAdvertiserGroup(
        self.__class__.advertiser_group1['id'], [self.__class__.advertiser_id]),
        None)


class AdvertiserGroupServiceTestV1_15(unittest.TestCase):

  """Unittest suite for AdvertiserGroupService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  service = None
  advertiser_group1 = None
  advertiser_group2 = None
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testDeleteAdvertiserGroup(self):
    """Test whether we can delete advertiser group."""
    if self.__class__.advertiser_group2 is None:
      self.testSaveAdvertiserGroup()
    self.assertEqual(self.__class__.service.DeleteAdvertiserGroup(
        self.__class__.advertiser_group2['id']), None)

  def testGetAdvertiserGroup(self):
    """Test whether we can fetch advertiser group."""
    if self.__class__.advertiser_group1 is None:
      self.testSaveAdvertiserGroup()
    self.assert_(isinstance(self.__class__.service.GetAdvertiserGroup(
        self.__class__.advertiser_group1['id']), tuple))

  def testGetAdvertiserGroups(self):
    """Test whether we can fetch advertiser groups."""
    search_criteria = {
        'sortOrder': {
            'fieldName': 'id',
            'descending': 'false'
        }
    }
    self.assert_(isinstance(self.__class__.service.GetAdvertiserGroups(
        search_criteria), tuple))

  def testSaveAdvertiserGroup(self):
    """Test whether we can create an advertiser group."""
    advertiser_group = {
        'name': 'AdvertiserGroup #%s' % Utils.GetUniqueName()
    }
    advertiser_group = self.__class__.service.SaveAdvertiserGroup(
        advertiser_group)
    self.__class__.advertiser_group1 = advertiser_group[0]
    self.assert_(isinstance(advertiser_group, tuple))

    advertiser_group = {
        'name': 'AdvertiserGroup #%s' % Utils.GetUniqueName()
    }
    advertiser_group = self.__class__.service.SaveAdvertiserGroup(
        advertiser_group)
    self.__class__.advertiser_group2 = advertiser_group[0]
    self.assert_(isinstance(advertiser_group, tuple))

  def testAssignAdvertisersToAdvertiserGroup(self):
    """Test whether we can assign advertisers to an advertiser group."""
    if self.__class__.advertiser_group1 is None:
      self.testSaveAdvertiserGroup()
    self.assertEqual(self.__class__.service.AssignAdvertisersToAdvertiserGroup(
        self.__class__.advertiser_group1['id'], [self.__class__.advertiser_id]),
        None)


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdvertiserGroupServiceTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdvertiserGroupServiceTestV1_13))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdvertiserGroupServiceTestV1_15))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_14:
    suites.append(makeTestSuiteV1_14())
  if TEST_VERSION_V1_13:
    suites.append(makeTestSuiteV1_13())
  if TEST_VERSION_V1_15:
    suites.append(makeTestSuiteV1_15())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
