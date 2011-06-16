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

""" This example assigns creatives to placements and creates a unique ad for
each assignment. To get creatives, run GetCreatives.java example. To get
placements, run get_placement.py.

Tags: creative.assignCreativesToPlacements
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
creative_service = client.GetCreativeService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

creative_ids = ['INSERT_FIRST_CREATIVE_ID', 'INSERT_SECOND_CREATIVE_ID']
placement_ids = ['INSERT_FIRST_PLACEMENT_ID', 'INSERT_SECOND_PLACEMENT_ID']

# Create creative placement assignment structure.
creative_placement_assignments = []
for index in range(len(creative_ids)):
  creative_placement_assignments.append({
      'xsi_type': 'CreativePlacementAssignment',
      'creativeId': creative_ids[index],
      'placementId': placement_ids[index],
      'placementIds': placement_ids
  })

# Submit the request.
results = creative_service.AssignCreativesToPlacements(
    creative_placement_assignments);

# Display results.
if results:
  for assignment_result in results:
    if assignment_result['errorMessage'] is None:
      print ('Ad with name \'%s\' and ID \'%s\' was created.' %
             (assignment_result['adName'], assignment_result['adId']))
    else:
      print ('Assignment unsuccessful for creative ID \'%s\' and placementID'
             ' \'%s\'. Error message says \'%s\'.'
             % (assignment_result['creativeId'],
                assignment_result['placementId'],
                assignment_result['errorMessage']))
else:
  print 'No ads were created.'
