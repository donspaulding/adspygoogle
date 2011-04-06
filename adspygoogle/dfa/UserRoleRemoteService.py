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

"""Methods to access UserRoleRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class UserRoleRemoteService(ApiService):

  """Wrapper for UserRoleRemoteService.

  The UserRole Service allows you to create, delete, and retrieve user roles.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits UserRoleRemoteService.

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
           'api/dfa-api/userrole']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(UserRoleRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeleteUserRole(self, id):
    """Delete user role for given id.

    Args:
      id: str Id of the user role to delete.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'deleteUserRole'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAvailablePermissions(self, subnetwork_id):
    """Return available permissions.

    Args:
      subnetwork_id: str Id of the subnetwork for which to return permissions.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((subnetwork_id, (str, unicode)),))

    method_name = 'getAvailablePermissions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(subnetwork_id,
                                                  'subnetworkId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetUserRole(self, user_role_id):
    """Return user role for given id.

    Args:
      user_role_id: str Id of the user role to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((user_role_id, (str, unicode)),))

    method_name = 'getUserRole'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(user_role_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetUserRoles(self, search_criteria):
    """Return user roles matching given criteria.

    Args:
      search_criteria: dict Search criteria to match user roles.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateUserRoleSearchCriteria(search_criteria)

    method_name = 'getUserRoles'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                  'userRoleSearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetUserRoleSummaries(self, search_criteria):
    """Return user role summaries matching given criteria.

    Args:
      search_criteria: dict Search criteria to match user roles.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateUserRoleSearchCriteria(search_criteria)

    method_name = 'getUserRoleSummaries'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                  'userRoleSearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveUserRole(self, user_role):
    """Save given user role.

    Args:
      user_role: dict User role to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateUserRole(user_role)

    method_name = 'saveUserRole'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(user_role, 'userRole', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
