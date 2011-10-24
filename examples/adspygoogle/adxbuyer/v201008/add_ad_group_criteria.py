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

"""This example adds ad group criteria to an ad group. To get ad groups, run
get_all_ad_groups.py.

Tags: AdGroupCriterionService.mutate
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
ad_group_criterion_service = client.GetAdGroupCriterionService(
    'https://adwords-sandbox.google.com', 'v201008')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'

# Construct placement ad group criterion object.
placement = {
    'xsi_type': 'BiddableAdGroupCriterion',
    'adGroupId': ad_group_id,
    'criterion': {
        'xsi_type': 'Placement',
        'url': 'http://mars.google.com'
    }
}

# Construct operations and add ad group criteria.
operations = [
    {
        'operator': 'ADD',
        'operand': placement
    }
]
ad_group_criteria = ad_group_criterion_service.Mutate(operations)[0]['value']

# Display results.
for criterion in ad_group_criteria:
  if criterion['criterion']['Criterion_Type'] == 'Placement':
    print ('Placement ad group criterion with ad group id \'%s\', criterion '
           'id \'%s\', and url \'%s\' was added.'
           % (criterion['adGroupId'], criterion['criterion']['id'],
              criterion['criterion']['url']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
