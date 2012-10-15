#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""Tests to cover ReportDownloader."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import StringIO
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest
import urllib2

import mock

from adspygoogle import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.AdWordsErrors import AdWordsReportError
from adspygoogle.adwords.util import XsdToWsdl


class ReportDownloaderTest(unittest.TestCase):
  """Tests for ReportDownloader."""

  def setUp(self):
    """Prepare unittest."""
    XsdToWsdl.CreateWsdlFromXsdUrl = mock.Mock()
    client = AdWordsClient(headers={'authToken': ' ',
                                    'userAgent': ' ',
                                    'developerToken': ' '})
    self.service = client.GetReportDownloader(
        'https://adwords-sandbox.google.com', 'v201209')

  def _ThrowErrorFromMakeRequest(self, payload_contents):
    """A test helper function to mock receiving an error during __MakeRequest.

    Args:
      payload_contents: str The payload to be returned with the HTTPError

    Raises:
      AdWordsError: The error returned from __MakeRequest
    """
    headers = mock.Mock()
    headers.headers = {'test': 'this'}
    payload = StringIO.StringIO()
    payload.write(payload_contents)
    payload.seek(0)
    adwords_report_response = urllib2.HTTPError(
        'url', '400', 'Bad Request', headers, payload)

    def RaiseMyError(*unused_args):
      raise adwords_report_response

    urllib2.urlopen = mock.Mock(side_effect=RaiseMyError)

    self.service._ReportDownloader__MakeRequest('url', payload='nothing')

  def testHandleLegacyError(self):
    self.service._op_config['version'] = 'v201206'
    error_message = ('AuthenticationError.CUSTOMER_NOT_FOUND @ ; '
                     'trigger:\'6495984802\' Service[ReportInfoService.get]')
    payload = '!!!2|||-1|||%s???' % error_message
    try:
      self._ThrowErrorFromMakeRequest(payload)
    except AdWordsError, e:
      self.assertTrue(error_message in str(e))

  def testHandleXmlError(self):
    self.service._op_config['version'] = 'v201209'
    payload = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<reportDownloadError><ApiError><type>'
               'QueryError.INVALID_FROM_CLAUSE</type><trigger>Joseph'
               '</trigger><fieldPath>one.two.three</fieldPath></ApiError>'
               '</reportDownloadError>')
    try:
      self._ThrowErrorFromMakeRequest(payload)
      self.fail('Exception should have been thrown.')
    except AdWordsReportError, error:
      self.assertEquals('400', error.http_code)
      self.assertEquals('QueryError.INVALID_FROM_CLAUSE', error.type)
      self.assertEquals('Joseph', error.trigger)
      self.assertEquals('one.two.three', error.field_path)

  def testHandleUnknownError(self):
    payload = ('This is not a recognized error. It should appear unaltered in '
               'the error raised.')
    try:
      self._ThrowErrorFromMakeRequest(payload)
    except AdWordsError, e:
      self.assertTrue(payload in str(e))

  def testCheckForXmlError_withError(self):
    xml_message = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<reportDownloadError><ApiError><type>'
                   'QueryError.INVALID_FROM_CLAUSE</type><trigger>Joseph'
                   '</trigger><fieldPath>one.two\n.three</fieldPath></ApiError>'
                   '</reportDownloadError>')
    try:
      self.service._ReportDownloader__CheckForXmlError('400', xml_message)
      self.fail('Exception should have been thrown.')
    except AdWordsReportError, error:
      self.assertEquals('400', error.http_code)
      self.assertEquals('QueryError.INVALID_FROM_CLAUSE', error.type)
      self.assertEquals('Joseph', error.trigger)
      self.assertEquals('one.two\n.three', error.field_path)

  def testCheckForXmlError_noError(self):
    self.service._ReportDownloader__CheckForXmlError(
        '400', 'This is not an error XML message')


if __name__ == '__main__':
  unittest.main()
