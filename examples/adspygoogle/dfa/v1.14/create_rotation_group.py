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

"""This example creates a rotation group ad in a given campaign. To get ad types
run get_ad_types.py. Start and end date for the ad must be within campaign
start and end dates. To create creatives, run create_[type]_creative.py. To get
available placements, run get_placements.py. To get a size ID, run
get_size.py example.

Tags: ad.saveAd
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
ad_service = client.GetAdService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'
size_id = 'INSERT_SIZE_ID_HERE'
creative_id = 'INSERT_CREATIVE_ID_HERE'
placement_id = 'INSERT_PLACEMENT_ID_HERE'
ad_name = 'INSERT_AD_NAME_HERE'
start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
    'year': 'INSERT_START_YEAR_HERE',
    'month': int('INSERT_START_MONTH_HERE'),
    'day': int('INSERT_START_DAY_HERE')}
end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
    'year': 'INSERT_END_YEAR_HERE',
    'month': int('INSERT_END_MONTH_HERE'),
    'day': int('INSERT_END_DAY_HERE')}


# Construct basic rotation group structure.
rotation_group = {
    'xsi_type': 'RotationGroup',
    'name': ad_name,
    'active': 'true',
    'archived': 'false',
    'campaignId': campaign_id,
    'sizeId': size_id,
    'typeId': '1',
    'priority': '12',
    'ratio': '1',
    'rotationType': '1',
    'startTime': start_date,
    'endTime': end_date,
}

# Construct creative assignments and add them to the rotation group.
creative_assignment = {
    'active': 'true',
    'creativeId': creative_id,
    'clickThroughUrl': {
        'defaultLandingPageUsed': 'true',
        'landingPageId': '0'
    }
}
rotation_group['creativeAssignments'] = [creative_assignment]

# Construct placement assignments and add them to the rotation group.
placement_assignment = {
    'active': 'true',
    'placementId': placement_id
}
rotation_group['placementAssignments'] = [placement_assignment]

# Save the rotation group.
result = ad_service.SaveAd(rotation_group)[0]

# Display results.
print 'Ad with ID \'%s\' was created.' % result['id']
