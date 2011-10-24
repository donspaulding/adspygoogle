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

"""This example illustrates how to find a client customer ID for a client email.
We recommend to use this script as a one off to convert your identifiers to IDs
and store them for future use.

Tags: InfoService.get
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import datetime
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))
client.use_mcc = True

# Initialize appropriate service.
info_service = client.GetInfoService(
    'https://adwords-sandbox.google.com', 'v201109')

today = datetime.datetime.today().strftime('%Y%m%d')

# Email address to find ID for.
client_email = 'INSERT_EMAIL_ADDRESS_HERE'

# Construct info selector object and retrieve usage info.
selector = {
  'clientEmails': [client_email],
  'apiUsageType': 'UNIT_COUNT_FOR_CLIENTS',
  'includeSubAccounts': 'true',
  'dateRange': {
      'min': today,
      'max': today
  }
}
info = info_service.Get(selector)[0]

# Display results.
for record in info['apiUsageRecords']:
  print ('Client with email \'%s\' has ID \'%s\'.' %
         (record['clientEmail'], record['clientCustomerId']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
