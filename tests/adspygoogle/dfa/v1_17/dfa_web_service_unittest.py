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

"""Unit tests to cover GenericDfaService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfa.DfaErrors import DfaApiError
from adspygoogle.dfa.GenericDfaService import GenericDfaService
from tests.adspygoogle.dfa.v1_17 import client
from tests.adspygoogle.dfa.v1_17 import HTTP_PROXY
from tests.adspygoogle.dfa.v1_17 import SERVER_V1_17
from tests.adspygoogle.dfa.v1_17 import VERSION_V1_17


class DfaWebServiceTestV1_17(unittest.TestCase):

  """Unittest suite for DfaWebService using v1_17."""

  SERVER = SERVER_V1_17
  VERSION = VERSION_V1_17
  client.debug = False
  res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    search_criteria = {'pageSize': '10'}
    self.assert_(isinstance(client.GetAdvertiserService(
        self.__class__.SERVER,
        self.__class__.VERSION, HTTP_PROXY).GetAdvertisers(search_criteria),
                            tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(
        os.path.join('..', 'data', 'request_getadvertisers.xml'))
    url = '/v1.16/api/dfa-api/advertiser'
    http_proxy = None

    self.assert_(isinstance(client.CallRawMethod(
        soap_message, url, self.__class__.SERVER, http_proxy), tuple))

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV1_17()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.res), self.__class__.MAX_THREADS)


class TestThreadV1_17(threading.Thread):

  """Creates TestThread using v1_17.

  Responsible for defining an action for a single thread.
  """

  def run(self):
    """Represent thread's activity."""
    search_criteria = {'pageSize': '10'}
    DfaWebServiceTestV1_17.res.append(client.GetAdvertiserService(
        DfaWebServiceTestV1_17.SERVER, DfaWebServiceTestV1_17.VERSION,
        HTTP_PROXY).GetAdvertisers(search_criteria))


if __name__ == '__main__':
  unittest.main()
