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

"""Methods to access PlacementService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class PlacementService(ApiService):

  """Wrapper for PlacementService.

  The Placement Service provides methods for creating, updating and retrieving
  placements.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits PlacementService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = DfpWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(PlacementService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreatePlacement(self, placement):
    """Create a new placement.

    Args:
      placement: dict Placement to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, placement, 'Placement')

    method_name = 'createPlacement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              placement, 'placement', self._wsdl_types_map, False,
              'Placement')))
    elif self._config['soap_lib'] == ZSI:
      placement = self._transformation.MakeZsiCompatible(
          placement, 'Placement', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placement': placement},)),
                                       'Placement', self._loc, request)

  def CreatePlacements(self, placements):
    """Create a list of new placements.

    Args:
      placements: list Placements to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placements, list),))
    for placement in placements:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, placement, 'Placement')

    method_name = 'createPlacements'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              placements, 'placements', self._wsdl_types_map,
              False, 'ArrayOf_Placement')))
    elif self._config['soap_lib'] == ZSI:
      placements = self._transformation.MakeZsiCompatible(
          placements, 'ArrayOf_Placement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placements': placements},)),
                                       'Placement', self._loc, request)

  def GetPlacement(self, placement_id):
    """Return the placement uniquely identified by the given id.

    Args:
      placement_id: str ID of the placement, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placement_id, (str, unicode)),))

    method_name = 'getPlacement'
    if self._config['soap_lib'] == SOAPPY:
      placement_id = self._message_handler.PackVarAsXml(
          placement_id, 'placementId')
      return self.__service.CallMethod(method_name, (placement_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placementId': placement_id},)),
                                       'Placement', self._loc, request)

  def GetPlacementsByStatement(self, filter_statement):
    """Return the placements that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of placements.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getPlacementsByStatement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              filter_statement, 'filterStatement',
              self._wsdl_types_map, False, 'Statement')))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'filterStatement': filter_statement},)),
          'Placement', self._loc, request)

  def PerformPlacementAction(self, action, filter_statement):
    """Perform action on placements that match the given statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, action, 'PlacementAction')

    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'performPlacementAction'
    if self._config['soap_lib'] == SOAPPY:
      action = self._message_handler.PackVarAsXml(
          action, 'placementAction', self._wsdl_types_map, False,
          'PlacementAction')
      filter_statement = self._message_handler.PackVarAsXml(
          filter_statement, 'filterStatement', self._wsdl_types_map, False,
          'Statement')
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._transformation.MakeZsiCompatible(
          action, 'PlacementAction', self._wsdl_types_map,
          self._web_services)
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'placementAction': action},
                         {'filterStatement': filter_statement})),
          'Placement', self._loc, request)

  def UpdatePlacement(self, placement):
    """Update the specified placement.

    Args:
      placement: dict Placement to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, placement, 'Placement')

    method_name = 'updatePlacement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              placement, 'placement', self._wsdl_types_map, False,
              'Placement')))
    elif self._config['soap_lib'] == ZSI:
      placement = self._transformation.MakeZsiCompatible(
          placement, 'Placement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placement': placement},)),
                                       'Placement', self._loc, request)

  def UpdatePlacements(self, placements):
    """Update a list of specified placements.

    Args:
      placements: list Placements to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placements, list),))
    for placement in placements:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, placement, 'Placement')

    method_name = 'updatePlacements'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              placements, 'placements', self._wsdl_types_map, False,
              'ArrayOf_Placement')))
    elif self._config['soap_lib'] == ZSI:
      placements = self._transformation.MakeZsiCompatible(
          placements, 'ArrayOf_Placement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'placements': placements},)),
                                       'Placement', self._loc, request)
