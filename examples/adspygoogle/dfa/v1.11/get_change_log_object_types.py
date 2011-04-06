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

"""This example displays change log object type names and IDs.

Tags: changelog.getChangeLogObjectTypes
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
change_log_service = client.GetChangeLogService(
    'http://advertisersapitest.doubleclick.net', 'v1.11')

# Get change log object types.
results = change_log_service.GetChangeLogObjectTypes()

# Display change log object type names and IDs.
if results:
  for object_type in results:
    print ('Change log object type with name \'%s\' and ID \'%s\' was found.'
           % (object_type['name'], object_type['id']))
else:
  print 'No change log object types found.'
