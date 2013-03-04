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

"""Unit tests to cover Advanced Operations examples."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))
import unittest

from examples.adspygoogle.adwords.v201302.advanced_operations import add_click_to_download_ad
from examples.adspygoogle.adwords.v201302.advanced_operations import add_site_links
from tests.adspygoogle.adwords import client
from tests.adspygoogle.adwords import util
from tests.adspygoogle.adwords import SERVER_V201302
from tests.adspygoogle.adwords import TEST_VERSION_V201302
from tests.adspygoogle.adwords import VERSION_V201302


class AdvancedOperations(unittest.TestCase):

  """Unittest suite for Advanced Operations code examples."""

  SERVER = SERVER_V201302
  VERSION = VERSION_V201302
  client.debug = False
  loaded = False

  def setUp(self):
    """Prepare unittest."""
    if not self.loaded:
      self.campaign_id = util.CreateTestEnhancedCampaign(client)
      self.ad_group_id = util.CreateTestAdGroup(client, self.campaign_id)

  def testAddClickToDownloadAd(self):
    """Tests whether we can create an account."""
    add_click_to_download_ad.main(client, self.ad_group_id)

  def testAddSiteLink(self):
    """Test whether we can get account alerts."""
    add_site_links.main(client, self.campaign_id)


if __name__ == '__main__':
  if TEST_VERSION_V201302:
    unittest.main()
