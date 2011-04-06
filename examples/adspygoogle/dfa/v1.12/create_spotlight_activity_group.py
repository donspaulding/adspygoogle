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

"""This example creates a new activity group for a given spotlight
configuration. To get spotlight tag configuration, run get_advertisers.py.
To get activity types, run get_activity_types.py.

Tags: spotlight.saveSpotlightActivityGroup
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
spotlight_service = client.GetSpotlightService(
    'http://advertisersapitest.doubleclick.net', 'v1.12')

spotlight_configuration_id = 'INSERT_SPOTLIGHT_CONFIGURATION_ID_HERE'
activity_type = 'INSERT_ACTIVITY_TYPE_HERE'
group_name = 'INSERT_GROUP_NAME_HERE'

# Construct and save spotlight activity group.
spotlight_activity_group = {
    'name': group_name,
    'spotlightConfigurationId': spotlight_configuration_id,
    'groupType': activity_type
}
result = spotlight_service.SaveSpotlightActivityGroup(
    spotlight_activity_group)[0]

# Display results.
print 'Spotlight activity group with ID \'%s\' was created.' % result['id']

