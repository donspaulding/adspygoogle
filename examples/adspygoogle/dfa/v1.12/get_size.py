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

"""This example gets the size ID for a given width and height.

Tags: size.getSize
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
size_service = client.GetSizeService(
    'http://advertisersapitest.doubleclick.net', 'v1.12')

width = 'INSERT_WIDTH_HERE'
height = 'INSERT_HEIGHT_HERE'

# Get size.
size = size_service.GetSizeByWidthHeight(width, height)[0]

# Display size ID.
if size:
  print 'Size id for \'%sx%s\' is \'%s\'.' % (width, height, size['id'])
else:
  print 'No size found for your criteria.'
