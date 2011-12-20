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

"""This example retrieves available creative groups for a given advertiser and
displays the name, ID, advertiser ID, and group number. To get an advertiser
ID, run GetAdvertisers.java. Results are limited to the first 10.

Tags: creativegroup.getCreativeGroups
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
creative_group_service = client.GetCreativeGroupService(
    'http://advertisersapitest.doubleclick.net', 'v1.16')

advertiser_id = 'INSERT_ADVERTISER_ID_HERE'

# Set up creative group search criteria structure.
creative_group_search_criteria = {
    'advertiserIds': [advertiser_id],
}

# Get creatives groups for the selected criteria.
results = creative_group_service.GetCreativeGroups(
    creative_group_search_criteria)[0]

# Display creative group names, IDs, advertiser IDs, and group numbers.
if results['records']:
  for creative_field_value in results['records']:
    print ('Creative group with name \'%s\', ID \'%s\', advertiser ID \'%s\','
           ' and group number \'%s\' was found.'
           % (creative_field_value['name'], creative_field_value['id'],
              creative_field_value['advertiserId'],
              creative_field_value['groupNumber']))
else:
  print 'No creative groups found for your criteria.'