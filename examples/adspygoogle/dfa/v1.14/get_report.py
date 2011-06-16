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

"""This example fetches information about a report, including its status
(pending, running, complete, etc.) and a URL where it can be downloaded if
completed. To get a report ID, run run_deferred_report.py.

Tags: report.getReport
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
reporting_service = client.GetReportService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

report_id = 'INSERT_REPORT_ID_HERE'

# Create report search criteria structure.
report_request = {
    'reportId': report_id
}

# Fetch report information.
report_info = reporting_service.GetReport(report_request)[0]

# Display information on the report.
print ('Report with ID \'%s\', status of \'%s\', and URL of \'%s\' was'
       ' found.' % (report_info['reportId'], report_info['status']['name'],
                    report_info['url']))
