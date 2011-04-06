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

"""This example creates a campaign in a given advertiser. To create an
advertiser, run create_advertiser.py.

Tags: campaign.saveCampaign
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
campaign_service = client.GetCampaignService(
    'http://advertisersapitest.doubleclick.net', 'v1.13')

advertiser_id = 'INSERT_ADVERTISER_ID_HERE'
campaign_name = 'INSERT_CAMPAIGN_NAME_HERE'
url = 'INSERT_LANDING_PAGE_URL_HERE'
landing_page_name = 'INSERT_LANDING_PAGE_NAME_HERE'
start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
    'year': 'INSERT_START_YEAR_HERE',
    'month': int('INSERT_START_MONTH_HERE'),
    'day': int('INSERT_START_DAY_HERE')}
end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
    'year': 'INSERT_END_YEAR_HERE',
    'month': int('INSERT_END_MONTH_HERE'),
    'day': int('INSERT_END_DAY_HERE')}

# Create a default landing page for the campaign and save it.
default_landing_page = {
    'url': url,
    'name': landing_page_name
}

default_landing_page_id = campaign_service.SaveLandingPage(
    default_landing_page)[0]['id']

# Construct and save the campaign.
campaign = {
    'name': campaign_name,
    'advertiserId': advertiser_id,
    'defaultLandingPageId': default_landing_page_id,
    'archived': 'false',
    'startDate': start_date,
    'endDate': end_date
}
result = campaign_service.SaveCampaign(campaign)[0]

# Display results.
print 'Campaign with ID \'%s\' was created.' % result['id']
