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

"""This example authenticates using your DFA user name and password, and
displays the user profile token, DFA account name and ID.

Tags: login.authenticate
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
login_service = client.GetLoginService(
    'https://advertisersapitest.doubleclick.net', 'v1.17')

username = 'INSERT_USER_NAME_HERE'
password = 'INSERT_PASSWORD_HERE'

# Authenticate.
user_profile = login_service.Authenticate(username, password)[0]

# Display user profile token, DFA account name and ID.
print ('User profile token is \'%s\', DFA account name is \'%s\', and DFA'
       ' account ID is \'%s\'.' % (user_profile['token'],
                                   user_profile['networkName'],
                                   user_profile['networkId']))
