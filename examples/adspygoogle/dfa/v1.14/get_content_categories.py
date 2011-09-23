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

"""This example displays available content categories for a given search string.
Results are limited to 10.

Tags: contentcategory.getContentCategories
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.dfa.DfaClient import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
content_category_service = client.GetContentCategoryService(
    'http://advertisersapitest.doubleclick.net', 'v1.14')

search_string = 'INSERT_SEARCH_STRING_HERE'

# Create content category search criteria structure.
content_category_search_criteria = {
    'searchString': search_string,
    'pageSize': '10'
}

# Get content category record set.
results = content_category_service.GetContentCategories(
    content_category_search_criteria)[0]

# Display content category names, IDs and descriptions.
if results['records']:
  for content_category in results['records']:
    print ('Content category with name \'%s\', ID \'%s\', and description'
           ' \'%s\' was found.' % (content_category['name'],
                                   content_category['id'],
                                   content_category['description']))
else:
  print 'No content categories found for your criteria.'
