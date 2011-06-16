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

"""This example creates a creative field associated with a given advertiser. To
get an advertiser ID, run get_advertisers.py.

Tags: creativefield.saveCreativeField
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
creative_field_service = client.GetCreativeFieldService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

advertiser_id = 'INSERT_ADVERTISER_ID_HERE'
creative_field_name = 'INSERT_CREATIVE_FIELD_NAME_HERE'

# Construct and save creative field.
creative_field = {
    'name': creative_field_name,
    'advertiserId': advertiser_id,
    'id': '-1'
}
result = creative_field_service.SaveCreativeField(creative_field)[0]

# Display results.
print 'Creative field with ID \'%s\' was created.' % result['id']
