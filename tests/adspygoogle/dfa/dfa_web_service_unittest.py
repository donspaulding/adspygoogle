#!/usr/bin/python
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

"""Unit tests to cover DfaWebService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from adspygoogle.dfa.DfaErrors import DfaApiError
from adspygoogle.dfa.DfaWebService import DfaWebService
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_11
from tests.adspygoogle.dfa import SERVER_V1_12
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import VERSION_V1_11
from tests.adspygoogle.dfa import VERSION_V1_12
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import client


class DfaWebServiceTestV1_13(unittest.TestCase):

  """Unittest suite for DfaWebService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    search_criteria = {'pageSize': '10'}
    self.assert_(isinstance(client.GetAdvertiserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetAdvertisers(
            search_criteria), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = '/'.join([DfaWebServiceTestV1_12.SERVER,
                    'v1.12/api/dfa-api', 'placement'])
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = DfaWebService(headers, config, op_config, url, lock)
    method_name = 'getPlacementTypes'
    if config['soap_lib'] == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, (),
                                                 'placement'), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getadvertisers.xml'))
    url = '/v1.12/api/dfa-api/advertiser'
    http_proxy = None

    self.failUnlessRaises(DfaApiError, client.CallRawMethod, soap_message, url,
                          self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV1_12()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV1_13(threading.Thread):

  """Creates TestThread using v1_13.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    search_criteria = {'pageSize': '10'}
    DfaWebServiceTestV1_13.res.append(client.GetAdvertiserService(
        DfaWebServiceTestV1_13.SERVER, DfaWebServiceTestV1_13.VERSION,
        HTTP_PROXY).GetAdvertisers(search_criteria))


class DfaWebServiceTestV1_12(unittest.TestCase):

  """Unittest suite for DfaWebService using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    search_criteria = {'pageSize': '10'}
    self.assert_(isinstance(client.GetAdvertiserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetAdvertisers(
            search_criteria), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = '/'.join([DfaWebServiceTestV1_12.SERVER,
                    'v1.12/api/dfa-api', 'placement'])
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = DfaWebService(headers, config, op_config, url, lock)
    method_name = 'getPlacementTypes'
    if config['soap_lib'] == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, (),
                                                 'placement'), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getadvertisers.xml'))
    url = '/v1.12/api/dfa-api/advertiser'
    http_proxy = None

    self.failUnlessRaises(DfaApiError, client.CallRawMethod, soap_message, url,
                          self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV1_12()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV1_12(threading.Thread):

  """Creates TestThread using v1_12.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    search_criteria = {'pageSize': '10'}
    DfaWebServiceTestV1_12.res.append(client.GetAdvertiserService(
        DfaWebServiceTestV1_12.SERVER, DfaWebServiceTestV1_12.VERSION,
        HTTP_PROXY).GetAdvertisers(search_criteria))


class DfaWebServiceTestV1_11(unittest.TestCase):

  """Unittest suite for DfaWebService using v1_11."""

  SERVER = SERVER_V1_11
  VERSION = VERSION_V1_11
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    search_criteria = {'pageSize': '10'}
    self.assert_(isinstance(client.GetAdvertiserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetAdvertisers(
            search_criteria), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = '/'.join([DfaWebServiceTestV1_12.SERVER,
                   'v1.11/api/dfa-api', 'placement'])
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = DfaWebService(headers, config, op_config, url, lock)
    method_name = 'getPlacementTypes'
    if config['soap_lib'] == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, (),
                                                 'placement'), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getadvertisers.xml'))
    url = '/v1.11/api/dfa-api/advertiser'
    http_proxy = None

    self.failUnlessRaises(DfaApiError, client.CallRawMethod, soap_message, url,
                          self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV1_11()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV1_11(threading.Thread):

  """Creates TestThread using v1_11.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    search_criteria = {'pageSize': '10'}
    DfaWebServiceTestV1_11.res.append(client.GetAdvertiserService(
        DfaWebServiceTestV1_11.SERVER, DfaWebServiceTestV1_11.VERSION,
        HTTP_PROXY).GetAdvertisers(search_criteria))


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaWebServiceTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaWebServiceTestV1_12))
  return suite


def makeTestSuiteV1_11():
  """Set up test suite using v1_11.

  Returns:
    TestSuite test suite using v1_11.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaWebServiceTestV1_11))
  return suite


if __name__ == '__main__':
  suite_v1_13 = makeTestSuiteV1_13()
  suite_v1_12 = makeTestSuiteV1_12()
  suite_v1_11 = makeTestSuiteV1_11()
  alltests = unittest.TestSuite([suite_v1_13, suite_v1_12, suite_v1_11])
  unittest.main(defaultTest='alltests')
