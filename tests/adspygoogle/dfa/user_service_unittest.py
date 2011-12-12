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

"""Unit tests to cover UserService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

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


class UserServiceTestV1_14(unittest.TestCase):

  """Unittest suite for UserService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  service = None
  user_self = None
  user_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testSaveUser(self):
    """Test whether we can save a user."""
    if self.__class__.user_self is None:
      self.testGetUsersByCriteria()
    network_id = self.__class__.user_self['networkId']
    subnetwork_id = self.__class__.user_self['subnetworkId']
    email_address = self.__class__.user_self['email']
    user_group_id = self.__class__.user_self['userGroupId']
    user = {
        'name': 'User%s' % Utils.GetUniqueName(),
        'password': 'password1234',
        'comments': 'Test user created by python library unit tests',
        'id' : '-1',
        'networkId': network_id,
        'subnetworkId': subnetwork_id,
        'email': email_address,
        'userGroupId': user_group_id
    }
    user = self.__class__.service.SaveUser(
        user)
    self.__class__.user_id = user[0]['id']
    self.assert_(isinstance(user, tuple))

  def testGetUser(self):
    """Test whether we can fetch a user by id."""
    if self.__class__.user_id == '0':
      self.testSaveUser()
    user_id = self.__class__.user_id
    self.assert_(isinstance(self.__class__.service.GetUser(
        user_id), tuple))

  def testGetUsersByCriteria(self):
    """Test whether we can fetch users by criteria. Attempts to fetch the user
    object associated with the DfaClient username.
    """
    search_criteria = {
        'searchString': client._headers['Username']
    }
    result = self.__class__.service.GetUsersByCriteria(search_criteria)
    self.__class__.user_self = result[0]['records'][0]
    self.assert_(isinstance(result, tuple))

  def testGenerateUniqueUsername(self):
    """Test whether we can generate a unique username."""
    if self.__class__.user_self is None:
      self.testGetUsersByCriteria()
    user_name = self.__class__.user_self['name']
    self.assert_(isinstance(self.__class__.service.GenerateUniqueUsername(
        user_name), tuple))

  def testGetAvailableTraffickerTypes(self):
    """Test whether we can fetch available trafficker types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableTraffickerTypes(), tuple))

  def testGetAvailableUserFilterCriteriaTypes(self):
    """Test whether we can fetch available user filter criteria types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableUserFilterCriteriaTypes(), tuple))

  def testGetAvailableUserFilterTypes(self):
    """Test whether we can fetch available user filter types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableUserFilterTypes(), tuple))

  def testSendUserInvitationEmail(self):
    """Test whether we can send a user invitation email."""
    if self.__class__.user_id == '0':
      self.testSaveUser()
    email_request = {
        'emailMessage': 'You have been sent a test e-mail from the Python '
                        'client library unit tests!',
        'emailSubject': 'Email #%s' % Utils.GetUniqueName(),
        'id': self.__class__.user_id
    }
    self.assertEquals(
        self.__class__.service.SendUserInvitationEmail(email_request), None)


class UserServiceTestV1_16(unittest.TestCase):

  """Unittest suite for UserService using v1_16."""

  SERVER = SERVER_V1_16
  VERSION = VERSION_V1_16
  client.debug = False
  service = None
  user_self = None
  user_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testSaveUser(self):
    """Test whether we can save a user."""
    if self.__class__.user_self is None:
      self.testGetUsersByCriteria()
    network_id = self.__class__.user_self['networkId']
    subnetwork_id = self.__class__.user_self['subnetworkId']
    email_address = self.__class__.user_self['email']
    user_group_id = self.__class__.user_self['userGroupId']
    user = {
        'name': 'User%s' % Utils.GetUniqueName(),
        'password': 'password1234',
        'comments': 'Test user created by python library unit tests',
        'id' : '-1',
        'networkId': network_id,
        'subnetworkId': subnetwork_id,
        'email': email_address,
        'userGroupId': user_group_id
    }
    user = self.__class__.service.SaveUser(
        user)
    self.__class__.user_id = user[0]['id']
    self.assert_(isinstance(user, tuple))

  def testGetUser(self):
    """Test whether we can fetch a user by id."""
    if self.__class__.user_id == '0':
      self.testSaveUser()
    user_id = self.__class__.user_id
    self.assert_(isinstance(self.__class__.service.GetUser(
        user_id), tuple))

  def testGetUsersByCriteria(self):
    """Test whether we can fetch users by criteria. Attempts to fetch the user
    object associated with the DfaClient username.
    """
    search_criteria = {
        'searchString': client._headers['Username']
    }
    result = self.__class__.service.GetUsersByCriteria(search_criteria)
    self.__class__.user_self = result[0]['records'][0]
    self.assert_(isinstance(result, tuple))

  def testGenerateUniqueUsername(self):
    """Test whether we can generate a unique username."""
    if self.__class__.user_self is None:
      self.testGetUsersByCriteria()
    user_name = self.__class__.user_self['name']
    self.assert_(isinstance(self.__class__.service.GenerateUniqueUsername(
        user_name), tuple))

  def testGetAvailableTraffickerTypes(self):
    """Test whether we can fetch available trafficker types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableTraffickerTypes(), tuple))

  def testGetAvailableUserFilterCriteriaTypes(self):
    """Test whether we can fetch available user filter criteria types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableUserFilterCriteriaTypes(), tuple))

  def testGetAvailableUserFilterTypes(self):
    """Test whether we can fetch available user filter types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableUserFilterTypes(), tuple))

  def testSendUserInvitationEmail(self):
    """Test whether we can send a user invitation email."""
    if self.__class__.user_id == '0':
      self.testSaveUser()
    email_request = {
        'emailMessage': 'You have been sent a test e-mail from the Python '
                        'client library unit tests!',
        'emailSubject': 'Email #%s' % Utils.GetUniqueName(),
        'id': self.__class__.user_id
    }
    self.assertEquals(
        self.__class__.service.SendUserInvitationEmail(email_request), None)


class UserServiceTestV1_15(unittest.TestCase):

  """Unittest suite for UserService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  service = None
  user_self = None
  user_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testSaveUser(self):
    """Test whether we can save a user."""
    if self.__class__.user_self is None:
      self.testGetUsersByCriteria()
    network_id = self.__class__.user_self['networkId']
    subnetwork_id = self.__class__.user_self['subnetworkId']
    email_address = self.__class__.user_self['email']
    user_group_id = self.__class__.user_self['userGroupId']
    user = {
        'name': 'User%s' % Utils.GetUniqueName(),
        'password': 'password1234',
        'comments': 'Test user created by python library unit tests',
        'id' : '-1',
        'networkId': network_id,
        'subnetworkId': subnetwork_id,
        'email': email_address,
        'userGroupId': user_group_id
    }
    user = self.__class__.service.SaveUser(
        user)
    self.__class__.user_id = user[0]['id']
    self.assert_(isinstance(user, tuple))

  def testGetUser(self):
    """Test whether we can fetch a user by id."""
    if self.__class__.user_id == '0':
      self.testSaveUser()
    user_id = self.__class__.user_id
    self.assert_(isinstance(self.__class__.service.GetUser(
        user_id), tuple))

  def testGetUsersByCriteria(self):
    """Test whether we can fetch users by criteria. Attempts to fetch the user
    object associated with the DfaClient username.
    """
    search_criteria = {
        'searchString': client._headers['Username']
    }
    result = self.__class__.service.GetUsersByCriteria(search_criteria)
    self.__class__.user_self = result[0]['records'][0]
    self.assert_(isinstance(result, tuple))

  def testGenerateUniqueUsername(self):
    """Test whether we can generate a unique username."""
    if self.__class__.user_self is None:
      self.testGetUsersByCriteria()
    user_name = self.__class__.user_self['name']
    self.assert_(isinstance(self.__class__.service.GenerateUniqueUsername(
        user_name), tuple))

  def testGetAvailableTraffickerTypes(self):
    """Test whether we can fetch available trafficker types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableTraffickerTypes(), tuple))

  def testGetAvailableUserFilterCriteriaTypes(self):
    """Test whether we can fetch available user filter criteria types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableUserFilterCriteriaTypes(), tuple))

  def testGetAvailableUserFilterTypes(self):
    """Test whether we can fetch available user filter types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableUserFilterTypes(), tuple))

  def testSendUserInvitationEmail(self):
    """Test whether we can send a user invitation email."""
    if self.__class__.user_id == '0':
      self.testSaveUser()
    email_request = {
        'emailMessage': 'You have been sent a test e-mail from the Python '
                        'client library unit tests!',
        'emailSubject': 'Email #%s' % Utils.GetUniqueName(),
        'id': self.__class__.user_id
    }
    self.assertEquals(
        self.__class__.service.SendUserInvitationEmail(email_request), None)


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserServiceTestV1_14))
  return suite


def makeTestSuiteV1_16():
  """Set up test suite using v1_16.

  Returns:
    TestSuite test suite using v1_16.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserServiceTestV1_16))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserServiceTestV1_15))
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
