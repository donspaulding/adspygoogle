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

"""This code example archives all active third party slots for a company.
To determine which third party slots exist, run get_all_third_party_slots.py."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfp import DfpUtils
from adspygoogle.dfp.DfpClient import DfpClient


# Initialize client object.
client = DfpClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service. By default, the request is always made against
# sandbox environment.
third_party_slot_service = client.GetThirdPartySlotService(
    'https://sandbox.google.com', 'v201111')

company_id = 'INSERT_COMPANY_ID_HERE'

# Create query.
query = 'WHERE status = \'ACTIVE\' and companyId = ' + company_id

# Get third party slots by statement.
third_party_slots = DfpUtils.GetAllEntitiesByStatementWithService(
    third_party_slot_service, query)

for third_party_slot in third_party_slots:
  print ('Third party slot with id \'%s\' will be archived.'
         % third_party_slot['id'])

print ('Number of third party slots to be archived: %s'
       % len(third_party_slots))

# Perform action.
result = third_party_slot_service.PerformThirdPartySlotAction(
    {'type': 'ArchiveThirdPartySlots'}, {'query': query})[0]

# Display results.
if result and int(result['numChanges']) > 0:
  print 'Number of third party slots archived: %s' % result['numChanges']
else:
  print 'No third party slots were archived.'
