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

"""This example gets existing campaigns based on a given search criteria.
Results are limited to the first 10.

Tags: campaign.getCampaignsByCriteria
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
campaign_service = client.GetCampaignService(
    'https://advertisersapitest.doubleclick.net', 'v1.17')

search_string = 'INSERT_CAMPAIGN_SEARCH_STRING_HERE'

# Create campaign search criteria structure.
campaign_search_criteria = {
    'searchString': search_string,
    'pageSize': '10'
}

# Get campaign record set.
results = campaign_service.GetCampaignsByCriteria(campaign_search_criteria)[0]

# Display campaign names and IDs.
if results['records']:
  for campaign in results['records']:
    print ('Campaign with name \'%s\' and ID \'%s\' was found.'
           % (campaign['name'], campaign['id']))
else:
  print 'No campaigns found for your criteria.'
