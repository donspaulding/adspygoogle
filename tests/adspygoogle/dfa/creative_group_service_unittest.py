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

"""Unit tests to cover CreativeGroupService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_11
from tests.adspygoogle.dfa import SERVER_V1_12
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import VERSION_V1_11
from tests.adspygoogle.dfa import VERSION_V1_12
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import client


class CreativeGroupServiceTestV1_13(unittest.TestCase):

  """Unittest suite for CreativeGroupService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  service = None
  creative_group_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testGetCreativeGroup(self):
    """Test whether we can fetch a creative group by id"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    creative_group_id = self.__class__.creative_group_id
    self.assert_(isinstance(self.__class__.service.GetCreativeGroup(
        creative_group_id), tuple))

  def testSaveCreativeGroup(self):
    """Test whether we can save a creative group"""
    creative_group = {
        'name': 'Creative Group #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'groupNumber' : '1',
        'id' : '-1'
    }
    creative_group = self.__class__.service.SaveCreativeGroup(
        creative_group)
    self.__class__.creative_group_id = creative_group[0]['id']
    self.assert_(isinstance(creative_group, tuple))

  def testGetCreativeGroups(self):
    """Test whether we can fetch creative groups by criteria."""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    search_criteria = {
        'ids': [self.__class__.creative_group_id]
    }
    self.__class__.creative_group_id = self.__class__.service.GetCreativeGroups(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeGroup(self):
    """Test whether we can delete a creative group"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    self.assertEqual(self.__class__.service.DeleteCreativeGroup(
        self.__class__.creative_group_id), None)
    self.__class__.creative_group_id = '0'


class CreativeGroupServiceTestV1_12(unittest.TestCase):

  """Unittest suite for CreativeGroupService using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  client.debug = False
  service = None
  creative_group_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testGetCreativeGroup(self):
    """Test whether we can fetch a creative group by id"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    creative_group_id = self.__class__.creative_group_id
    self.assert_(isinstance(self.__class__.service.GetCreativeGroup(
        creative_group_id), tuple))

  def testSaveCreativeGroup(self):
    """Test whether we can save a creative group"""
    creative_group = {
        'name': 'Creative Group #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'groupNumber' : '1',
        'id' : '-1'
    }
    creative_group = self.__class__.service.SaveCreativeGroup(
        creative_group)
    self.__class__.creative_group_id = creative_group[0]['id']
    self.assert_(isinstance(creative_group, tuple))

  def testGetCreativeGroups(self):
    """Test whether we can fetch creative groups by criteria."""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    search_criteria = {
        'ids': [self.__class__.creative_group_id]
    }
    self.__class__.creative_group_id = self.__class__.service.GetCreativeGroups(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeGroup(self):
    """Test whether we can delete a creative group"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    self.assertEqual(self.__class__.service.DeleteCreativeGroup(
        self.__class__.creative_group_id), None)
    self.__class__.creative_group_id = '0'


class CreativeGroupServiceTestV1_11(unittest.TestCase):

  """Unittest suite for CreativeGroupService using v1_11."""

  SERVER = SERVER_V1_11
  VERSION = VERSION_V1_11
  client.debug = False
  service = None
  creative_group_id = '0'
  advertiser_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCreativeGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.advertiser_id == '0':
      advertiser_service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.advertiser_id = advertiser_service.GetAdvertisers(
          search_criteria)[0]['records'][0]['id']

  def testGetCreativeGroup(self):
    """Test whether we can fetch a creative group by id"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    creative_group_id = self.__class__.creative_group_id
    self.assert_(isinstance(self.__class__.service.GetCreativeGroup(
        creative_group_id), tuple))

  def testSaveCreativeGroup(self):
    """Test whether we can save a creative group"""
    creative_group = {
        'name': 'Creative Group #%s' % Utils.GetUniqueName(),
        'advertiserId': self.__class__.advertiser_id,
        'groupNumber' : '1',
        'id' : '-1'
    }
    creative_group = self.__class__.service.SaveCreativeGroup(
        creative_group)
    self.__class__.creative_group_id = creative_group[0]['id']
    self.assert_(isinstance(creative_group, tuple))

  def testGetCreativeGroups(self):
    """Test whether we can fetch creative groups by criteria."""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    search_criteria = {
        'ids': [self.__class__.creative_group_id]
    }
    self.__class__.creative_group_id = self.__class__.service.GetCreativeGroups(
        search_criteria)[0]['records'][0]['id']

  def testDeleteCreativeGroup(self):
    """Test whether we can delete a creative group"""
    if self.__class__.creative_group_id == '0':
      self.testSaveCreativeGroup()
    self.assertEqual(self.__class__.service.DeleteCreativeGroup(
        self.__class__.creative_group_id), None)
    self.__class__.creative_group_id = '0'


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeGroupServiceTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeGroupServiceTestV1_12))
  return suite


def makeTestSuiteV1_11():
  """Set up test suite using v1_11.

  Returns:
    TestSuite test suite using v1_11.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CreativeGroupServiceTestV1_11))
  return suite


if __name__ == '__main__':
  suite_v1_13 = makeTestSuiteV1_13()
  suite_v1_12 = makeTestSuiteV1_12()
  suite_v1_11 = makeTestSuiteV1_11()
  alltests = unittest.TestSuite([suite_v1_13, suite_v1_12, suite_v1_11])
  unittest.main(defaultTest='alltests')
