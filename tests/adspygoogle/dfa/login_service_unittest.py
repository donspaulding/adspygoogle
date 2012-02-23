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

"""Unit tests to cover LoginService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_16
from tests.adspygoogle.dfa import SERVER_V1_15
from tests.adspygoogle.dfa import TEST_VERSION_V1_16
from tests.adspygoogle.dfa import TEST_VERSION_V1_15
from tests.adspygoogle.dfa import VERSION_V1_16
from tests.adspygoogle.dfa import VERSION_V1_15


class LoginServiceTestV1_16(unittest.TestCase):

  """Unittest suite for LoginService using v1_16."""

  SERVER = SERVER_V1_16
  VERSION = VERSION_V1_16
  client.debug = False
  test_super_user = False
  service = None
  auth_token = '0'
  user_to_impersonate = '0'
  network_to_impersonate = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLoginService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.test_super_user:
      if self.__class__.user_to_impersonate == '0':
        user_service = client.GetUserService(
            self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
        search_criteria = {
            'activeFilter': {
                'activeOnly': 'true'
            }
        }
        self.__class__.user_to_impersonate = user_service.GetUsersByCriteria(
            search_criteria)[0]['records'][0]['id']

      if self.__class__.network_to_impersonate == '0':
        user_service = client.GetUserService(
            self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
        search_criteria = {
            'searchString': client._headers['Username']
        }
        self.__class__.network_to_impersonate = user_service.GetUsersByCriteria(
            search_criteria)[0]['records'][0]['networkId']

  def testAuthenticate(self):
    """Test whether we can authenticate."""
    username = client._headers['Username']
    password = client._headers['Password']
    response = self.__class__.service.Authenticate(username, password)
    self.assert_(isinstance(response, tuple))
    self.__class__.auth_token = response[0]['token']

  def testImpersonateNetwork(self):
    """Test whether we can impersonate a network."""
    if self.__class__.test_super_user:
      if self.__class__.auth_token == '0':
        self.testAuthenticate()
      username = client._headers['Username']
      token = self.__class__.auth_token
      network_to_impersonate = self.__class__.network_to_impersonate
      self.assert_(isinstance(self.__class__.service.ImpersonateNetwork(
          username, token, network_to_impersonate), tuple))

  def testImpersonateUser(self):
    """Test whether we can impersonate a user."""
    if self.__class__.test_super_user:
      if self.__class__.auth_token == '0':
        self.testAuthenticate()
      username = client._headers['Username']
      token = self.__class__.auth_token
      user_to_impersonate = self.__class__.user_to_impersonate
      self.assert_(isinstance(self.__class__.service.ImpersonateUser(
          username, token, user_to_impersonate), tuple))


class LoginServiceTestV1_15(unittest.TestCase):

  """Unittest suite for LoginService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  test_super_user = False
  service = None
  auth_token = '0'
  user_to_impersonate = '0'
  network_to_impersonate = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetLoginService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.test_super_user:
      if self.__class__.user_to_impersonate == '0':
        user_service = client.GetUserService(
            self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
        search_criteria = {
            'activeFilter': {
                'activeOnly': 'true'
            }
        }
        self.__class__.user_to_impersonate = user_service.GetUsersByCriteria(
            search_criteria)[0]['records'][0]['id']

      if self.__class__.network_to_impersonate == '0':
        user_service = client.GetUserService(
            self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
        search_criteria = {
            'searchString': client._headers['Username']
        }
        self.__class__.network_to_impersonate = user_service.GetUsersByCriteria(
            search_criteria)[0]['records'][0]['networkId']

  def testAuthenticate(self):
    """Test whether we can authenticate."""
    username = client._headers['Username']
    password = client._headers['Password']
    response = self.__class__.service.Authenticate(username, password)
    self.assert_(isinstance(response, tuple))
    self.__class__.auth_token = response[0]['token']

  def testImpersonateNetwork(self):
    """Test whether we can impersonate a network."""
    if self.__class__.test_super_user:
      if self.__class__.auth_token == '0':
        self.testAuthenticate()
      username = client._headers['Username']
      token = self.__class__.auth_token
      network_to_impersonate = self.__class__.network_to_impersonate
      self.assert_(isinstance(self.__class__.service.ImpersonateNetwork(
          username, token, network_to_impersonate), tuple))

  def testImpersonateUser(self):
    """Test whether we can impersonate a user."""
    if self.__class__.test_super_user:
      if self.__class__.auth_token == '0':
        self.testAuthenticate()
      username = client._headers['Username']
      token = self.__class__.auth_token
      user_to_impersonate = self.__class__.user_to_impersonate
      self.assert_(isinstance(self.__class__.service.ImpersonateUser(
          username, token, user_to_impersonate), tuple))


def makeTestSuiteV1_16():
  """Set up test suite using v1_16.

  Returns:
    TestSuite test suite using v1_16.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LoginServiceTestV1_16))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LoginServiceTestV1_15))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_16:
    suites.append(makeTestSuiteV1_16())
  if TEST_VERSION_V1_15:
    suites.append(makeTestSuiteV1_15())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
