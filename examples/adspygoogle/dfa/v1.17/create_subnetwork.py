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

"""This example creates a subnetwork in a given DFA network. To get the network
ID, run authenticate.py. To get the available permissions, run
get_available_permissions.py.

Tags: subnetwork.saveSubnetwork
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
subnetwork_service = client.GetSubnetworkService(
    'https://advertisersapitest.doubleclick.net', 'v1.17')

network_id = 'INSERT_NETWORK_ID_HERE'
subnetwork_name = 'INSERT_SUBNETWORK_NAME_HERE'
permission1 = 'INSERT_FIRST_PERMISSION_ID_HERE'
permission2 = 'INSERT_SECOND_PERMISSION_ID_HERE'

# Construct and the basic subnetwork structure.
subnetwork = {
    'name': subnetwork_name,
    'networkId': network_id
}

# Create an array of all permissions assigned to this subnetwork and add it to
# the subnetwork structure. To get a list of available permissions, run
# get_available_permissions.py.
subnetwork['availablePermissions'] = [permission1, permission2]

# Save the subnetwork.
result = subnetwork_service.SaveSubnetwork(subnetwork)[0]

# Display results.
print 'Subnetwork with ID \'%s\' was created.' % result['id']
