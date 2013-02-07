#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""Test to cover issue 51.

Ensures when using PyXML and pretty_print turned off, the library is able to
deserialize AdWords errors.
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import StringIO
import sys
import unittest
sys.path.insert(0, os.path.join('..', '..', '..'))

import mock
from oauth2client.client import OAuth2Credentials

from adspygoogle import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.AdWordsSoapBuffer import AdWordsSoapBuffer



# Location of a cached WSDL to generate a service proxy from.
WSDL_FILE_LOCATION = os.path.join('..', 'data', 'campaign_service.wsdl')

# Location of a cached buffer to parse.
BUFFER_FILE_LOCATION = os.path.join('..', 'data', 'issue51_buffer.txt')


class Issue51Test(unittest.TestCase):
  """Tests for Issue 51."""

  def testParseError(self):
    """Tests that the SOAP buffer parses AdWords errors correctly."""
    client = AdWordsClient(headers={
        'userAgent': 'USER_AGENT',
        'developerToken': 'DEVELOPER_TOKEN',
        'clientCustomerId': 'CLIENT_CUSTOMER_ID',
        'oauth2credentials': OAuth2Credentials(
            'ACCESS_TOKEN', 'client_id', 'client_secret', 'refresh_token', None,
            'uri', 'user_agent')
    })

    wsdl_data = open(WSDL_FILE_LOCATION).read()
    with mock.patch('urllib.urlopen') as mock_urlopen:
      mock_urlopen.return_value = StringIO.StringIO(wsdl_data)
      service = client.GetCampaignService()

    buf = AdWordsSoapBuffer('1', False)
    buf.write(open(BUFFER_FILE_LOCATION).read())

    try:
      service._HandleLogsAndErrors(buf, '', '', {'data': 'datum'})
    except AdWordsError, e:
      if 'Unable to parse incoming SOAP XML.' in str(e):
        self.fail('Failed to parse the error properly')


if __name__ == '__main__':
  unittest.main()
