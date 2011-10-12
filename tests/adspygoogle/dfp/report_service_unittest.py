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

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.dfp import client
from tests.adspygoogle.dfp import HTTP_PROXY
from tests.adspygoogle.dfp import SERVER_V201103
from tests.adspygoogle.dfp import SERVER_V201104
from tests.adspygoogle.dfp import SERVER_V201107
from tests.adspygoogle.dfp import SERVER_V201108
from tests.adspygoogle.dfp import VERSION_V201103
from tests.adspygoogle.dfp import VERSION_V201104
from tests.adspygoogle.dfp import VERSION_V201107
from tests.adspygoogle.dfp import VERSION_V201108


class ReportServiceTestV201103(unittest.TestCase):

  """Unittest suite for ReportService using v201103."""

  SERVER = SERVER_V201103
  VERSION = VERSION_V201103
  client.debug = False
  service = None
  report_job_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testRunDeliveryReport(self):
    """Test whether we can run a delivery report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['ORDER'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'AD_SERVER_CTR', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    report_job = self.__class__.service.RunReportJob(report_job)
    self.__class__.report_job_id = report_job[0]['id']
    self.assert_(isinstance(report_job, tuple))

  def testRunInventoryReport(self):
    """Test whether we can run an inventory report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['DATE'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'ADSENSE_IMPRESSIONS', 'ADSENSE_CLICKS',
                        'TOTAL_IMPRESSIONS', 'TOTAL_REVENUE'],
            'dateRangeType': 'LAST_WEEK'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testRunSalesReport(self):
    """Test whether we can run a sales report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['SALESPERSON'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testGetReportJob(self):
    """Test whether we can retrieve existing report job."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportJob(
        self.__class__.report_job_id), tuple))

  def testGetReportDownloadUrl(self):
    """Test whether we can retrieve report download URL."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportDownloadURL(
        self.__class__.report_job_id, 'CSV'), tuple))

  def testDownloadCsvReport(self):
    """Test whether we can download a CSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'CSV'), str))

  def testDownloadTsvReport(self):
    """Test whether we can download a TSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'TSV'), str))


class ReportServiceTestV201104(unittest.TestCase):

  """Unittest suite for ReportService using v201104."""

  SERVER = SERVER_V201104
  VERSION = VERSION_V201104
  client.debug = False
  service = None
  report_job_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testRunDeliveryReport(self):
    """Test whether we can run a delivery report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['ORDER'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'AD_SERVER_CTR', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    report_job = self.__class__.service.RunReportJob(report_job)
    self.__class__.report_job_id = report_job[0]['id']
    self.assert_(isinstance(report_job, tuple))

  def testRunInventoryReport(self):
    """Test whether we can run an inventory report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['DATE'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'ADSENSE_IMPRESSIONS', 'ADSENSE_CLICKS',
                        'TOTAL_IMPRESSIONS', 'TOTAL_REVENUE'],
            'dateRangeType': 'LAST_WEEK'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testRunSalesReport(self):
    """Test whether we can run a sales report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['SALESPERSON'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testGetReportJob(self):
    """Test whether we can retrieve existing report job."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportJob(
        self.__class__.report_job_id), tuple))

  def testGetReportDownloadUrl(self):
    """Test whether we can retrieve report download URL."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportDownloadURL(
        self.__class__.report_job_id, 'CSV'), tuple))

  def testDownloadCsvReport(self):
    """Test whether we can download a CSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'CSV'), str))

  def testDownloadTsvReport(self):
    """Test whether we can download a TSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'TSV'), str))


class ReportServiceTestV201107(unittest.TestCase):

  """Unittest suite for ReportService using v201107."""

  SERVER = SERVER_V201107
  VERSION = VERSION_V201107
  client.debug = False
  service = None
  report_job_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testRunDeliveryReport(self):
    """Test whether we can run a delivery report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['ORDER'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'AD_SERVER_CTR', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    report_job = self.__class__.service.RunReportJob(report_job)
    self.__class__.report_job_id = report_job[0]['id']
    self.assert_(isinstance(report_job, tuple))

  def testRunInventoryReport(self):
    """Test whether we can run an inventory report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['DATE'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'ADSENSE_IMPRESSIONS', 'ADSENSE_CLICKS',
                        'TOTAL_IMPRESSIONS', 'TOTAL_REVENUE'],
            'dateRangeType': 'LAST_WEEK'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testRunSalesReport(self):
    """Test whether we can run a sales report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['SALESPERSON'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testGetReportJob(self):
    """Test whether we can retrieve existing report job."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportJob(
        self.__class__.report_job_id), tuple))

  def testGetReportDownloadUrl(self):
    """Test whether we can retrieve report download URL."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportDownloadURL(
        self.__class__.report_job_id, 'CSV'), tuple))

  def testDownloadCsvReport(self):
    """Test whether we can download a CSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'CSV'), str))

  def testDownloadTsvReport(self):
    """Test whether we can download a TSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'TSV'), str))


class ReportServiceTestV201108(unittest.TestCase):

  """Unittest suite for ReportService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  service = None
  report_job_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testRunDeliveryReport(self):
    """Test whether we can run a delivery report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['ORDER'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'AD_SERVER_CTR', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    report_job = self.__class__.service.RunReportJob(report_job)
    self.__class__.report_job_id = report_job[0]['id']
    self.assert_(isinstance(report_job, tuple))

  def testRunInventoryReport(self):
    """Test whether we can run an inventory report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['DATE'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                        'ADSENSE_IMPRESSIONS', 'ADSENSE_CLICKS',
                        'TOTAL_IMPRESSIONS', 'TOTAL_REVENUE'],
            'dateRangeType': 'LAST_WEEK'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testRunSalesReport(self):
    """Test whether we can run a sales report."""
    report_job = {
        'reportQuery': {
            'dimensions': ['SALESPERSON'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_REVENUE',
                        'AD_SERVER_AVERAGE_ECPM'],
            'dateRangeType': 'LAST_MONTH'
        }
    }
    self.assert_(isinstance(self.__class__.service.RunReportJob(
        report_job), tuple))

  def testGetReportJob(self):
    """Test whether we can retrieve existing report job."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportJob(
        self.__class__.report_job_id), tuple))

  def testGetReportDownloadUrl(self):
    """Test whether we can retrieve report download URL."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.GetReportDownloadURL(
        self.__class__.report_job_id, 'CSV'), tuple))

  def testDownloadCsvReport(self):
    """Test whether we can download a CSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'CSV'), str))

  def testDownloadTsvReport(self):
    """Test whether we can download a TSV report."""
    if self.__class__.report_job_id == '0':
      self.testRunDeliveryReport()
    self.assert_(isinstance(self.__class__.service.DownloadReport(
        self.__class__.report_job_id, 'TSV'), str))


def makeTestSuiteV201103():
  """Set up test suite using v201103.

  Returns:
    TestSuite test suite using v201103.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV201103))
  return suite


def makeTestSuiteV201104():
  """Set up test suite using v201104.

  Returns:
    TestSuite test suite using v201104.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV201104))
  return suite


def makeTestSuiteV201107():
  """Set up test suite using v201107.

  Returns:
    TestSuite test suite using v201107.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV201107))
  return suite


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV201108))
  return suite


if __name__ == '__main__':
  suite_v201103 = makeTestSuiteV201103()
  suite_v201104 = makeTestSuiteV201104()
  suite_v201107 = makeTestSuiteV201107()
  suite_v201108 = makeTestSuiteV201108()
  alltests = unittest.TestSuite([suite_v201103, suite_v201104, suite_v201107,
                                 suite_v201108])
  unittest.main(defaultTest='alltests')
