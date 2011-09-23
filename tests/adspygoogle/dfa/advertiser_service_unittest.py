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

"""Unit tests to cover AdvertiserService."""

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


class AdvertiserServiceTestV1_14(unittest.TestCase):

  """Unittest suite for AdvertiserService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  service = None
  advertiser1 = None
  advertiser2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testDeleteAdvertiser(self):
    """Test whether we can delete an advertiser."""
    if self.__class__.advertiser2 is None:
      self.testSaveAdvertiser()
    self.assertEqual(self.__class__.service.DeleteAdvertiser(
        self.__class__.advertiser2['id']), None)

  def testGetAdvertisers(self):
    """Test whether we can fetch advertisers."""
    if self.__class__.advertiser1 is None:
      self.testSaveAdvertiser()
    search_criteria = {
        'ids': [self.__class__.advertiser1['id']]
    }
    self.__class__.advertiser_id = self.__class__.service.GetAdvertisers(
        search_criteria)[0]['records'][0]['id']

  def testSaveAdvertiser(self):
    """Test whether we can create an advertiser."""
    advertiser = {
        'name': 'Advertiser #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser1 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))

    advertiser = {
        'name': '广告客户 #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser2 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))


class AdvertiserServiceTestV1_13(unittest.TestCase):

  """Unittest suite for AdvertiserService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  service = None
  advertiser1 = None
  advertiser2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testDeleteAdvertiser(self):
    """Test whether we can delete an advertiser."""
    if self.__class__.advertiser2 is None:
      self.testSaveAdvertiser()
    self.assertEqual(self.__class__.service.DeleteAdvertiser(
        self.__class__.advertiser2['id']), None)

  def testGetAdvertisers(self):
    """Test whether we can fetch advertisers."""
    if self.__class__.advertiser1 is None:
      self.testSaveAdvertiser()
    search_criteria = {
        'ids': [self.__class__.advertiser1['id']]
    }
    self.__class__.advertiser_id = self.__class__.service.GetAdvertisers(
        search_criteria)[0]['records'][0]['id']

  def testSaveAdvertiser(self):
    """Test whether we can create an advertiser."""
    advertiser = {
        'name': 'Advertiser #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser1 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))

    advertiser = {
        'name': '广告客户 #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser2 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))


class AdvertiserServiceTestV1_15(unittest.TestCase):

  """Unittest suite for AdvertiserService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  service = None
  advertiser1 = None
  advertiser2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdvertiserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testDeleteAdvertiser(self):
    """Test whether we can delete an advertiser."""
    if self.__class__.advertiser2 is None:
      self.testSaveAdvertiser()
    self.assertEqual(self.__class__.service.DeleteAdvertiser(
        self.__class__.advertiser2['id']), None)

  def testGetAdvertisers(self):
    """Test whether we can fetch advertisers."""
    if self.__class__.advertiser1 is None:
      self.testSaveAdvertiser()
    search_criteria = {
        'ids': [self.__class__.advertiser1['id']]
    }
    self.__class__.advertiser_id = self.__class__.service.GetAdvertisers(
        search_criteria)[0]['records'][0]['id']

  def testSaveAdvertiser(self):
    """Test whether we can create an advertiser."""
    advertiser = {
        'name': 'Advertiser #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser1 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))

    advertiser = {
        'name': '广告客户 #%s' % Utils.GetUniqueName(),
        'approved': 'true',
        'hidden': 'false'
    }
    advertiser = self.__class__.service.SaveAdvertiser(advertiser)
    self.__class__.advertiser2 = advertiser[0]
    self.assert_(isinstance(advertiser, tuple))


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdvertiserServiceTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdvertiserServiceTestV1_13))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdvertiserServiceTestV1_15))
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
