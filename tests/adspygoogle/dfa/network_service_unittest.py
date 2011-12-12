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

"""Unit tests to cover NetworkService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import base64
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_16
from tests.adspygoogle.dfa import SERVER_V1_14
from tests.adspygoogle.dfa import SERVER_V1_15
from tests.adspygoogle.dfa import TEST_VERSION_V1_16
from tests.adspygoogle.dfa import TEST_VERSION_V1_14
from tests.adspygoogle.dfa import TEST_VERSION_V1_15
from tests.adspygoogle.dfa import VERSION_V1_16
from tests.adspygoogle.dfa import VERSION_V1_14
from tests.adspygoogle.dfa import VERSION_V1_15


class NetworkServiceTestV1_14(unittest.TestCase):

  """Unittest suite for NetworkService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  test_super_user = False
  service = None
  user_self = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveNetwork(self):
    """Test whether we can save a network"""
    if self.__class__.test_super_user:
      network = {
          'name': 'Network #%s' % Utils.GetUniqueName(),
      }
      network = self.__class__.service.SaveNetwork(network)
      self.__class__.network_id = network[0]['id']
      self.assert_(isinstance(network, tuple))

  def testGetNetworks(self):
    """Test whether we can fetch networks by criteria."""
    if self.__class__.test_super_user:
      search_criteria = {
          'ids': [self.__class__.user_self['networkId']]
      }
      self.assert_(isinstance(self.__class__.service.GetNetworks(
          search_criteria), tuple))

  def testGetNetwork(self):
    """Test whether we can fetch a network by id."""
    network_id = self.__class__.user_self['networkId']
    self.assert_(isinstance(self.__class__.service.GetNetwork(
        network_id), tuple))

  def testGetAdministratorPermissions(self):
    """Test whether we can fetch administrator permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAdministratorPermissions(), tuple))

  def testGetAllNetworkPermissions(self):
    """Test whether we can fetch all network permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllNetworkPermissions(), tuple))

  def testGetAllPermissions(self):
    """Test whether we can fetch all permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllPermissions(), tuple))

  def testGetAssignedNetworkPermissions(self):
    """Test whether we can fetch all network permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAssignedNetworkPermissions(
            self.__class__.user_self['networkId']), tuple))

  def testGetCurrencies(self):
    """Test whether we can fetch currencies."""
    self.assert_(isinstance(
        self.__class__.service.GetCurrencies(), tuple))

  def testGetLanguageEncodingList(self):
    """Test whether we can fetch supported language encodings."""
    self.assert_(isinstance(
        self.__class__.service.GetLanguageEncodingList(), tuple))

  def testGetTimeZoneList(self):
    """Test whether we can fetch support time zones."""
    self.assert_(isinstance(
        self.__class__.service.GetTimeZoneList(), tuple))

  def testUploadNetworkWidgetImage(self):
    """Test whether we can upload a widget backup image."""
    image = Utils.ReadFile(os.path.join('data', 'code_logo.gif'))
    image = base64.encodestring(image)
    widget_image_upload_request = {
        'network': self.__class__.user_self['networkId'],
        'filedata': image,
        'filename': 'testImage.gif',
        'networkWidgetImageUpload': 'true'
    }
    self.assert_(isinstance(
        self.__class__.service.UploadNetworkWidgetImage(
            widget_image_upload_request), tuple))


class NetworkServiceTestV1_16(unittest.TestCase):

  """Unittest suite for NetworkService using v1_16."""

  SERVER = SERVER_V1_16
  VERSION = VERSION_V1_16
  client.debug = False
  test_super_user = False
  service = None
  user_self = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveNetwork(self):
    """Test whether we can save a network"""
    if self.__class__.test_super_user:
      network = {
          'name': 'Network #%s' % Utils.GetUniqueName(),
      }
      network = self.__class__.service.SaveNetwork(network)
      self.__class__.network_id = network[0]['id']
      self.assert_(isinstance(network, tuple))

  def testGetNetworks(self):
    """Test whether we can fetch networks by criteria."""
    if self.__class__.test_super_user:
      search_criteria = {
          'ids': [self.__class__.user_self['networkId']]
      }
      self.assert_(isinstance(self.__class__.service.GetNetworks(
          search_criteria), tuple))

  def testGetNetwork(self):
    """Test whether we can fetch a network by id."""
    network_id = self.__class__.user_self['networkId']
    self.assert_(isinstance(self.__class__.service.GetNetwork(
        network_id), tuple))

  def testGetAdministratorPermissions(self):
    """Test whether we can fetch administrator permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAdministratorPermissions(), tuple))

  def testGetAllNetworkPermissions(self):
    """Test whether we can fetch all network permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllNetworkPermissions(), tuple))

  def testGetAllPermissions(self):
    """Test whether we can fetch all permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllPermissions(), tuple))

  def testGetAssignedNetworkPermissions(self):
    """Test whether we can fetch all network permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAssignedNetworkPermissions(
            self.__class__.user_self['networkId']), tuple))

  def testGetCurrencies(self):
    """Test whether we can fetch currencies."""
    self.assert_(isinstance(
        self.__class__.service.GetCurrencies(), tuple))

  def testGetLanguageEncodingList(self):
    """Test whether we can fetch supported language encodings."""
    self.assert_(isinstance(
        self.__class__.service.GetLanguageEncodingList(), tuple))

  def testGetTimeZoneList(self):
    """Test whether we can fetch support time zones."""
    self.assert_(isinstance(
        self.__class__.service.GetTimeZoneList(), tuple))

  def testUploadNetworkWidgetImage(self):
    """Test whether we can upload a widget backup image."""
    image = Utils.ReadFile(os.path.join('data', 'code_logo.gif'))
    image = base64.encodestring(image)
    widget_image_upload_request = {
        'network': self.__class__.user_self['networkId'],
        'filedata': image,
        'filename': 'testImage.gif',
        'networkWidgetImageUpload': 'true'
    }
    self.assert_(isinstance(
        self.__class__.service.UploadNetworkWidgetImage(
            widget_image_upload_request), tuple))


class NetworkServiceTestV1_15(unittest.TestCase):

  """Unittest suite for NetworkService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  test_super_user = False
  service = None
  user_self = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetNetworkService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveNetwork(self):
    """Test whether we can save a network"""
    if self.__class__.test_super_user:
      network = {
          'name': 'Network #%s' % Utils.GetUniqueName(),
      }
      network = self.__class__.service.SaveNetwork(network)
      self.__class__.network_id = network[0]['id']
      self.assert_(isinstance(network, tuple))

  def testGetNetworks(self):
    """Test whether we can fetch networks by criteria."""
    if self.__class__.test_super_user:
      search_criteria = {
          'ids': [self.__class__.user_self['networkId']]
      }
      self.assert_(isinstance(self.__class__.service.GetNetworks(
          search_criteria), tuple))

  def testGetNetwork(self):
    """Test whether we can fetch a network by id."""
    network_id = self.__class__.user_self['networkId']
    self.assert_(isinstance(self.__class__.service.GetNetwork(
        network_id), tuple))

  def testGetAdministratorPermissions(self):
    """Test whether we can fetch administrator permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAdministratorPermissions(), tuple))

  def testGetAllNetworkPermissions(self):
    """Test whether we can fetch all network permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllNetworkPermissions(), tuple))

  def testGetAllPermissions(self):
    """Test whether we can fetch all permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAllPermissions(), tuple))

  def testGetAssignedNetworkPermissions(self):
    """Test whether we can fetch all network permissions."""
    self.assert_(isinstance(
        self.__class__.service.GetAssignedNetworkPermissions(
            self.__class__.user_self['networkId']), tuple))

  def testGetCurrencies(self):
    """Test whether we can fetch currencies."""
    self.assert_(isinstance(
        self.__class__.service.GetCurrencies(), tuple))

  def testGetLanguageEncodingList(self):
    """Test whether we can fetch supported language encodings."""
    self.assert_(isinstance(
        self.__class__.service.GetLanguageEncodingList(), tuple))

  def testGetTimeZoneList(self):
    """Test whether we can fetch support time zones."""
    self.assert_(isinstance(
        self.__class__.service.GetTimeZoneList(), tuple))

  def testUploadNetworkWidgetImage(self):
    """Test whether we can upload a widget backup image."""
    image = Utils.ReadFile(os.path.join('data', 'code_logo.gif'))
    image = base64.encodestring(image)
    widget_image_upload_request = {
        'network': self.__class__.user_self['networkId'],
        'filedata': image,
        'filename': 'testImage.gif',
        'networkWidgetImageUpload': 'true'
    }
    self.assert_(isinstance(
        self.__class__.service.UploadNetworkWidgetImage(
            widget_image_upload_request), tuple))


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV1_14))
  return suite


def makeTestSuiteV1_16():
  """Set up test suite using v1_16.

  Returns:
    TestSuite test suite using v1_16.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV1_16))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(NetworkServiceTestV1_15))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_14:
    suites.append(makeTestSuiteV1_14())
  if TEST_VERSION_V1_16:
    suites.append(makeTestSuiteV1_16())
  if TEST_VERSION_V1_15:
    suites.append(makeTestSuiteV1_15())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
