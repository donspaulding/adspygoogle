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

"""This example retrieves the cost, in API units per operator, of the given
method on a specific date.

Tags: InfoService.get
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

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
    'https://adwords-sandbox.google.com', 'v200909')

# Construct info selector object and retrieve usage info.
today = datetime.datetime.today()
service_name = 'AdGroupService'
method_name = 'mutate'
operator = 'SET'
selector = {
    'dateRange': {
        'min': today.strftime('%Y%m01'),
        'max': today.strftime('%Y%m01')
    },
    'serviceName': service_name,
    'methodName': method_name,
    'operator': operator,
    'apiUsageType': 'METHOD_COST'
}
info = info_service.Get(selector)[0]

# Display results.
print ('The cost of the %s.%s.%s during %s-%s is \'%s\'.'
       % (selector['serviceName'], selector['methodName'], selector['operator'],
          selector['dateRange']['min'], selector['dateRange']['max'],
          info['cost']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
