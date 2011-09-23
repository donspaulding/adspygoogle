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

"""This example displays advertiser group name, ID, and advertiser count for the
given search criteria. Results are limited to the first 10 records.


Tags: advertisergroup.getAdvertiserGroups
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
advertiser_group_service = client.GetAdvertiserGroupService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

search_string = 'INSERT_SEARCH_STRING_CRITERIA_HERE'

# Create advertiser group search criteria structure.
advertiser_group_search_criteria = {
    'searchString': search_string,
    'pageSize': '10'
}

# Get advertiser group record set.
results = advertiser_group_service.GetAdvertiserGroups(
             advertiser_group_search_criteria)[0]

# Display advertiser group names, IDs and advertiser count.
if results['records']:
  for advertiser_group in results['records']:
    print ('Advertiser group with name \'%s\', ID \'%s\', containing %s'
           ' advertisers was found.' % (advertiser_group['name'],
                                        advertiser_group['id'],
                                        advertiser_group['advertiserCount']))
else:
  print 'No advertiser groups found for your criteria.'
