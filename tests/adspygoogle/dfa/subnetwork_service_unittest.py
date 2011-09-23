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

"""Unit tests to cover SubnetworkService."""

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


class SubnetworkServiceTestV1_14(unittest.TestCase):

  """Unittest suite for SubnetworkService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  test_super_user = False
  service = None
  user_self = None
  subnetwork_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSubnetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveSubnetwork(self):
    """Test whether we can save a subnetwork"""
    if self.__class__.test_super_user:
      network_id = self.__class__.user_self['networkId']
      subnetwork = {
          'name': 'Subnetwork #%s' % Utils.GetUniqueName(),
          'networkId': network_id,
      }
      subnetwork = self.__class__.service.SaveSubnetwork(subnetwork)
      self.__class__.subnetwork_id = subnetwork[0]['id']
      self.assert_(isinstance(subnetwork, tuple))

  def testGetSubnetwork(self):
    """Test whether we can fetch a subnetwork by id."""
    subnetwork_id = self.__class__.user_self['subnetworkId']
    self.assert_(isinstance(self.__class__.service.GetSubnetwork(
        subnetwork_id), tuple))

  def testGetSubnetworks(self):
    """Test whether we can fetch subnetworks by criteria."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworks(
        search_criteria), tuple))

  def testGetSubnetworkSummaries(self):
    """Test whether we can fetch subnetwork summaries."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworkSummaries(
        search_criteria), tuple))

  def testGetAllAvailablePermissions(self):
    """Test whether we can fetch all available permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllAvailablePermissions(), tuple))

  def testGetDefaultPermissions(self):
    """Test whether we can fetch default permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetDefaultPermissions(), tuple))


class SubnetworkServiceTestV1_13(unittest.TestCase):

  """Unittest suite for SubnetworkService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  test_super_user = False
  service = None
  user_self = None
  subnetwork_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSubnetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveSubnetwork(self):
    """Test whether we can save a subnetwork"""
    if self.__class__.test_super_user:
      network_id = self.__class__.user_self['networkId']
      subnetwork = {
          'name': 'Subnetwork #%s' % Utils.GetUniqueName(),
          'networkId': network_id,
      }
      subnetwork = self.__class__.service.SaveSubnetwork(subnetwork)
      self.__class__.subnetwork_id = subnetwork[0]['id']
      self.assert_(isinstance(subnetwork, tuple))

  def testGetSubnetwork(self):
    """Test whether we can fetch a subnetwork by id."""
    subnetwork_id = self.__class__.user_self['subnetworkId']
    self.assert_(isinstance(self.__class__.service.GetSubnetwork(
        subnetwork_id), tuple))

  def testGetSubnetworks(self):
    """Test whether we can fetch subnetworks by criteria."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworks(
        search_criteria), tuple))

  def testGetSubnetworkSummaries(self):
    """Test whether we can fetch subnetwork summaries."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworkSummaries(
        search_criteria), tuple))

  def testGetAllAvailablePermissions(self):
    """Test whether we can fetch all available permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllAvailablePermissions(), tuple))

  def testGetDefaultPermissions(self):
    """Test whether we can fetch default permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetDefaultPermissions(), tuple))


class SubnetworkServiceTestV1_15(unittest.TestCase):

  """Unittest suite for SubnetworkService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  test_super_user = False
  service = None
  user_self = None
  subnetwork_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSubnetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveSubnetwork(self):
    """Test whether we can save a subnetwork"""
    if self.__class__.test_super_user:
      network_id = self.__class__.user_self['networkId']
      subnetwork = {
          'name': 'Subnetwork #%s' % Utils.GetUniqueName(),
          'networkId': network_id,
      }
      subnetwork = self.__class__.service.SaveSubnetwork(subnetwork)
      self.__class__.subnetwork_id = subnetwork[0]['id']
      self.assert_(isinstance(subnetwork, tuple))

  def testGetSubnetwork(self):
    """Test whether we can fetch a subnetwork by id."""
    subnetwork_id = self.__class__.user_self['subnetworkId']
    self.assert_(isinstance(self.__class__.service.GetSubnetwork(
        subnetwork_id), tuple))

  def testGetSubnetworks(self):
    """Test whether we can fetch subnetworks by criteria."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworks(
        search_criteria), tuple))

  def testGetSubnetworkSummaries(self):
    """Test whether we can fetch subnetwork summaries."""
    search_criteria = {
        'ids': [self.__class__.user_self['subnetworkId']]
    }
    self.assert_(isinstance(self.__class__.service.GetSubnetworkSummaries(
        search_criteria), tuple))

  def testGetAllAvailablePermissions(self):
    """Test whether we can fetch all available permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllAvailablePermissions(), tuple))

  def testGetDefaultPermissions(self):
    """Test whether we can fetch default permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetDefaultPermissions(), tuple))


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SubnetworkServiceTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SubnetworkServiceTestV1_13))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SubnetworkServiceTestV1_15))
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
