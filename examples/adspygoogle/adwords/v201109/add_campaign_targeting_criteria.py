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

"""This example adds various types of targeting criteria to a given campaign. To
get campaigns, run get_all_campaigns.py.

Tags: CampaignCriterionService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
campaign_criterion_service = client.GetCampaignCriterionService(
    'https://adwords-sandbox.google.com', 'v201109')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Create locations. The IDs can be found in the documentation or retrieved with
# the LocationCriterionService.
california = {
    'xsi_type': 'Location',
    'id': '21137'
}
mexico = {
    'xsi_type': 'Location',
    'id': '2484'
}

# Create languages. The IDs can be found in the documentation or retrieved with
# the ConstantDataService.
english = {
    'xsi_type': 'Language',
    'id': '1000'
}
spanish = {
    'xsi_type': 'Language',
    'id': '1003'
}

# Create platforms. The IDs can be found in the documentation.
mobile = {
    'xsi_type': 'Platform',
    'id': '30001'
}
tablets = {
    'xsi_type': 'Platform',
    'id': '30002'
}

# Create operations
operations = []
for criterion in [california, mexico, english, spanish, mobile, tablets]:
  operations.append({
      'operator': 'ADD',
      'operand': {
          'campaignId': campaign_id,
          'criterion': criterion
      }
  })

# Make the mutate request.
result = campaign_criterion_service.mutate(operations)[0]

# Display the resulting campaign criteria.
for campaign_criterion in result['value']:
  print ('Campaign criterion with campaign id \'%s\', criterion id \'%s\', and'
  ' type \'%s\' was added.' % (campaign_criterion['campaignId'],
                               campaign_criterion['criterion']['id'],
                               campaign_criterion['criterion']['type']))
