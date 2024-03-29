#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
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

"""This code example creates a click-to-download ad, also known as an app
promotion ad to a given ad group. To list ad groups, run get_ad_groups.py.

Tags: AdGroupAdService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


ad_group_id = 'INSERT_AD_GROUP_ID_HERE'


def main(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_ad_service = client.GetAdGroupAdService(version='v201302')

  # Create the template elements for the ad. You can refer to
  #     https://developers.google.com/adwords/api/docs/appendix/templateads
  # for the list of available template fields.
  ad_data = {
      'uniqueName': 'adData',
      'fields': [
          {
              'name': 'headline',
              'fieldText': 'Enjoy your drive in Mars',
              'type': 'TEXT'
          },
          {
              'name': 'description1',
              'fieldText': 'Realistic physics simulation',
              'type': 'TEXT'
          },
          {
              'name': 'description2',
              'fieldText': 'Race against players online',
              'type': 'TEXT'
          },
          {
              'name': 'appId',
              'fieldText': 'com.example.demogame',
              'type': 'TEXT'
          },
          {
              'name': 'appStore',
              'fieldText': '2',
              'type': 'ENUM'
          }
      ]
  }

  # Create click to download ad.
  click_to_download_app_ad = {
      'xsi_type': 'TemplateAd',
      'name': 'Ad for demo game',
      'templateId': '353',
      'url': ('http://play.google.com/store/apps/details?'
              'id=com.example.demogame'),
      'displayUrl': 'play.google.com',
      'templateElements': [ad_data]
  }

  # Create ad group ad.
  ad_group_ad = {
      'adGroupId': ad_group_id,
      'ad': click_to_download_app_ad,
      # Optional.
      'status': 'PAUSED'
  }

  # Add ad.
  ads = ad_group_ad_service.mutate([
      {'operator': 'ADD', 'operand': ad_group_ad}
  ])[0]
  # Display results.
  if 'value' in ads:
    for ad in ads['value']:
      print ('Added new click-to-download ad to ad group ID \'%s\' '
             'with URL \'%s\'.' % (ad['ad']['id'], ad['ad']['url']))
  else:
    print 'No ads were added.'

  print
  print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, ad_group_id)
