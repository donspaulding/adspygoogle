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

"""Methods to access SubnetworkRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class SubnetworkRemoteService(ApiService):

  """Wrapper for StrategyRemoteService.

  The Subnetwork Service allows you to create and retrieve subnetworks.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits SubnetworkRemoteService.

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
           'api/dfa-api/subnetwork']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(SubnetworkRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def GetAllAvailablePermissions(self):
    """Return supported permissions for the subnetworks.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAllAvailablePermissions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDefaultPermissions(self):
    """Return default permissions for subnetworks.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getDefaultPermissions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSubnetwork(self, subnetwork_id):
    """Return subnetwork for given id.

    Args:
      subnetwork_id: str Id of the subnetwork to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((subnetwork_id, (str, unicode)),))

    method_name = 'getSubnetwork'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(subnetwork_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSubnetworkSummaries(self, subnetwork_search_criteria):
    """Return subnetwork summary matching given criteria.

    Args:
      subnetwork_search_criteria: dict Search criteria to match subnetwork.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSubnetworkSearchCriteria(
        subnetwork_search_criteria)

    method_name = 'getSubnetworkSummaries'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  subnetwork_search_criteria, 'subnetworkSearchCriteria', [],
                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSubnetworks(self, subnetwork_search_criteria):
    """Return subnetwork matching given criteria.

    Args:
      subnetwork_search_criteria: dict Search criteria to match subnetwork.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSubnetworkSearchCriteria(
        subnetwork_search_criteria)

    method_name = 'getSubnetworks'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  subnetwork_search_criteria, 'subnetworkSearchCriteria', [],
                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveSubnetwork(self, subnetwork):
    """Save given subnetwork.

    Args:
      subnetwork: dict Subnetwork to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSubnetwork(subnetwork)

    method_name = 'saveSubnetwork'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(subnetwork, 'subnetwork', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
