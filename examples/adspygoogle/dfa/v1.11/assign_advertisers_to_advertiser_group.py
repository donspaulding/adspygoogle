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

"""This example assigns a list of advertisers to an advertiser group.

CAUTION: An advertiser that has campaigns associated with it cannot be
removed from an advertiser group once assigned.

Tags: advertisergroup.assignAdvertisersToAdvertiserGroup
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))
client.debug = False

# Initialize appropriate service.
advertiser_group_service = client.GetAdvertiserGroupService(
    'http://advertisersapitest.doubleclick.net', 'v1.11')

advertiser_ids = ['INSERT_FIRST_ADVERTISER_ID_HERE',
                  'INSERT_SECOND_ADVERTISER_ID_HERE']
advertiser_group_id = 'INSERT_ADVERTISER_GROUP_ID_HERE'

# Assign the advertisers to the advertiser group.
advertiser_group_service.AssignAdvertisersToAdvertiserGroup(advertiser_group_id,
                                                            advertiser_ids);
print 'Advertisers have been updated.'
