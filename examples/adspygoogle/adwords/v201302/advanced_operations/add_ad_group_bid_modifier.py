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

"""Adds an ad group level mobile bid modifier override for a campaign.

To get your ad groups, run get_ad_groups.py.

Tags: AdGroupBidModifierService.mutate
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'
BID_MODIFIER = 'INSERT_BID_MODIFIER_HERE'


def main(client, ad_group_id, bid_modifier):
  # Initialize appropriate service.
  ad_group_bid_modifier_service = client.GetAdGroupBidModifierService(
      version='v201302')

  # Mobile criterion ID.
  criterion_id = '30001'

  # Prepare to add an ad group level override.
  operation = {
      # Use 'ADD' to add a new modifier and 'SET' to update an existing one. A
      # modifier can be removed with the 'REMOVE' operator.
      'operator': 'ADD',
      'operand': {
          'adGroupId': ad_group_id,
          'criterion': {
              'xsi_type': 'Platform',
              'id': criterion_id
          },
          'bidModifier': bid_modifier
      }
  }

  # Add ad group level mobile bid modifier.
  response = ad_group_bid_modifier_service.mutate([operation])[0]
  if response and response['value']:
    modifier = response['value'][0]
    value = modifier.get('bidModifier') or 'unset'
    print ('Campaign ID %s, AdGroup ID %s, Criterion ID %s was updated with '
           'ad group level modifier: %s' %
           (modifier['campaignId'], modifier['adGroupId'],
            modifier['criterion']['id'], value))
  else:
    print 'No modifiers were added.'


if __name__ == '__main__':
  # Initialize client object.
  client_ = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client_, AD_GROUP_ID, BID_MODIFIER)
