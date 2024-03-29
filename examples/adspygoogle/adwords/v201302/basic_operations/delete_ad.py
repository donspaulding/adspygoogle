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

"""This example deletes an ad using the 'REMOVE' operator. To get ads,
run get_text_ads.py.

Tags: AdGroupAdService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
ad_id = 'INSERT_AD_ID_HERE'


def main(client, ad_group_id, ad_id):
  # Initialize appropriate service.
  ad_group_ad_service = client.GetAdGroupAdService(version='v201302')

  # Construct operations and delete ad.
  operations = [{
      'operator': 'REMOVE',
      'operand': {
          'xsi_type': 'AdGroupAd',
          'adGroupId': ad_group_id,
          'ad': {
              'id': ad_id
          }
      }
  }]
  result = ad_group_ad_service.Mutate(operations)[0]

  # Display results.
  for ad in result['value']:
    print ('Ad with id \'%s\' and type \'%s\' was deleted.'
           % (ad['ad']['id'], ad['ad']['Ad_Type']))

  print
  print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, ad_group_id, ad_id)
