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

"""Unit tests to cover Logger."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import logging
import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
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


class DfaLoggerTestV1_14(unittest.TestCase):

  """Unittest suite for Logger using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    advertiser_service = client.GetAdvertiserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    advertiser_service.GetAdvertisers({})
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


class DfaLoggerTestV1_13(unittest.TestCase):

  """Unittest suite for Logger using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    advertiser_service = client.GetAdvertiserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    advertiser_service.GetAdvertisers({})
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


class DfaLoggerTestV1_12(unittest.TestCase):

  """Unittest suite for Logger using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  TMP_LOG = os.path.join('..', '..', '..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made.
    """
    logger = logging.getLogger(self.__class__.__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    advertiser_service = client.GetAdvertiserService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    advertiser_service.GetAdvertisers({})
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaLoggerTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaLoggerTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(DfaLoggerTestV1_12))
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
