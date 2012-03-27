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

"""This code example updates the names of all companies that are advertisers by
appending ' LLC.' up to the first 500. To determine which companies exist, run
get_all_companies.py."""

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

# Initialize appropriate service.
company_service = client.GetService(
    'CompanyService', 'https://www.google.com', 'v201203')

# Create statement object to only select companies that are advertises.
values = [{
    'key': 'type',
    'value': {
        'xsi_type': 'TextValue',
        'value': 'ADVERTISER'
    }
}]
filter_statement = {'query': 'WHERE type = :type LIMIT 500', 'values': values}

# Get companies by statement.
response = company_service.GetCompaniesByStatement(filter_statement)[0]
companies = []
if 'results' in response:
  companies = response['results']

if companies:
  # Update each local company object by appending ' LLC.' to its name.
  for company in companies:
    company['name'] += ' LLC.'

  # Update companies remotely.
  companies = company_service.UpdateCompanies(companies)

  # Display results.
  if companies:
    for company in companies:
      print ('Company with id \'%s\' and name \'%s\' was updated.'
             % (company['id'], company['name']))
  else:
    print 'No companies were updated.'
else:
  print 'No companies found to update.'
