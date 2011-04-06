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

"""Methods to access StrategyRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class StrategyRemoteService(ApiService):

  """Wrapper for StrategyRemoteService.

  The Strategy Service allows you to create, delete, and retrieve strategies.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits SizeRemoteService.

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
           'api/dfa-api/strategy']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(StrategyRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeletePlacementStrategy(self, placement_strategy_id):
    """Delete placement strategy for given id.

    Args:
      placement_strategy_id: str Id of the placement strategy to delete.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placement_strategy_id, (str, unicode)),))

    method_name = 'deletePlacementStrategy'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(placement_strategy_id,
                                                  'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementStrategiesByCriteria(self,
                                       placement_strategy_search_criteria):
    """Return placement strategy matching given criteria.

    Args:
      placement_strategy_search_criteria: dict Search criteria to match
                                          placement strategy.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementStrategySearchCriteria(
        placement_strategy_search_criteria)

    method_name = 'getPlacementStrategiesByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  placement_strategy_search_criteria,
                  'placementStrategySearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetPlacementStrategy(self, placement_strategy_id):
    """Return placement strategy for given id.

    Args:
      placement_strategy_id: str Id of the placement strategy to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((placement_strategy_id, (str, unicode)),))

    method_name = 'getPlacementStrategy'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(placement_strategy_id,
                                                  'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SavePlacementStrategy(self, placement_strategy):
    """Save given placement strategy.

    Args:
      placement_strategy: dict Placement strategy to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementStrategy(placement_strategy)

    method_name = 'savePlacementStrategy'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(placement_strategy,
                                                  'placementStrategy', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
