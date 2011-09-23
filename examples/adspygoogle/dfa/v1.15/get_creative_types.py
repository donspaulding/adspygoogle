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

"""This example gets available creative types and displays the name and ID for
each type.

Tags: creative.getCreativeTypes
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))
client.debug = True

# Initialize appropriate service.
creative_service = client.GetCreativeService(
    'http://advertisersapitest.doubleclick.net', 'v1.15')

# Get creative types.
results = creative_service.GetCreativeTypes()

# Display creative types and IDs.
if results:
  for creative_type in results:
    print ('Creative type with name \'%s\' and ID \'%s\' was found.'
           % (creative_type['name'], creative_type['id']))
else:
  print 'No creative types found.'
