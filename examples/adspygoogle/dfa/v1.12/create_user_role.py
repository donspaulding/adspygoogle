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

"""This example creates a user role in a given DFA subnetwork. To get the
subnetwork ID, run get_subnetworks.py. To get the available permissions, run
get_available_permissions.py. To get the parent user role ID, run
get_user_roles.py.

Tags: userrole.saveUserRole
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
user_role_service = client.GetUserRoleService(
    'http://advertisersapitest.doubleclick.net', 'v1.12')

user_role_name = 'INSERT_USER_ROLE_NAME_HERE'
subnetwork_id = 'INSERT_SUBNETWORK_ID_HERE'
parent_user_role_id = 'INSERT_PARENT_USER_ROLE_ID_HERE'
permission1_id = 'INSERT_FIRST_PERMISSION_ID_HERE'
permission2_id = 'INSERT_SECOND_PERMISSION_ID_HERE'

# Construct and the basic user role structure.
user_role = {
    'name': user_role_name,
    'subnetworkId': subnetwork_id,
    'parentUserRoleId': parent_user_role_id
}

# Create an array of all permissions assigned to this user role and add it to
# the user role structure. To get a list of available permissions, run
# get_available_permissions.py.
permission1 = {
    'id': permission1_id
}
permission2 = {
    'id': permission2_id
}
user_role['permissions'] = [permission1, permission2]

# Save the user role.
result = user_role_service.SaveUserRole(user_role)[0]

# Display results.
print 'User role with ID \'%s\' was created.' % result['id']
