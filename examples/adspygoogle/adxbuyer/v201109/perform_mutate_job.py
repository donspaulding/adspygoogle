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

"""This code sample illustrates how to perform asynchronous requests using the
MutateJobService.

Tags: MutateJobService.mutate, MutateJobService.get, MutateJobService.getResult
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import random
import re
import sys
import time
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


RETRY_INTERVAL = 30
RETRIES_COUNT = 30
PLACEMENT_NUMBER = 100
INDEX_REGEX = r'operations\[(\d+)\].operand'

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'

# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
mutate_job_service = client.GetMutateJobService(
    'https://adwords-sandbox.google.com', 'v201109')

# Create list of all operations for the job.
operations = []

  # Create AdGroupCriterionOperations to add placements.
for i in range(PLACEMENT_NUMBER):
  if random.randint(1,10) == 1:
    url = 'invalid-url/%d' % i
  else:
    url = 'http://mars.google.com/%d' % i

  operations.append({
      'xsi_type': 'AdGroupCriterionOperation',
      'operator': 'ADD',
      'operand': {
          'xsi_type': 'BiddableAdGroupCriterion',
          'adGroupId': ad_group_id,
          'criterion': {
              'xsi_type': 'Placement',
              'url': url
          }
      }
  })

# You can specify up to 3 job IDs that must successfully complete before
# this job can be processed.
policy = {
    'prerequisiteJobIds': []
}

# Call mutate to create a new job.
response = mutate_job_service.Mutate(operations, policy)[0]

if not response:
  raise 'Failed to submit a job; aborting.'

job_id = response['id']
print 'Job with ID %s was successfully created.' % job_id

# Create selector to retrieve job status and wait for it to complete.
selector = {
    'xsi_type': 'BulkMutateJobSelector',
    'jobIds': [job_id]
}

# Poll for job status until it's finished.
print 'Retrieving job status...'
for i in range(RETRIES_COUNT):
  job_status_response = mutate_job_service.Get(selector)
  status = job_status_response[0]['status']
  if status in ('COMPLETED', 'FAILED'):
    break
  print ('[%d] Current status is \'%s\', waiting %d seconds to retry...' %
      (i, status, RETRY_INTERVAL))
  time.sleep(RETRY_INTERVAL)

if status == 'FAILED':
  raise ('Job failed with reason: \'%s\'' %
      job_status_response[0]['failure_reason'])
if status in ('PROCESSING', 'PENDING'):
  raise ('Job did not complete within %d seconds' %
      (RETRY_INTERVAL * (RETRIES_COUNT - 1)))

# Status must be COMPLETED.
# Get the job result. Here we re-use the same selector.
result_response = mutate_job_service.GetResult(selector)[0]

# Output results.
index = 0
for result in result_response['SimpleMutateResult']['results']:
  if 'PlaceHolder' in result:
    print 'Operation [%d] - FAILED' % index
  else:
    print 'Operation [%d] - SUCCEEDED' % index
  index += 1

# Output errors
for error in result_response['SimpleMutateResult']['errors']:
  index = int(re.search(INDEX_REGEX, error['fieldPath']).group(1))
  reason = error['reason']
  placement = operations[index]['operand']['criterion']['url']
  print ('ERROR - placement \'%s\' failed due to \'%s\'' %
         (placement, reason))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))