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

"""This example downloads a keywords performance report. To get report fields,
run get_report_fields.py.

Tags: ReportDefinitionService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
report_downloader = client.GetReportDownloader(
    'https://adwords-sandbox.google.com', 'v201109')

# Specify where to download the file here.
path = '/tmp/report_download.csv'

# Construct operations and create report definition.
report = {
    'reportName': 'Keywords performance report #%s' % Utils.GetUniqueName(),
    'dateRangeType': 'YESTERDAY',
    'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
    'downloadFormat': 'CSV',
    'selector': {
        'fields': ['AdGroupId', 'Id', 'KeywordText', 'KeywordMatchType',
                   'Impressions', 'Clicks', 'Cost']
    },
    # Enable to get rows with zero impressions.
    'includeZeroImpressions': 'false'
}

file_path = report_downloader.DownloadReport(report, file_path=path)

print 'Report was downloaded to \'%s\'.' % file_path
