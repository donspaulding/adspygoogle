#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Unit tests to cover GenericAdWordsService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.adwords.AdWordsErrors import AdWordsApiError
from adspygoogle.adwords.GenericAdWordsService import GenericAdWordsService
from adspygoogle.adwords.GenericV13AdWordsService import GenericV13AdWordsService
from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V13
from tests.adspygoogle.adwords import SERVER_V200909
from tests.adspygoogle.adwords import SERVER_V201003
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import SERVER_V201109
from tests.adspygoogle.adwords import TEST_VERSION_V13
from tests.adspygoogle.adwords import TEST_VERSION_V200909
from tests.adspygoogle.adwords import TEST_VERSION_V201003
from tests.adspygoogle.adwords import TEST_VERSION_V201008
from tests.adspygoogle.adwords import TEST_VERSION_V201101
from tests.adspygoogle.adwords import TEST_VERSION_V201109
from tests.adspygoogle.adwords import VERSION_V13
from tests.adspygoogle.adwords import VERSION_V200909
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import VERSION_V201109
from tests.adspygoogle.adwords import client


class GenericAdWordsServiceTestV13(unittest.TestCase):

  """Unittest suite for GenericAdWordsService using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    self.assert_(isinstance(client.GetAccountService(
        self.__class__.SERVER, self.__class__.VERSION,
        HTTP_PROXY).GetAccountInfo(), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getaccountinfo.xml'))
    url = '/api/adwords/v13/AccountService'
    http_proxy = HTTP_PROXY

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV13()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV13(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v13.
  """

  def run(self):
    """Represent thread's activity."""
    GenericAdWordsServiceTestV13.responses.append(
        client.GetAccountService(GenericAdWordsServiceTestV13.SERVER,
            GenericAdWordsServiceTestV13.VERSION, HTTP_PROXY).GetAccountInfo())


class GenericAdWordsServiceTestV200909(unittest.TestCase):

  """Unittest suite for GenericAdWordsService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v200909/CampaignService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV200909()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV200909(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v200909.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {'ids': []}
    GenericAdWordsServiceTestV200909.responses.append(
        client.GetCampaignService(GenericAdWordsServiceTestV200909.SERVER,
            GenericAdWordsServiceTestV200909.VERSION, HTTP_PROXY).Get(selector))


class GenericAdWordsServiceTestV201003(unittest.TestCase):

  """Unittest suite for GenericAdWordsService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201003/CampaignService'
    http_proxy = HTTP_PROXY

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201003()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV201003(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v201003.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {'ids': []}
    GenericAdWordsServiceTestV201003.responses.append(
        client.GetCampaignService(GenericAdWordsServiceTestV201003.SERVER,
            GenericAdWordsServiceTestV201003.VERSION, HTTP_PROXY).Get(selector))


class GenericAdWordsServiceTestV201008(unittest.TestCase):

  """Unittest suite for GenericAdWordsService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = True
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201008/CampaignService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201008()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class GenericAdWordsServiceTestV201101(unittest.TestCase):

  """Unittest suite for GenericAdWordsService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201101/CampaignService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201101()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class AdWordsWebServiceTestV201109(unittest.TestCase):

  """Unittest suite for AdWordsWebService using v201109."""

  SERVER = SERVER_V201109
  VERSION = VERSION_V201109
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201109/CampaignService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201109()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV201008(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v201008.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {'ids': []}
    GenericAdWordsServiceTestV201008.responses.append(
        client.GetCampaignService(GenericAdWordsServiceTestV201008.SERVER,
            GenericAdWordsServiceTestV201008.VERSION, HTTP_PROXY).Get(selector))


class TestThreadV201101(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v201101.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {
        'fields': ['Id', 'Name', 'Status']
    }
    GenericAdWordsServiceTestV201101.responses.append(
        client.GetCampaignService(GenericAdWordsServiceTestV201101.SERVER,
            GenericAdWordsServiceTestV201101.VERSION, HTTP_PROXY).Get(selector))


class TestThreadV201109(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v201109.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {
        'fields': ['Id', 'Name', 'Status']
    }
    AdWordsWebServiceTestV201109.responses.append(
        client.GetCampaignService(AdWordsWebServiceTestV201109.SERVER,
            AdWordsWebServiceTestV201109.VERSION, HTTP_PROXY).Get(selector))


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GenericAdWordsServiceTestV13))
  return suite


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GenericAdWordsServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GenericAdWordsServiceTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GenericAdWordsServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GenericAdWordsServiceTestV201101))
  return suite


def makeTestSuiteV201109():
  """Set up test suite using v201109.

  Returns:
    TestSuite test suite using v201109.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsWebServiceTestV201109))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V13:
    suites.append(makeTestSuiteV13())
  if TEST_VERSION_V200909:
    suites.append(makeTestSuiteV200909())
  if TEST_VERSION_V201003:
    suites.append(makeTestSuiteV201003())
  if TEST_VERSION_V201008:
    suites.append(makeTestSuiteV201008())
  if TEST_VERSION_V201101:
    suites.append(makeTestSuiteV201101())
  if TEST_VERSION_V201109:
    suites.append(makeTestSuiteV201109())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')

