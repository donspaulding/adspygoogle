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

"""This code example updates labels that are competitive exclusion by updating
the description up to the first 500. To determine which labels exist,
run get_all_labels.py.  This feature is only available to DFP premium solution
networks."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# the sandbox environment.
label_service = client.GetLabelService('https://sandbox.google.com', 'v201108')

#Create a statement to only select labels that are competitive sorted by name.
values = [
    {
        'key': 'type',
        'value': {
            'xsi_type': 'TextValue',
            'value': 'COMPETITIVE_EXCLUSION'
        }
    },
    {
        'key': 'isActive',
        'value': {
            'xsi_type': 'BooleanValue',
            'value': 'true'
        }
    }
]

filter_statement = {
    'query': 'WHERE type = :type and isActive = :isActive LIMIT 500',
    'values': values}

# Get labels by filter.
labels = label_service.GetLabelsByStatement(filter_statement)[0]['results']

if labels:
  # Update each local label object by changing the description.
  for label in labels:
    label['description'] = 'These labels are still competing with each other.'

  # Update labels remotely.
  labels = label_service.UpdateLabels(labels)

  # Display results.
  if labels:
    for label in labels:
      print ('Label with id \'%s\', name \'%s\' was updated.'
             % (label['id'], label['name']))
  else:
    print 'No labels were updated.'
else:
  print 'No labels found to update.'
