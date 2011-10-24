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

"""Unit tests to cover DfpWebService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfp.DfpErrors import DfpApiError
from adspygoogle.dfp.GenericDfpService import GenericDfpService
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


class DfpWebServiceTestV201103(unittest.TestCase):

  """Unittest suite for DfpWebService using v201103."""

  SERVER = SERVER_V201103
  VERSION = VERSION_V201103
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201103/UserService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201103()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201103(threading.Thread):

  """Creates TestThread using v201103.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201103.res.append(client.GetUserService(
        DfpWebServiceTestV201103.SERVER, DfpWebServiceTestV201103.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


class DfpWebServiceTestV201104(unittest.TestCase):

  """Unittest suite for DfpWebService using v201104."""

  SERVER = SERVER_V201104
  VERSION = VERSION_V201104
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201104/UserService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201104()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201104(threading.Thread):

  """Creates TestThread using v201104.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201104.res.append(client.GetUserService(
        DfpWebServiceTestV201104.SERVER, DfpWebServiceTestV201104.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


class DfpWebServiceTestV201107(unittest.TestCase):

  """Unittest suite for DfpWebService using v201107."""

  SERVER = SERVER_V201107
  VERSION = VERSION_V201107
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201107/UserService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201107()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201107(threading.Thread):

  """Creates TestThread using v201107.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201107.res.append(client.GetUserService(
        DfpWebServiceTestV201107.SERVER, DfpWebServiceTestV201107.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


class DfpWebServiceTestV201108(unittest.TestCase):

  """Unittest suite for DfpWebService using v201108."""

  SERVER = SERVER_V201108
  VERSION = VERSION_V201108
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    filter_statement = {'query': 'ORDER BY name LIMIT 500'}
    self.assert_(isinstance(client.GetUserService(self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetUsersByStatement(
            filter_statement), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('data', 'request_getusersbystatement.xml'))
    url = '/apis/ads/publisher/v201108/UserService'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(soap_message, url,
                            self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201108()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV201108(threading.Thread):

  """Creates TestThread using v201108.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    statement = {'query': 'ORDER BY name LIMIT 500'}
    DfpWebServiceTestV201108.res.append(client.GetUserService(
        DfpWebServiceTestV201108.SERVER, DfpWebServiceTestV201108.VERSION,
        HTTP_PROXY).GetUsersByStatement(statement))


def makeTestSuiteV201103():
  """Set up test suite using v201103.

  Returns:
    TestSuite test suite using v201103.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201103))
  return suite


def makeTestSuiteV201104():
  """Set up test suite using v201104.

  Returns:
    TestSuite test suite using v201104.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201104))
  return suite


def makeTestSuiteV201107():
  """Set up test suite using v201107.

  Returns:
    TestSuite test suite using v201107.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201107))
  return suite


def makeTestSuiteV201108():
  """Set up test suite using v201108.

  Returns:
    TestSuite test suite using v201108.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfpWebServiceTestV201108))
  return suite


if __name__ == '__main__':
  suite_v201103 = makeTestSuiteV201103()
  suite_v201104 = makeTestSuiteV201104()
  suite_v201107 = makeTestSuiteV201107()
  suite_v201108 = makeTestSuiteV201108()
  alltests = unittest.TestSuite([suite_v201103, suite_v201104, suite_v201107,
                                 suite_v201108])
  unittest.main(defaultTest='alltests')
