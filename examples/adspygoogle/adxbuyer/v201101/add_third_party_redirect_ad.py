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

"""This example adds a third party redirect ad to an ad group. To get ad group,
run get_all_ad_groups.py.

Tags: AdGroupAdService.mutate
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
ad_group_ad_service = client.GetAdGroupAdService(
    'https://adwords-sandbox.google.com', 'v201101')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'

# Construct operations and add ads.
operations = [
    {
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': ad_group_id,
            'ad': {
                'type': 'ThirdPartyRedirectAd',
                'name': 'Example third party ad #%s' % Utils.GetUniqueName(),
                'url': 'http://www.example.com',
                'dimensions': {
                    'width': '300',
                    'height': '250'
                },
                # This field normally contains the javascript ad tag.
                'snippet': '<img src="http://www.google.com/intl/en/adwords/select/images/samples/inline.jpg"/>',
                'impressionBeaconUrl': 'http://www.examples.com/beacon',
                'certifiedVendorFormatId': '119',
                'isCookieTargeted': 'false',
                'isUserInterestTargeted': 'false',
                'isTagged': 'false'
            }
        }
    }
]
ads = ad_group_ad_service.Mutate(operations)[0]

# Display results.
for ad in ads['value']:
  print ('Ad with id \'%s\' and of type \'%s\' was added.'
         % (ad['ad']['id'], ad['ad']['Ad_Type']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
