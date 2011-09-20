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

"""Methods to access InventoryService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class InventoryService(ApiService):

  """Wrapper for InventoryService.

  The Inventory Service provides operations for creating, updating and
  retrieving ad units.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits InventoryService.

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
    super(InventoryService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateAdUnit(self, ad_unit):
    """Create a new ad unit.

    Args:
      ad_unit: dict Ad unit to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, ad_unit, 'AdUnit')

    method_name = 'createAdUnit'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              ad_unit, 'adUnit', self._wsdl_types_map, False, 'AdUnit')))
    elif self._config['soap_lib'] == ZSI:
      ad_unit = self._transformation.MakeZsiCompatible(
          ad_unit, 'AdUnit', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'adUnit': ad_unit},)),
                                       'Inventory', self._loc, request)

  def CreateAdUnits(self, ad_units):
    """Create a list of new ad units.

    Args:
      ad_units: list Ad units to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((ad_units, list),))
    for ad_unit in ad_units:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, ad_unit, 'AdUnit')

    method_name = 'createAdUnits'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              ad_units, 'adUnits', self._wsdl_types_map, False,
              'ArrayOf_AdUnit')))
    elif self._config['soap_lib'] == ZSI:
      ad_units = self._transformation.MakeZsiCompatible(
          ad_units, 'ArrayOf_AdUnit', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'adUnits': ad_units},)),
                                       'Inventory', self._loc, request)

  def GetAdUnit(self, ad_unit_id):
    """Return the ad unit uniquely identified by the given id.

    Args:
      ad_unit_id: str ID of the ad unit, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((ad_unit_id, (str, unicode)),))

    method_name = 'getAdUnit'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(ad_unit_id,
                                                           'adUnitId')))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'adUnitId': ad_unit_id},)),
                                       'Inventory', self._loc, request)

  def GetAdUnitSizes(self):
    """Retrieves the sorted set of sizes across all ad units.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAdUnitSizes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Inventory', self._loc,
                                       request)

  def GetAdUnitsByStatement(self, filter_statement):
    """Return the ad units that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of ad units.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getAdUnitsByStatement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              filter_statement, 'filterStatement', self._wsdl_types_map, False,
              'Statement')))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'filterStatement': filter_statement},)),
          'Inventory', self._loc, request)

  def PerformAdUnitAction(self, action, filter_statement):
    """Perform action on ad units that match the given statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, action, 'AdUnitAction')
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'performAdUnitAction'
    if self._config['soap_lib'] == SOAPPY:
      action = self._message_handler.PackVarAsXml(
          action, 'adUnitAction', self._wsdl_types_map, False, 'AdUnitAction')
      filter_statement = self._message_handler.PackVarAsXml(
          filter_statement, 'filterStatement', self._wsdl_types_map, False,
          'Statement')
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._transformation.MakeZsiCompatible(
          action, 'AdUnitAction', self._wsdl_types_map,
          self._web_services)
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'adUnitAction': action},
                         {'filterStatement': filter_statement})),
          'Inventory', self._loc, request)

  def UpdateAdUnit(self, ad_unit):
    """Update the specified ad unit.

    Args:
      ad_unit: dict Ad unit to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, ad_unit, 'AdUnit')

    method_name = 'updateAdUnit'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              ad_unit, 'adUnit', self._wsdl_types_map, False, 'AdUnit')))
    elif self._config['soap_lib'] == ZSI:
      ad_unit = self._transformation.MakeZsiCompatible(
          ad_unit, 'AdUnit', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'adUnit': ad_unit},)),
                                       'Inventory', self._loc, request)

  def UpdateAdUnits(self, ad_units):
    """Update a list of specified ad units.

    Args:
      ad_units: list Ad units to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((ad_units, list),))
    for ad_unit in ad_units:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, ad_unit, 'AdUnit')

    method_name = 'updateAdUnits'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              ad_units, 'adUnits', self._wsdl_types_map, False,
              'ArrayOf_AdUnit')))
    elif self._config['soap_lib'] == ZSI:
      ad_units = self._transformation.MakeZsiCompatible(
          ad_units, 'ArrayOf_AdUnit', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'adUnits': ad_units},)),
                                       'Inventory', self._loc, request)
