#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover PlacementService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_11
from tests.adspygoogle.dfa import SERVER_V1_12
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import VERSION_V1_11
from tests.adspygoogle.dfa import VERSION_V1_12
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import client


class PlacementServiceTestV1_13(unittest.TestCase):

  """Unittest suite for PlacementService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  service = None
  campaign = None
  placement_id = '0'
  placement_group_id = '0'
  dfa_site_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPlacementService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign is None:
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.campaign = campaign_service.GetCampaignsByCriteria(
          search_criteria)[0]['records'][0]

    if self.__class__.dfa_site_id == '0':
      site_service = client.GetSiteService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {'pageSize': '1'}
      self.__class__.dfa_site_id = site_service.GetDfaSites(
          search_criteria)[0]['records'][0]['id']

  def testSavePlacement(self):
    """Test whether we can save a placement."""
    campaign_id = self.__class__.campaign['id']
    site_id = self.__class__.dfa_site_id
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2]}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 1}
    placement = {
        'name': 'Placement #%s' % Utils.GetUniqueName(),
        'dfaSiteId': site_id,
        'campaignId': campaign_id,
        'pricingSchedule': {
            'endDate': end_date,
            'startDate': start_date,
            'pricingType': '1',
            'pricingPeriods': [{
                'rateOrCost': '1.50',
                'units': '10000',
                'endDate': end_date,
                'startDate': start_date
            }]
        },
        'placementType': '3',
        'sizeId': '2495',
        'tagSettings': {
            'tagTypes': ['1','2','3','4','5','9']
        }
    }
    placement = self.__class__.service.SavePlacement(placement)
    self.__class__.placement_id = placement[0]['id']
    self.assert_(isinstance(placement, tuple))

  def testDeletePlacement(self):
    """Test whether we can delete a placement."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    self.assertEqual(self.__class__.service.DeletePlacement(
        self.__class__.placement_id), None)
    self.__class__.placement_id = '0'

  def testGetPlacement(self):
    """Test whether we can fetch a placement by id."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    placement_id = self.__class__.placement_id
    self.assert_(isinstance(self.__class__.service.GetPlacement(
        placement_id), tuple))

  def testGetPlacements(self):
    """Test whether we can fetch placements by criteria."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    search_criteria = {
        'ids': [self.__class__.placement_id]
    }
    self.assert_(isinstance(self.__class__.service.GetPlacementsByCriteria(
        search_criteria), tuple))

  def testGetInStreamVideoPlacementTagOptions(self):
    """Test whether we can fetch in-stream video placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetInStreamVideoPlacementTagOptions(), tuple))

  def testGetInterstitialPlacementTagOptions(self):
    """Test whether we can fetch interstitial placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetInterstitialPlacementTagOptions(), tuple))

  def testGetMobilePlacementTagOptions(self):
    """Test whether we can fetch mobile placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetMobilePlacementTagOptions(), tuple))

  def testGetPlacementGroupTypes(self):
    """Test whether we can placement group types."""
    self.assert_(isinstance(
        self.__class__.service.GetPlacementGroupTypes(), tuple))

  def testGetPlacementTypes(self):
    """Test whether we can fetch placement types."""
    self.assert_(isinstance(
        self.__class__.service.GetPlacementTypes(), tuple))

  def testGetPricingTypes(self):
    """Test whether we can fetch pricing types."""
    self.assert_(isinstance(
        self.__class__.service.GetPricingTypes(), tuple))

  def testGetRegularPlacementTagOptions(self):
    """Test whether we can fetch regular placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetRegularPlacementTagOptions(), tuple))

  def testSavePlacementGroup(self):
    """Test whether we can save a placement group."""
    campaign_id = self.__class__.campaign['id']
    site_id = self.__class__.dfa_site_id
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2]}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 1}
    placement_group = {
        'name': 'PlacementGroup #%s' % Utils.GetUniqueName(),
        'dfaSiteId': site_id,
        'campaignId': campaign_id,
        'placementGroupType': '1',
        'pricingSchedule': {
            'endDate': end_date,
            'startDate': start_date,
            'pricingType': '1',
            'pricingPeriods': [{
                'rateOrCost': '1.50',
                'units': '10000',
                'endDate': end_date,
                'startDate': start_date
            }]
        }
    }
    placement_group = self.__class__.service.SavePlacementGroup(placement_group)
    self.__class__.placement_group_id = placement_group[0]['id']
    self.assert_(isinstance(placement_group, tuple))

  def testDeletePlacementGroup(self):
    """Test whether we can delete a placement group."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    self.assertEqual(self.__class__.service.DeletePlacementGroup(
        self.__class__.placement_group_id), None)
    self.__class__.placement_group_id = '0'

  def testGetPlacementGroup(self):
    """Test whether we can fetch a placement group by id."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    placement_group_id = self.__class__.placement_group_id
    self.assert_(isinstance(self.__class__.service.GetPlacementGroup(
        placement_group_id), tuple))

  def testGetPlacementGroups(self):
    """Test whether we can fetch placement groups by criteria."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    search_criteria = {
        'ids': [self.__class__.placement_group_id]
    }
    self.assert_(isinstance(self.__class__.service.GetPlacementGroupsByCriteria(
        search_criteria), tuple))

  def testUpdatePlacements(self):
    """Test whether we can update placements."""
    campaign_id = self.__class__.campaign['id']
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2] + 2}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 2}
    placement_update_request = {
        'campaignId' : campaign_id,
        'endDate': end_date,
        'startDate': start_date,
        'updateOption' : '2'
    }
    self.assert_(isinstance(self.__class__.service.UpdatePlacements(
        placement_update_request), tuple))

  def testGetPlacementTagData(self):
    """Test whether we can get placement tag data."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    placement_tag_criteria = [{
        'id' : self.__class__.placement_id,
        'tagOptionIds' : ['1','2','3','4','5','9']
    }]
    campaign_id = self.__class__.campaign['id']
    self.assert_(isinstance(self.__class__.service.GetPlacementTagData(
        campaign_id, placement_tag_criteria), tuple))


class PlacementServiceTestV1_12(unittest.TestCase):

  """Unittest suite for PlacementService using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  client.debug = False
  service = None
  campaign = None
  placement_id = '0'
  placement_group_id = '0'
  dfa_site_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPlacementService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign is None:
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.campaign = campaign_service.GetCampaignsByCriteria(
          search_criteria)[0]['records'][0]

    if self.__class__.dfa_site_id == '0':
      site_service = client.GetSiteService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {'pageSize': '1'}
      self.__class__.dfa_site_id = site_service.GetDfaSites(
          search_criteria)[0]['records'][0]['id']

  def testSavePlacement(self):
    """Test whether we can save a placement."""
    campaign_id = self.__class__.campaign['id']
    site_id = self.__class__.dfa_site_id
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2]}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 1}
    placement = {
        'name': 'Placement #%s' % Utils.GetUniqueName(),
        'dfaSiteId': site_id,
        'campaignId': campaign_id,
        'pricingSchedule': {
            'endDate': end_date,
            'startDate': start_date,
            'pricingType': '1',
            'pricingPeriods': [{
                'rateOrCost': '1.50',
                'units': '10000',
                'endDate': end_date,
                'startDate': start_date
            }]
        },
        'placementType': '3',
        'sizeId': '2495',
        'tagSettings': {
            'tagTypes': ['1','2','3','4','5','9']
        }
    }
    placement = self.__class__.service.SavePlacement(placement)
    self.__class__.placement_id = placement[0]['id']
    self.assert_(isinstance(placement, tuple))

  def testDeletePlacement(self):
    """Test whether we can delete a placement."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    self.assertEqual(self.__class__.service.DeletePlacement(
        self.__class__.placement_id), None)
    self.__class__.placement_id = '0'

  def testGetPlacement(self):
    """Test whether we can fetch a placement by id."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    placement_id = self.__class__.placement_id
    self.assert_(isinstance(self.__class__.service.GetPlacement(
        placement_id), tuple))

  def testGetPlacements(self):
    """Test whether we can fetch placements by criteria."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    search_criteria = {
        'ids': [self.__class__.placement_id]
    }
    self.assert_(isinstance(self.__class__.service.GetPlacementsByCriteria(
        search_criteria), tuple))

  def testGetInStreamVideoPlacementTagOptions(self):
    """Test whether we can fetch in-stream video placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetInStreamVideoPlacementTagOptions(), tuple))

  def testGetInterstitialPlacementTagOptions(self):
    """Test whether we can fetch interstitial placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetInterstitialPlacementTagOptions(), tuple))

  def testGetMobilePlacementTagOptions(self):
    """Test whether we can fetch mobile placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetMobilePlacementTagOptions(), tuple))

  def testGetPlacementGroupTypes(self):
    """Test whether we can placement group types."""
    self.assert_(isinstance(
        self.__class__.service.GetPlacementGroupTypes(), tuple))

  def testGetPlacementTypes(self):
    """Test whether we can fetch placement types."""
    self.assert_(isinstance(
        self.__class__.service.GetPlacementTypes(), tuple))

  def testGetPricingTypes(self):
    """Test whether we can fetch pricing types."""
    self.assert_(isinstance(
        self.__class__.service.GetPricingTypes(), tuple))

  def testGetRegularPlacementTagOptions(self):
    """Test whether we can fetch regular placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetRegularPlacementTagOptions(), tuple))

  def testSavePlacementGroup(self):
    """Test whether we can save a placement group."""
    campaign_id = self.__class__.campaign['id']
    site_id = self.__class__.dfa_site_id
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2]}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 1}
    placement_group = {
        'name': 'PlacementGroup #%s' % Utils.GetUniqueName(),
        'dfaSiteId': site_id,
        'campaignId': campaign_id,
        'placementGroupType': '1',
        'pricingSchedule': {
            'endDate': end_date,
            'startDate': start_date,
            'pricingType': '1',
            'pricingPeriods': [{
                'rateOrCost': '1.50',
                'units': '10000',
                'endDate': end_date,
                'startDate': start_date
            }]
        }
    }
    placement_group = self.__class__.service.SavePlacementGroup(placement_group)
    self.__class__.placement_group_id = placement_group[0]['id']
    self.assert_(isinstance(placement_group, tuple))

  def testDeletePlacementGroup(self):
    """Test whether we can delete a placement group."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    self.assertEqual(self.__class__.service.DeletePlacementGroup(
        self.__class__.placement_group_id), None)
    self.__class__.placement_group_id = '0'

  def testGetPlacementGroup(self):
    """Test whether we can fetch a placement group by id."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    placement_group_id = self.__class__.placement_group_id
    self.assert_(isinstance(self.__class__.service.GetPlacementGroup(
        placement_group_id), tuple))

  def testGetPlacementGroups(self):
    """Test whether we can fetch placement groups by criteria."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    search_criteria = {
        'ids': [self.__class__.placement_group_id]
    }
    self.assert_(isinstance(self.__class__.service.GetPlacementGroupsByCriteria(
        search_criteria), tuple))

  def testUpdatePlacements(self):
    """Test whether we can update placements."""
    campaign_id = self.__class__.campaign['id']
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2] + 2}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 2}
    placement_update_request = {
        'campaignId' : campaign_id,
        'endDate': end_date,
        'startDate': start_date,
        'updateOption' : '2'
    }
    self.assert_(isinstance(self.__class__.service.UpdatePlacements(
        placement_update_request), tuple))

  def testGetPlacementTagData(self):
    """Test whether we can get placement tag data."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    placement_tag_criteria = [{
        'id' : self.__class__.placement_id,
        'tagOptionIds' : ['1','2','3','4','5','9']
    }]
    campaign_id = self.__class__.campaign['id']
    self.assert_(isinstance(self.__class__.service.GetPlacementTagData(
        campaign_id, placement_tag_criteria), tuple))


class PlacementServiceTestV1_11(unittest.TestCase):

  """Unittest suite for PlacementService using v1_11."""

  SERVER = SERVER_V1_11
  VERSION = VERSION_V1_11
  client.debug = False
  service = None
  campaign = None
  placement_id = '0'
  placement_group_id = '0'
  dfa_site_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetPlacementService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign is None:
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {}
      self.__class__.campaign = campaign_service.GetCampaignsByCriteria(
          search_criteria)[0]['records'][0]

    if self.__class__.dfa_site_id == '0':
      site_service = client.GetSiteService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      search_criteria = {'pageSize': '1'}
      self.__class__.dfa_site_id = site_service.GetDfaSites(
          search_criteria)[0]['records'][0]['id']

  def testSavePlacement(self):
    """Test whether we can save a placement."""
    campaign_id = self.__class__.campaign['id']
    site_id = self.__class__.dfa_site_id
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2]}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 1}
    placement = {
        'name': 'Placement #%s' % Utils.GetUniqueName(),
        'dfaSiteId': site_id,
        'campaignId': campaign_id,
        'pricingSchedule': {
            'endDate': end_date,
            'startDate': start_date,
            'pricingType': '1',
            'pricingPeriods': [{
                'rateOrCost': '1.50',
                'units': '10000',
                'endDate': end_date,
                'startDate': start_date
            }]
        },
        'placementType': '3',
        'sizeId': '2495',
        'tagSettings': {
            'tagTypes': ['1','2','3','4','5','9']
        }
    }
    placement = self.__class__.service.SavePlacement(placement)
    self.__class__.placement_id = placement[0]['id']
    self.assert_(isinstance(placement, tuple))

  def testDeletePlacement(self):
    """Test whether we can delete a placement."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    self.assertEqual(self.__class__.service.DeletePlacement(
        self.__class__.placement_id), None)
    self.__class__.placement_id = '0'

  def testGetPlacement(self):
    """Test whether we can fetch a placement by id."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    placement_id = self.__class__.placement_id
    self.assert_(isinstance(self.__class__.service.GetPlacement(
        placement_id), tuple))

  def testGetPlacements(self):
    """Test whether we can fetch placements by criteria."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    search_criteria = {
        'ids': [self.__class__.placement_id]
    }
    self.assert_(isinstance(self.__class__.service.GetPlacementsByCriteria(
        search_criteria), tuple))

  def testGetInterstitialPlacementTagOptions(self):
    """Test whether we can fetch interstitial placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetInterstitialPlacementTagOptions(), tuple))

  def testGetMobilePlacementTagOptions(self):
    """Test whether we can fetch mobile placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetMobilePlacementTagOptions(), tuple))

  def testGetPlacementGroupTypes(self):
    """Test whether we can placement group types."""
    self.assert_(isinstance(
        self.__class__.service.GetPlacementGroupTypes(), tuple))

  def testGetPlacementTypes(self):
    """Test whether we can fetch placement types."""
    self.assert_(isinstance(
        self.__class__.service.GetPlacementTypes(), tuple))

  def testGetPricingTypes(self):
    """Test whether we can fetch pricing types."""
    self.assert_(isinstance(
        self.__class__.service.GetPricingTypes(), tuple))

  def testGetRegularPlacementTagOptions(self):
    """Test whether we can fetch regular placement tag options."""
    self.assert_(isinstance(
        self.__class__.service.GetRegularPlacementTagOptions(), tuple))

  def testSavePlacementGroup(self):
    """Test whether we can save a placement group."""
    campaign_id = self.__class__.campaign['id']
    site_id = self.__class__.dfa_site_id
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2]}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 1}
    placement_group = {
        'name': 'PlacementGroup #%s' % Utils.GetUniqueName(),
        'dfaSiteId': site_id,
        'campaignId': campaign_id,
        'placementGroupType': '1',
        'pricingSchedule': {
            'endDate': end_date,
            'startDate': start_date,
            'pricingType': '1',
            'pricingPeriods': [{
                'rateOrCost': '1.50',
                'units': '10000',
                'endDate': end_date,
                'startDate': start_date
            }]
        }
    }
    placement_group = self.__class__.service.SavePlacementGroup(placement_group)
    self.__class__.placement_group_id = placement_group[0]['id']
    self.assert_(isinstance(placement_group, tuple))

  def testDeletePlacementGroup(self):
    """Test whether we can delete a placement group."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    self.assertEqual(self.__class__.service.DeletePlacementGroup(
        self.__class__.placement_group_id), None)
    self.__class__.placement_group_id = '0'

  def testGetPlacementGroup(self):
    """Test whether we can fetch a placement group by id."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    placement_group_id = self.__class__.placement_group_id
    self.assert_(isinstance(self.__class__.service.GetPlacementGroup(
        placement_group_id), tuple))

  def testGetPlacementGroups(self):
    """Test whether we can fetch placement groups by criteria."""
    if self.__class__.placement_group_id == '0':
      self.testSavePlacementGroup()
    search_criteria = {
        'ids': [self.__class__.placement_group_id]
    }
    self.assert_(isinstance(self.__class__.service.GetPlacementGroupsByCriteria(
        search_criteria), tuple))

  def testUpdatePlacements(self):
    """Test whether we can update placements."""
    campaign_id = self.__class__.campaign['id']
    start_date_dict = self.__class__.campaign['startDate']
    end_date_dict = self.__class__.campaign['endDate']
    start_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': start_date_dict[0],
        'month': start_date_dict[1],
        'day': start_date_dict[2] + 2}
    end_date = '%(year)s-%(month)02d-%(day)02dT12:00:00' % {
        'year': end_date_dict[0],
        'month': end_date_dict[1],
        'day': end_date_dict[2] - 2}
    placement_update_request = {
        'campaignId' : campaign_id,
        'endDate': end_date,
        'startDate': start_date,
        'updateOption' : '2'
    }
    self.assert_(isinstance(self.__class__.service.UpdatePlacements(
        placement_update_request), tuple))

  def testGetPlacementTagData(self):
    """Test whether we can get placement tag data."""
    if self.__class__.placement_id == '0':
      self.testSavePlacement()
    placement_tag_criteria = [{
        'id' : self.__class__.placement_id,
        'tagOptionIds' : ['1','2','3','4','5','9']
    }]
    campaign_id = self.__class__.campaign['id']
    self.assert_(isinstance(self.__class__.service.GetPlacementTagData(
        campaign_id, placement_tag_criteria), tuple))


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PlacementServiceTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PlacementServiceTestV1_12))
  return suite


def makeTestSuiteV1_11():
  """Set up test suite using v1_11.

  Returns:
    TestSuite test suite using v1_11.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(PlacementServiceTestV1_11))
  return suite


if __name__ == '__main__':
  suite_v1_13 = makeTestSuiteV1_13()
  suite_v1_12 = makeTestSuiteV1_12()
  suite_v1_11 = makeTestSuiteV1_11()
  alltests = unittest.TestSuite([suite_v1_13, suite_v1_12, suite_v1_11])
  unittest.main(defaultTest='alltests')
