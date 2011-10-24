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

"""This example gets all LocationCriterion.

Tags: LocationCriterionService.get
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


def GetLocationString(location):
  return '%s (%s)' % (location['locationName'], location.get('displayType'))

# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
location_criterion_service = client.GetLocationCriterionService(
    'https://adwords-sandbox.google.com', 'v201109')

location_names = ['Paris', 'Quebec', 'Spain', 'Deutchland']

# Create the selector.
selector = {
    'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
               'ParentLocations', 'Reach'],
    'predicates': [{
        'field': 'LocationName',
        'operator': 'IN',
        'values': location_names
    },
    {
        'field': 'Locale',
        'operator': 'EQUALS',
        'values': ['en']
    }]
}

# Make the get request.
location_criteria = location_criterion_service.Get(selector)

# Display the resulting location criteria.
for location_criterion in location_criteria:
  parent_string = ', '.join([GetLocationString(parent) for parent in
                             location_criterion['location']['parentLocations']])
  print ('The search term \'%s\' returned the location \'%s\' of type \'%s\''
         ' with parent locations \'%s\' and reach \'%s\''
         % (location_criterion['searchTerm'],
            location_criterion['location']['locationName'],
            location_criterion['location']['displayType'], parent_string,
            location_criterion.get('reach')))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
