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

"""This example creates a mobile creative asset in a given advertiser. Currently
only gif, jpg, jpeg, png and wbmp files are supported as mobile assets. To
create an advertiser, run create_advertiser.py.

Tags: creative.saveCreativeAsset
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import base64
import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.dfa.DfaClient import DfaClient


# Initialize client object.
client = DfaClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
creative_service = client.GetCreativeService(
    'http://advertisersapitest.doubleclick.net', 'v1.15')

advertiser_id = 'INSERT_ADVERTISER_ID_HERE'
asset_name = 'INSERT_MOBILE_ASSET_NAME_HERE'
path_to_file = 'INSERT_PATH_TO_FILE_HERE'

# Convert file into format that can be sent in SOAP messages.
content = Utils.ReadFile(path_to_file)
if client._config['soap_lib'] == SOAPPY:
  content = base64.encodestring(content)

# Construct and save mobile asset.
image_asset = {
    'name': asset_name,
    'advertiserId': advertiser_id,
    'content': content,
    'forHTMLCreatives': 'true'
}
result = creative_service.SaveCreativeAsset(image_asset)[0]

# Display results.
print ('Creative asset with file name of \'%s\' was created.'
       % result['savedFilename'])
