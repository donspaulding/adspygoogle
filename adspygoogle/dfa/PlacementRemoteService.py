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

"""Methods to access PlacementRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class PlacementRemoteService(ApiService):

  """Wrapper for PlacementRemoteService.

  The Placement Service allows you create, update, delete, and retrieve
  placements.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits PlacementRemoteService.

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
           'api/dfa-api/placement']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(PlacementRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeletePlacement(self, id):
    """Delete the placement with the given id.

    Args:
      id: str Id of the placement to delete.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'deletePlacement'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeletePlacementGroup(self, id):
    """Delete the placement group with the given id.

    Args:
      id: str Id of the placement group to delete.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'deletePlacementGroup'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetInterstitialPlacementTagOptions(self):
    """Return types of regular placement tag options.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getInterstitialPlacementTagOptions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetInStreamVideoPlacementTagOptions(self):
    """Return types of in-stream video placement tag options.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getInStreamVideoPlacementTagOptions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetMobilePlacementTagOptions(self):
    """Return types of mobile placement tag options.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getMobilePlacementTagOptions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacement(self, id):
    """Return placement for a given id.

    Args:
      id: str Id of the placement to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'getPlacement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementGroup(self, id):
    """Return placement group for a given id.

    Args:
      id: str Id of the placement group to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'getPlacementGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementGroupTypes(self):
    """Return types of placement group.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getPlacementGroupTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementGroupsByCriteria(self, search_criteria):
    """Return placement groups matching the given criteria.

    Args:
      search_criteria: dict Search criteria to match placement groups.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementGroupSearchCriteria(search_criteria)

    method_name = 'getPlacementGroupsByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                 'placementGroupSearchCriteria',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementsByCriteria(self, search_criteria):
    """Return placements matching the given criteria.

    Args:
      search_criteria: dict Search criteria to match placements.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementSearchCriteria(search_criteria)

    method_name = 'getPlacementsByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                  'placementSearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementTagData(self, campaign_id, placement_tag_criteria):
    """Replace a rich media asset for a rich media creative.

    Args:
      campaign_id: str Id of the campaign
      placement_tag_criteria: list Placement tag criteria.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),
                               (placement_tag_criteria, list)))
    for item in placement_tag_criteria:
      self._sanity_check.ValidatePlacementTagCriteria(item)

    method_name = 'getPlacementTagData'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(campaign_id, 'campaignId')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(placement_tag_criteria,
                                                  'PlacementTagCriteria',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementTypes(self):
    """Return types of placement.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getPlacementTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPricingTypes(self):
    """Return types of pricing.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getPricingTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetRegularPlacementTagOptions(self):
    """Return types of regular placement tag options.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getRegularPlacementTagOptions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SavePlacement(self, placement):
    """Save given placement.

    Args:
      placement: dict Placement to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacement(placement)

    method_name = 'savePlacement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(placement, 'placement', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SavePlacementGroup(self, placement_group):
    """Save given placement group.

    Args:
      placement_group: dict Placement group to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementGroup(placement_group)

    method_name = 'savePlacementGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(placement_group,
                                                  'placementGroup', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UpdatePlacements(self, request):
    """Update properties of placement.

    Args:
      request: dict Placement update request.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementUpdateRequest(request)

    method_name = 'updatePlacements'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(request, 'request', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
