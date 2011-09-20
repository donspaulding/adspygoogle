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

"""Methods to access CustomTargetingService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class CustomTargetingService(ApiService):

  """Wrapper for CustomTargetingService.

  The CustomTargeting Service provides methods for creating, updating and
  retrieving custom targeting keys and values.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CustomTargetingService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: Dict dictionary object with additional configuration values for
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
    super(CustomTargetingService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateCustomTargetingKeys(self, keys):
    """Create a list of new custom targeting keys.

    Args:
      keys: list Custom targeting keys to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((keys, list),))
    for key in keys:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, key,
                                 'CustomTargetingKey')

    method_name = 'createCustomTargetingKeys'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              keys, 'keys', self._wsdl_types_map, False,
              'ArrayOf_CustomTargetingKey')))
    elif self._config['soap_lib'] == ZSI:
      keys = self._transformation.MakeZsiCompatible(
          keys, 'ArrayOf_CustomTargetingKey', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'keys': keys},)),
                                       'CustomTargeting', self._loc, request)

  def CreateCustomTargetingValues(self, values):
    """Create a list of new custom targeting values.

    Args:
      values: list Custom targeting values to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((values, list),))
    for value in values:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, value,
                                 'CustomTargetingValue')

    method_name = 'createCustomTargetingValues'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              values, 'values', self._wsdl_types_map, False,
              'ArrayOf_CustomTargetingValue')))
    elif self._config['soap_lib'] == ZSI:
      values = self._transformation.MakeZsiCompatible(
          values, 'ArrayOf_CustomTargetingValue', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'values': values},)),
                                       'CustomTargeting', self._loc, request)

  def GetCustomTargetingKeysByStatement(self, filter_statement):
    """Return the custom targeting keys that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of custom targeting keys.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getCustomTargetingKeysByStatement'
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
          'CustomTargeting', self._loc, request)

  def GetCustomTargetingValuesByStatement(self, filter_statement):
    """Return the custom targeting values that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of custom targeting values.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getCustomTargetingValuesByStatement'
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
          'CustomTargeting', self._loc, request)

  def PerformCustomTargetingKeyAction(self, action, filter_statement):
    """Perform action on custom targeting keys that match the given statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, action, 'CustomTargetingKeyAction')
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'performCustomTargetingKeyAction'
    if self._config['soap_lib'] == SOAPPY:
      action = self._message_handler.PackVarAsXml(
          action, 'customTargetingKeyAction', self._wsdl_types_map, False,
          'CustomTargetingKeyAction')
      filter_statement = self._message_handler.PackVarAsXml(
          filter_statement, 'filterStatement', self._wsdl_types_map, False,
          'Statement')
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._transformation.MakeZsiCompatible(
          action, 'CustomTargetingKeyAction', self._wsdl_types_map,
          self._web_services)
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'customTargetingKeyAction': action},
                         {'filterStatement': filter_statement})),
          'CustomTargeting', self._loc, request)

  def PerformCustomTargetingValueAction(self, action, filter_statement):
    """Perform action on custom targeting values that match the given statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, action, 'CustomTargetingValueAction')
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'performCustomTargetingValueAction'
    if self._config['soap_lib'] == SOAPPY:
      action = self._message_handler.PackVarAsXml(
          action, 'customTargetingValueAction', self._wsdl_types_map, False,
          'CustomTargetingValueAction')
      filter_statement = self._message_handler.PackVarAsXml(
          filter_statement, 'filterStatement', self._wsdl_types_map, False,
          'Statement')
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._transformation.MakeZsiCompatible(
          action, 'CustomTargetingValueAction', self._wsdl_types_map,
          self._web_services)
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'customTargetingValueAction': action},
                         {'filterStatement': filter_statement})),
          'CustomTargeting', self._loc, request)

  def UpdateCustomTargetingKeys(self, keys):
    """Update a list of specified custom targeting keys.

    Args:
      keys: list Custom targeting keys to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((keys, list),))
    for key in keys:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, key,
                                 'CustomTargetingKey')

    method_name = 'updateCustomTargetingKeys'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              keys, 'keys', self._wsdl_types_map, False,
              'ArrayOf_CustomTargetingKey')))
    elif self._config['soap_lib'] == ZSI:
      keys = self._transformation.MakeZsiCompatible(
          keys, 'ArrayOf_CustomTargetingKey', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'keys': keys},)),
                                       'CustomTargeting', self._loc, request)

  def UpdateCustomTargetingValues(self, values):
    """Update a list of specified custom targeting values.

    Args:
      values: list Custom targeting values to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((values, list),))
    for value in values:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, value,
                                 'CustomTargetingValue')

    method_name = 'updateCustomTargetingValues'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              values, 'values', self._wsdl_types_map, False,
              'ArrayOf_CustomTargetingValue')))
    elif self._config['soap_lib'] == ZSI:
      values = self._transformation.MakeZsiCompatible(
          values, 'ArrayOf_CustomTargetingValue', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'values': values},)),
                                       'CustomTargeting', self._loc, request)
