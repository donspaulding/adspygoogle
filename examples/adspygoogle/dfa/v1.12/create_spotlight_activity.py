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

"""This example creates a spotlight activity in a given activity group. To
create an activity group, run create_spotlight_activity_group.py. To get tag
methods types, run get_tag_methods.py. To get activity type IDs, run
get_activity_types.py.

Tags: spotlight.saveSpotlightActivity
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

activity_group_id = 'INSERT_ACTIVITY_GROUP_ID_HERE'
activity_type_id = 'INSERT_ACTIVITY_TYPE_ID_HERE'
tag_method_type_id = 'INSERT_TAG_METHOD_TYPE_ID_HERE'
url = 'INSERT_EXPECTED_URL_HERE'
activity_name = 'INSERT_ACTIVITY_NAME_HERE'

# Construct and save spotlight activity.
spotlight_activity = {
    'name': activity_name,
    'activityGroupId': activity_group_id,
    'activityTypeId': activity_type_id,
    'tagMethodTypeId': tag_method_type_id,
    'expectedUrl': url
}
result = spotlight_service.SaveSpotlightActivity(spotlight_activity)[0]

# Display results.
print 'Spotlight activity with ID \'%s\' was created.' % result['id']
