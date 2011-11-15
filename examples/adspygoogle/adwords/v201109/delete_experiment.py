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

"""This example deletes an experiment. To get experiments, run
get_all_experiments.py. To ad an experiment, run add_experiment.py.

Tags: ExperimentService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
experiment_service = client.GetExperimentService(
    'https://adwords-sandbox.google.com', 'v201109')

experiment_id = 'INSERT_EXPERIMENT_ID_HERE'

# Construct operations and delete experiment.
operations = [{
    'operator': 'SET',
    'operand': {
        'id': experiment_id,
        'status': 'DELETED'
    }
}]
result = experiment_service.Mutate(operations)[0]

# Display results.
if 'value' in result:
  for experiment in result['value']:
    print ('Experiment with name \'%s\' and id \'%s\' was deleted.'
           % (experiment['name'], experiment['id']))
else:
  print 'No experiments were deleted.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))