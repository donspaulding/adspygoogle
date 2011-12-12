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

"""Unit tests to cover SiteService."""

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


class SiteServiceTestV1_14(unittest.TestCase):

  """Unittest suite for SiteService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  service = None
  site_id = '0'
  directory_site_id = '0'
  user_self = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSiteService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveDfaSite(self):
    """Test whether we can save a site"""
    site = {
        'name': 'Site #%s' % Utils.GetUniqueName(),
        'countryId': '256', # USA
        'keyname': 'http://www.example.com'
    }
    site = self.__class__.service.SaveDfaSite(site)
    self.__class__.site_id = site[0]['id']
    self.assert_(isinstance(site, tuple))

  def testGetDfaSite(self):
    """Test whether we can fetch a site by id."""
    if self.__class__.site_id == '0':
      self.testSaveDfaSite()
    site_id = self.__class__.site_id
    self.assert_(isinstance(self.__class__.service.GetDfaSite(
        site_id), tuple))

  def testGetDfaSites(self):
    """Test whether we can fetch sites by criteria."""
    if self.__class__.site_id == '0':
      self.testSaveDfaSite()
    search_criteria = {
        'ids': [self.__class__.site_id]
    }
    self.assert_(isinstance(self.__class__.service.GetDfaSites(
        search_criteria), tuple))

  def testGetSitesByCriteria(self):
    """Test whether we can fetch sites by criteria."""
    search_criteria = {}
    results = self.__class__.service.GetSitesByCriteria(search_criteria)
    self.assert_(isinstance(results, tuple))
    self.__class__.directory_site_id = results[0]['records'][0]['id']

  def testGetAvailableDfaSiteContactTypes(self):
    """Test whether we can fetch available DFA site contact types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableDfaSiteContactTypes(), tuple))

  def testGetContacts(self):
    """Test whether we can fetch contacts."""
    contact_search_criteria = {
        'pageSize': '10',
        'pageNumber': '1'
    }
    self.assert_(isinstance(
        self.__class__.service.GetContacts(contact_search_criteria), tuple))


class SiteServiceTestV1_16(unittest.TestCase):

  """Unittest suite for SiteService using v1_16."""

  SERVER = SERVER_V1_16
  VERSION = VERSION_V1_16
  client.debug = False
  service = None
  site_id = '0'
  directory_site_id = '0'
  user_self = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSiteService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]

  def testSaveDfaSite(self):
    """Test whether we can save a site"""
    site = {
        'name': 'Site #%s' % Utils.GetUniqueName(),
        'countryId': '256', # USA
        'keyname': 'http://www.example.com'
    }
    site = self.__class__.service.SaveDfaSite(site)
    self.__class__.site_id = site[0]['id']
    self.assert_(isinstance(site, tuple))

  def testGetDfaSite(self):
    """Test whether we can fetch a site by id."""
    if self.__class__.site_id == '0':
      self.testSaveDfaSite()
    site_id = self.__class__.site_id
    self.assert_(isinstance(self.__class__.service.GetDfaSite(
        site_id), tuple))

  def testGetDfaSites(self):
    """Test whether we can fetch sites by criteria."""
    if self.__class__.site_id == '0':
      self.testSaveDfaSite()
    search_criteria = {
        'ids': [self.__class__.site_id]
    }
    self.assert_(isinstance(self.__class__.service.GetDfaSites(
        search_criteria), tuple))

  def testGetSitesByCriteria(self):
    """Test whether we can fetch sites by criteria."""
    search_criteria = {}
    results = self.__class__.service.GetSitesByCriteria(search_criteria)
    self.assert_(isinstance(results, tuple))
    self.__class__.directory_site_id = results[0]['records'][0]['id']

  def testGetAvailableDfaSiteContactTypes(self):
    """Test whether we can fetch available DFA site contact types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableDfaSiteContactTypes(), tuple))

  def testGetContacts(self):
    """Test whether we can fetch contacts."""
    contact_search_criteria = {
        'pageSize': '10',
        'pageNumber': '1'
    }
    self.assert_(isinstance(
        self.__class__.service.GetContacts(contact_search_criteria), tuple))


class SiteServiceTestV1_15(unittest.TestCase):

  """Unittest suite for SiteService using v1_15."""

  SERVER = SERVER_V1_15
  VERSION = VERSION_V1_15
  client.debug = False
  service = None
  site_id = '0'
  directory_site_id = '0'
  user_self = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSiteService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.user_self is None:
      user_service = client.GetUserService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {
          'searchString': client._headers['Username']
      }
      self.__class__.user_self = user_service.GetUsersByCriteria(
          search_criteria)[0]['records'][0]
  def testSaveDfaSite(self):
    """Test whether we can save a site"""
    site = {
        'name': 'Site #%s' % Utils.GetUniqueName(),
        'countryId': '256', # USA
        'keyname': 'http://www.example.com'
    }
    site = self.__class__.service.SaveDfaSite(site)
    self.__class__.site_id = site[0]['id']
    self.assert_(isinstance(site, tuple))

  def testGetDfaSite(self):
    """Test whether we can fetch a site by id."""
    if self.__class__.site_id == '0':
      self.testSaveDfaSite()
    site_id = self.__class__.site_id
    self.assert_(isinstance(self.__class__.service.GetDfaSite(
        site_id), tuple))

  def testGetDfaSites(self):
    """Test whether we can fetch sites by criteria."""
    if self.__class__.site_id == '0':
      self.testSaveDfaSite()
    search_criteria = {
        'ids': [self.__class__.site_id]
    }
    self.assert_(isinstance(self.__class__.service.GetDfaSites(
        search_criteria), tuple))

  def testGetSitesByCriteria(self):
    """Test whether we can fetch sites by criteria."""
    search_criteria = {}
    results = self.__class__.service.GetSitesByCriteria(search_criteria)
    self.assert_(isinstance(results, tuple))
    self.__class__.directory_site_id = results[0]['records'][0]['id']

  def testGetAvailableDfaSiteContactTypes(self):
    """Test whether we can fetch available DFA site contact types."""
    self.assert_(isinstance(
        self.__class__.service.GetAvailableDfaSiteContactTypes(), tuple))

  def testGetContacts(self):
    """Test whether we can fetch contacts."""
    contact_search_criteria = {
        'pageSize': '10',
        'pageNumber': '1'
    }
    self.assert_(isinstance(
        self.__class__.service.GetContacts(contact_search_criteria), tuple))


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SiteServiceTestV1_14))
  return suite


def makeTestSuiteV1_16():
  """Set up test suite using v1_16.

  Returns:
    TestSuite test suite using v1_16.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SiteServiceTestV1_16))
  return suite


def makeTestSuiteV1_15():
  """Set up test suite using v1_15.

  Returns:
    TestSuite test suite using v1_15.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SiteServiceTestV1_15))
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
