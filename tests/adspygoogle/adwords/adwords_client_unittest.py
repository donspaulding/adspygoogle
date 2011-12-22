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

"""Unit tests to cover AdWordsClient."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError


DEFAULT_HEADERS = {
    'userAgent': 'Foo Bar',
    'developerToken': 'devtoken'
}


class AdWordsClientValidationTest(unittest.TestCase):

  """Tests the validation logic when instantiating AdWordsClient."""

  def setUp(self):
    """Monkey patch AuthToken retrieval."""

    def FakeGetAuthToken(a, b, c, d, e):
      return 'FooBar'
    Utils.GetAuthToken = FakeGetAuthToken

  def testEmailPassOnly(self):
    """Tests that specifying solely email & password works."""
    headers = DEFAULT_HEADERS.copy()
    headers['email'] = 'email@example.com'
    headers['password'] = 'password'
    client = AdWordsClient(headers=headers)
    self.assertEquals(client._headers['authToken'], 'FooBar')

  def testEmailPassOthersBlank(self):
    """Tests that email and password with other auth blank works."""
    headers = DEFAULT_HEADERS.copy()
    headers['email'] = 'email@example.com'
    headers['password'] = 'password'
    headers['authToken'] = ''
    headers['oauth_credentials'] = None
    client = AdWordsClient(headers=headers)
    self.assertEquals(client._headers['authToken'], 'FooBar')

  def testAuthTokenOnly(self):
    """Tests that specifying solely authtoken works."""
    headers = DEFAULT_HEADERS.copy()
    headers['authToken'] = 'MyToken'
    client = AdWordsClient(headers=headers)
    self.assertEquals(client._headers['authToken'], 'MyToken')

  def testAuthTokenOthersBlank(self):
    """Tests that authToken with other auth blank works."""
    headers = DEFAULT_HEADERS.copy()
    headers['authToken'] = 'MyToken'
    headers['email'] = ''
    headers['password'] = ''
    headers['oauth_credentials'] = None
    client = AdWordsClient(headers=headers)
    self.assertEquals(client._headers['authToken'], 'MyToken')

  def testOAuthCredentialsOnly(self):
    """Tests that specifying solely oauth_credentials works."""
    headers = DEFAULT_HEADERS.copy()
    headers['oauth_credentials'] = {
        'oauth_consumer_key': 'anonymous',
        'oauth_consumer_secret': 'anonymous'
    }
    client = AdWordsClient(headers=headers)
    self.assertTrue(client.oauth_credentials)

  def testOAuthCredentialsOthersBlank(self):
    """Tests that oauth_credentials with other auth blank works."""
    headers = DEFAULT_HEADERS.copy()
    headers['oauth_credentials'] = {
        'oauth_consumer_key': 'anonymous',
        'oauth_consumer_secret': 'anonymous'
    }
    headers['email'] = ''
    headers['password'] = ''
    headers['authToken'] = ''
    client = AdWordsClient(headers=headers)
    self.assertTrue(client.oauth_credentials)

  def testNonStrictThrowsValidationError(self):
    """Tests that even when using non-strict mode, we still raise a
    ValidationError when no auth credentials are provided."""
    headers = DEFAULT_HEADERS.copy()
    config = {'strict': 'n'}

    def Run():
      _ = AdWordsClient(headers=headers, config=config)
    self.assertRaises(ValidationError, Run)


def MakeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsClientValidationTest))
  return suite


if __name__ == '__main__':
  suites = [MakeTestSuite()]
  alltests = unittest.TestSuite(suites)
  unittest.main(defaultTest='alltests')
