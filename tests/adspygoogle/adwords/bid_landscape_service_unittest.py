#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Unit tests to cover BidLandscapeService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V201003
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import TEST_VERSION_V201003
from tests.adspygoogle.adwords import TEST_VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import client


class BidLandscapeServiceTestV201003(unittest.TestCase):

  """Unittest suite for BidLandscapeService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  ad_group_id = '0'
  criterion_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetBidLandscapeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0' or self.__class__.criterion_id == '0':
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'name': 'Campaign #%s' % Utils.GetUniqueName(),
              'status': 'PAUSED',
              'biddingStrategy': {
                'type': 'ManualCPC'
              },
              'budget': {
                  'period': 'DAILY',
                  'amount': {
                      'microAmount': '1000000'
                  },
                  'deliveryMethod': 'STANDARD'
              }
          }
      }]
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      self.__class__.ad_group_id = \
          ad_group_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_criterion_service = client.GetAdGroupCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'BiddableAdGroupCriterion',
              'adGroupId': self.__class__.ad_group_id,
              'criterion': {
                  'type': 'Keyword',
                  'matchType': 'BROAD',
                  'text': 'mars cruise'
              }
          }
      }]
      self.__class__.criterion_id = ad_group_criterion_service.Mutate(
          operations)[0]['value'][0]['criterion']['id']

  def testGetBidLandscape(self):
    """Test whether we can fetch existing bid landscape for a given ad group
    and criterion."""
    selector = {
        'type': 'CriterionBidLandscapeSelector',
        'idFilters': [{
            'adGroupId': self.__class__.ad_group_id,
            'criterionId': self.__class__.criterion_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.GetBidLandscape(selector),
                            tuple))


class BidLandscapeServiceTestV201008(unittest.TestCase):

  """Unittest suite for BidLandscapeService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None
  ad_group_id = '0'
  criterion_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetBidLandscapeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0' or self.__class__.criterion_id == '0':
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'name': 'Campaign #%s' % Utils.GetUniqueName(),
              'status': 'PAUSED',
              'biddingStrategy': {
                'type': 'ManualCPC'
              },
              'budget': {
                  'period': 'DAILY',
                  'amount': {
                      'microAmount': '1000000'
                  },
                  'deliveryMethod': 'STANDARD'
              }
          }
      }]
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      self.__class__.ad_group_id = \
          ad_group_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_criterion_service = client.GetAdGroupCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'BiddableAdGroupCriterion',
              'adGroupId': self.__class__.ad_group_id,
              'criterion': {
                  'type': 'Keyword',
                  'matchType': 'BROAD',
                  'text': 'mars cruise'
              }
          }
      }]
      self.__class__.criterion_id = ad_group_criterion_service.Mutate(
          operations)[0]['value'][0]['criterion']['id']

  def testGetCriterionBidLandscape(self):
    """Test whether we can fetch existing criterion bid landscape for a given
    ad group and criterion."""
    selector = {
        'type': 'CriterionBidLandscapeSelector',
        'idFilters': [{
            'adGroupId': self.__class__.ad_group_id,
            'criterionId': self.__class__.criterion_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.GetBidLandscape(selector),
                            tuple))

  def testGetAdGroupBidLandscape(self):
    """Test whether we can fetch existing criterion bid landscape for a given
    ad group and criterion."""
    selector = {
        'type': 'AdGroupBidLandscapeSelector',
        'idFilters': [{
            'adGroupId': self.__class__.ad_group_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.GetBidLandscape(selector),
                            tuple))


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(BidLandscapeServiceTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(BidLandscapeServiceTestV201008))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V201003:
    suites.append(makeTestSuiteV201003())
  if TEST_VERSION_V201008:
    suites.append(makeTestSuiteV201008())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
