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

"""Methods to access CampaignRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class CampaignRemoteService(ApiService):

  """Wrapper for CampaignRemoteService.

  The Campaign Service allows you to create, update, and retrieve campaign
  objects.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CampaignRemoteService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], op_config['version'],
           'api/dfa-api/campaign']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(CampaignRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def AddLandingPageToCampaign(self, campaign_id, landing_pages):
    """Associates one or more landing page objects with the campaign with the
    given id.

    Args:
      campaign_id: str Campaign id.
      landing_pages: list Landing pages.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),
                               (landing_pages, list)))
    for item in landing_pages:
      self._sanity_check.ValidateLandingPage(item)

    method_name = 'addLandingPageToCampaign'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_id, 'id')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(landing_pages, 'landingPages',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def CopyCampaigns(self, campaign_copy_requests):
    """Create copy of given campaigns.

    Args:
      campaign_copy_requests: list Campaign copy requests.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((campaign_copy_requests, list),))
    for item in campaign_copy_requests:
      self._sanity_check.ValidateCampaignCopyRequest(item)

    method_name = 'copyCampaigns'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_copy_requests,
                                                  'campaignCopyRequests', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteCampaign(self, campaign_id):
    """Delete campaign with a given id.

    Args:
      campaign_id: str Id of the campaign to delete.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),))

    method_name = 'deleteCampaign'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCampaign(self, campaign_id):
    """Return campaign for a given id.

    Args:
      campaign_id: str Id of the campaign to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),))

    method_name = 'getCampaign'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCampaignsByCriteria(self, search_criteria):
    """Return paged record set with campaign objects that satisfy the given
    search criteria.

    Args:
      search_criteria: dict Campaign search criteria.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCampaignSearchCriteria(search_criteria)

    method_name = 'getCampaignsByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                  'campaignSearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetLandingPagesForCampaign(self, campaign_id):
    """Return record set with landing page objects that are associated with the
    given campaign id.

    Args:
      campaign_id: str Id of the campaign to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),))

    method_name = 'getLandingPagesForCampaign'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def MigrateCampaign(self, campaign_migration_request):
    """Migrate DFA5 campaign to DFA6 campaign along with placements, ads, and
    creatives.

    Args:
      campaign_migration_request: dict Request with the DFA5 campaign id and
                                  landing page URL.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCampaignMigrationRequest(
        campaign_migration_request)

    method_name = 'migrateCampaign'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_migration_request,
                                                  'request', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCampaign(self, campaign):
    """Save campaign.

    Args:
      campaign: dict Campaign to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCampaign(campaign)

    method_name = 'saveCampaign'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign, 'campaign', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveLandingPage(self, landing_page):
    """Save landing page.

    Args:
      landing_page: dict Landing page to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateLandingPage(landing_page)

    method_name = 'saveLandingPage'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(landing_page, 'landingPage',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
