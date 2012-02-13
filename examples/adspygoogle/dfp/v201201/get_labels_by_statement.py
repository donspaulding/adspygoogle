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

"""This code example gets labels that are in competitive exclusion with a
statement. To create an label, run create_label.py.  This feature is only
available to DFP premium solution networks."""

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
# sandbox environment.
label_service = client.GetService(
    'LabelService', 'https://sandbox.google.com', 'v201201')

# Create a statement to only select labels that are competitive, sorted by name.
values = [{
    'key': 'type',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'COMPETITIVE_EXCLUSION'
    }
}]

filter_statement = {'query': 'WHERE type = :type ORDER BY name LIMIT 500',
                    'values': values}

# Get labels by statement.
response = label_service.GetLabelsByStatement(filter_statement)[0]
labels = []
if 'results' in response:
  labels = response['results']

# Display results.
for label in labels:
  print ('Label with id \'%s\', name \'%s\', and type \'%s\' was found.'
         % (label['id'], label['name'], label['type']))

print
print 'Number of results found: %s' % len(labels)