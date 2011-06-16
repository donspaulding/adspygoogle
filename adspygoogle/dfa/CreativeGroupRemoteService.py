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

"""Methods to access CreativeGroupRemoteService service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa import WSDL_MAP
from adspygoogle.dfa.DfaWebService import DfaWebService


class CreativeGroupRemoteService(ApiService):

  """Wrapper for CreativeGroupRemoteService.

  The CreativeGroup Service allows you to create, update, and retrieve creative
  groups.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CreativeGroupRemoteService.

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
           'api/dfa-api/creativegroup']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(CreativeGroupRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeleteCreativeGroup(self, creative_group_id):
    """Deletes the creative with the given id.

    Args:
      creative_group_id: str Id of the creative group to delete.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_group_id, (str, unicode)),))

    method_name = 'deleteCreativeGroup'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_group_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeGroup(self, id):
    """Returns the creative group for a given id.

    Args:
      id: str Id of the creative group to return.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'getCreativeGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeGroups(self, search_criteria):
    """Returns the creative groups matching the given criteria.

    Args:
      search_criteria: dict Search criteria to match creative groups.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, search_criteria, 'CreativeGroupSearchCriteria')

    method_name = 'getCreativeGroups'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  search_criteria, 'creativeGroupSearchCriteria',
                  self._wsdl_types_map, True, 'CreativeGroupSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreativeGroup(self, creative_group):
    """Saves the given creative group.

    Args:
      creative_group: dict Creative group to save.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_group, 'CreativeGroup')

    method_name = 'saveCreativeGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_group, 'creativeGroup',
                  self._wsdl_types_map, True, 'CreativeGroup'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
