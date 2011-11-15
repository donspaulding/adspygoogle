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

"""This example shows how to use validateOnly SOAP header.

Tags: CampaignService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsRequestError
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service with validate only flag enabled.
client.validate_only = True
campaign_service = client.GetCampaignService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct operations for adding campaign object and attempt to add campaign.
operations = [{
    'operator': 'ADD',
    'operand': {
        'name': 'Campaign #%s' % Utils.GetUniqueName(),
        'status': 'PAUSED',
        'biddingStrategy': {
            'xsi_type': 'ManualCPM'
        },
        'budget': {
            'period': 'DAILY',
            'amount': {
                'microAmount': '50000000'
            },
            'deliveryMethod': 'STANDARD'
        }
    }
}]
campaigns = campaign_service.Mutate(operations)
if len(campaigns) > 0:
  campaigns = campaigns[0]

# Display results.
if campaigns:
  for campaign in campaigns['value']:
    print ('Campaign with name \'%s\' and id \'%s\' was added.'
           % (campaign['name'], campaign['id']))
else:
  print 'No campaigns were added.'

# Construct operations for adding campaign object without a bidding strategy.
operations = [{
    'operator': 'ADD',
    'operand': {
        'name': 'Campaign #%s' % Utils.GetUniqueName(),
        'status': 'PAUSED',
        'budget': {
            'period': 'DAILY',
            'amount': {
                'microAmount': '50000000'
            },
            'deliveryMethod': 'STANDARD'
        }
    }
}]
try:
  campaigns = campaign_service.Mutate(operations)[0]
except AdWordsRequestError, e:
  print 'Validation for adding campaign failed with \'%s\'.' % str(e)

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))