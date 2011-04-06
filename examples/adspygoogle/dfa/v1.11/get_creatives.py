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

"""This example retrieves available creatives for a given advertiser and
displays the name and ID. To create an advertiser, run CreateAdvertiser.java.
Results are limited to the first 10.

Tags: creative.getCreatives
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
creative_service = client.GetCreativeService(
    'http://advertisersapitest.doubleclick.net', 'v1.11')

advertiser_id = 'INSERT_ADVERTISER_ID_HERE'

# Set up creative search criteria structure.
creative_search_criteria = {
    'advertiserId': advertiser_id,
    'pageSize': '10'
}

# Get creatives for the selected criteria.
results = creative_service.GetCreatives(creative_search_criteria)[0]

# Display creative name and its ID.
if results['records']:
  for creative in results['records']:
    print ('Creative with name \'%s\' and ID \'%s\' was found.'
           % (creative['name'], creative['id']))
else:
  print 'No creatives found for your criteria.'

