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

"""Unit tests to cover Utils."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfa.DfaSoapBuffer import DfaSoapBuffer
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_12
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import SERVER_V1_14
from tests.adspygoogle.dfa import TEST_VERSION_V1_12
from tests.adspygoogle.dfa import TEST_VERSION_V1_13
from tests.adspygoogle.dfa import TEST_VERSION_V1_14
from tests.adspygoogle.dfa import VERSION_V1_12
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import VERSION_V1_14


class DfaUtilsTestV1_14(unittest.TestCase):

  """Unittest suite for DfaUtils using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    buf = DfaSoapBuffer()

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    buf.write(html_code)

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)


class DfaUtilsTestV1_13(unittest.TestCase):

  """Unittest suite for DfaUtils using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    buf = DfaSoapBuffer()

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    buf.write(html_code)

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)


class DfaUtilsTestV1_12(unittest.TestCase):

  """Unittest suite for DfaUtils using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  client.debug = False
  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    buf = DfaSoapBuffer()

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    buf.write(html_code)

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaUtilsTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaUtilsTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaUtilsTestV1_12))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_14:
    suites.append(makeTestSuiteV1_14())
  if TEST_VERSION_V1_13:
    suites.append(makeTestSuiteV1_13())
  if TEST_VERSION_V1_12:
    suites.append(makeTestSuiteV1_12())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')