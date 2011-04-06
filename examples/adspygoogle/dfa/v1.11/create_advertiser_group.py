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

"""This example creates an advertiser group.

Tags: advertisergroup.saveAdvertiserGroup
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
advertiser_group_service = client.GetAdvertiserGroupService(
    'http://advertisersapitest.doubleclick.net', 'v1.11')

advertiser_group_name = 'INSERT_ADVERTISER_GROUP_NAME_HERE'

# Construct and save advertiser.
advertiser_group = {
    'name': advertiser_group_name
}
result = advertiser_group_service.SaveAdvertiserGroup(advertiser_group)[0]

# Display results.
print 'Advertiser group with ID \'%s\' was created.' % result['id']
