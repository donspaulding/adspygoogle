#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""This example adds a campaign ad extension to a given campaign. To get
campaigns, run get_campaigns.py.

Tags: GeoLocationService.get, CampaignAdExtensionService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import AdWordsClient


campaign_id = 'INSERT_CAMPAIGN_ID_HERE'


def main(client, campaign_id):
  # Initialize appropriate service.
  geo_location_service = client.GetGeoLocationService(version='v201209')
  campaign_ad_extension_service = client.GetCampaignAdExtensionService(
      version='v201209')

  # Construct selector and get geo location info for given addresses.
  selector = {
      'addresses': [
          {
              'streetAddress': '1600 Amphitheatre Parkway',
              'cityName': 'Mountain View',
              'provinceCode': 'US-CA',
              'provinceName': 'California',
              'postalCode': '94043',
              'countryCode': 'US'
          },
          {
              'streetAddress': '38 avenue de l\'Opéra',
              'cityName': 'Paris',
              'postalCode': '75002',
              'countryCode': 'FR'
          }
      ]
  }
  geo_locations = geo_location_service.Get(selector)

  # Construct operations and add campaign ad extension.
  operations = [
      {
          'operator': 'ADD',
          'operand': {
              'xsi_type': 'CampaignAdExtension',
              'campaignId': campaign_id,
              'adExtension': {
                  'xsi_type': 'LocationExtension',
                  'address': geo_locations[0]['address'],
                  'geoPoint': geo_locations[0]['geoPoint'],
                  'encodedLocation': geo_locations[0]['encodedLocation'],
                  'source': 'ADWORDS_FRONTEND',
                  # Optional fields.
                  'companyName': 'ACME Inc.',
                  'phoneNumber': '(650) 253-0000'
              }
          }
      },
      {
          'operator': 'ADD',
          'operand': {
              'xsi_type': 'CampaignAdExtension',
              'campaignId': campaign_id,
              'adExtension': {
                  'xsi_type': 'LocationExtension',
                  'address': geo_locations[1]['address'],
                  'geoPoint': geo_locations[1]['geoPoint'],
                  'encodedLocation': geo_locations[1]['encodedLocation'],
                  'source': 'ADWORDS_FRONTEND'
              }
          }
      }
  ]
  ad_extensions = campaign_ad_extension_service.Mutate(operations)[0]

  # Display results.
  for ad_extension in ad_extensions['value']:
    print ('Campaign ad extension with id \'%s\' and status \'%s\' was added.'
           % (ad_extension['adExtension']['id'], ad_extension['status']))

  print
  print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                             client.GetOperations()))


if __name__ == '__main__':
  # Initialize client object.
  client = AdWordsClient(path=os.path.join('..', '..', '..', '..', '..'))

  main(client, campaign_id)
