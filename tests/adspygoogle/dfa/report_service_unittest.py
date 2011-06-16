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

"""Unit tests to cover ReportService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import datetime
import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfa.DfaErrors import DfaRequestError
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import SERVER_V1_14
from tests.adspygoogle.dfa import TEST_VERSION_V1_13
from tests.adspygoogle.dfa import TEST_VERSION_V1_14
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import VERSION_V1_14


class ReportServiceTestV1_14(unittest.TestCase):

  """Unittest suite for ReportService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  service = None
  report_id = '-1'
  # There is no way to retrieve a query ID through the API. In order for these
  # tests to function, you must get a query ID through the web interface or the
  # Java DART API and enter it here.
  query_id = '-1'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetReport(self):
    """Test whether we can fetch a report by id"""
    if self.__class__.query_id == '-1':
      return
    elif self.__class__.report_id == '-1':
      self.testRunDeferredReport()
    report_request = {
        'reportId': self.__class__.report_id
    }
    self.assert_(isinstance(self.__class__.service.GetReport(report_request),
                            tuple))

  def testGetReports(self):
    """Test whether we can fetch reports by criteria."""
    if self.__class__.query_id == '-1':
      return
    report_search_criteria = {
        'queryId': self.__class__.query_id
    }
    self.assert_(isinstance(self.__class__.service.GetReportsByCriteria(
        report_search_criteria), tuple))

  def testRunDeferredReport(self):
    """Test whether we can schedule a deferred report"""
    if self.__class__.query_id == '-1':
      return
    report_request = {
        'queryId': self.__class__.query_id
    }
    response = self.__class__.service.RunDeferredReport(report_request)
    self.assert_(isinstance(response, tuple))
    self.__class__.report_id = response[0]['reportId']


class ReportServiceTestV1_13(unittest.TestCase):

  """Unittest suite for ReportService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  service = None
  report_id = '-1'
  # There is no way to retrieve a query ID through the API. In order for these
  # tests to function, you must get a query ID through the web interface or the
  # Java DART API and enter it here.
  query_id = '-1'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetReport(self):
    """Test whether we can fetch a report by id"""
    if self.__class__.query_id == '-1':
      return
    elif self.__class__.report_id == '-1':
      self.testRunDeferredReport()
    report_request = {
        'reportId': self.__class__.report_id
    }
    self.assert_(isinstance(self.__class__.service.GetReport(report_request),
                            tuple))

  def testGetReports(self):
    """Test whether we can fetch reports by criteria."""
    if self.__class__.query_id == '-1':
      return
    report_search_criteria = {
        'queryId': self.__class__.query_id
    }
    self.assert_(isinstance(self.__class__.service.GetReportsByCriteria(
        report_search_criteria), tuple))

  def testRunDeferredReport(self):
    """Test whether we can schedule a deferred report"""
    if self.__class__.query_id == '-1':
      return
    report_request = {
        'queryId': self.__class__.query_id
    }
    response = self.__class__.service.RunDeferredReport(report_request)
    self.assert_(isinstance(response, tuple))
    self.__class__.report_id = response[0]['reportId']


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV1_13))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_14:
    suites.append(makeTestSuiteV1_14())
  if TEST_VERSION_V1_13:
    suites.append(makeTestSuiteV1_13())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
