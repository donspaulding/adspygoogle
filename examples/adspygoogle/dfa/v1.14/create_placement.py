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

"""This example creates a placement in a given campaign. Requires the DFA site
ID and campaign ID in which the placement will be created into. To create a
campaign, run create_campaign.py. To get DFA site ID, run get_dfa_site.py.
To get a size ID, run get_size.py. To get placement types, run
get_placement_types.py. To get pricing types, run get_pricing_types.py.

Tags: placement.savePlacement
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
placement_service = client.GetPlacementService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

placement_name = 'INSERT_PLACEMENT_NAME_HERE'
dfaSite_id = 'INSERT_DFA_SITE_ID_HERE'
campaign_id = 'INSERT_CAMPAIGN_ID_HERE'
pricing_type = 'INSERT_PRICING_TYPE_HERE'
placement_type = 'INSERT_PLACEMENT_TYPE_HERE'
size_id = 'INSERT_SIZE_ID_HERE'
start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
    'year': 'INSERT_START_YEAR_HERE',
    'month': int('INSERT_START_MONTH_HERE'),
    'day': int('INSERT_START_DAY_HERE')}
end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
    'year': 'INSERT_END_YEAR_HERE',
    'month': int('INSERT_END_MONTH_HERE'),
    'day': int('INSERT_END_DAY_HERE')}

# Construct and save placement.
placement = {
    'name': placement_name,
    'campaignId': campaign_id,
    'dfaSiteId': dfaSite_id,
    'sizeId': size_id,
    'placementType': placement_type,
    'pricingSchedule': {
        'startDate': start_date,
        'endDate': end_date,
        'pricingType': pricing_type
    }
}

# Set placement tag settings.
tag_options = placement_service.GetRegularPlacementTagOptions()
tag_types = []
for tag_listing in tag_options:
  tag_types.append(tag_listing['id'])

placement['tagSettings'] =  { 'tagTypes': tag_types }

result = placement_service.SavePlacement(placement)[0]

# Display results.
print 'Placement with ID \'%s\' was created.' % result['id']
