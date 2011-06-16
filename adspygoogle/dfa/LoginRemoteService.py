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

"""Methods to access LoginRemoteService service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa import WSDL_MAP
from adspygoogle.dfa.DfaWebService import DfaWebService


class LoginRemoteService(ApiService):

  """Wrapper for LoginRemoteService.

  The Login Service allows you to log in into the DFA and perform various
  authentication routines.

  The LoginRemoteService is the only service that still uses SOAPpy's default
  "<v1>...</v1>" parameter wrapping.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits LoginRemoteService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], op_config['version'], 'api/dfa-api/login']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(LoginRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def Authenticate(self, username, password):
    """Returns the profile for authenticated credentials.

    Args:
      username: str Account's user name.
      password: str Account's password.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((username, (str, unicode)),
                               (password, (str, unicode))))

    method_name = 'authenticate'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(username, 'username')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                password, 'password'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ChangePassword(self, change_password_request):
    """Changes the password for a given user.

    Args:
      change_password_request: dict Change password request.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, change_password_request, 'ChangePasswordRequest')

    method_name = 'changePassword'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  change_password_request, 'changePasswordRequest',
                  self._wsdl_types_map, True, 'ChangePasswordRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ImpersonateNetwork(self, username, token, network_id):
    """Impersonates a given network.

    Args:
      username: str Super user's login.
      token: str Super user's authentication token.
      network_id: str Id of the network to impersonate.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((username, (str, unicode)),
                               (token, (str, unicode)),
                               (network_id, (str, unicode))))

    method_name = 'impersonateNetwork'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(username, 'username')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(token, 'token')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                network_id, 'networkId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ImpersonateUser(self, username, token, user_to_impersonate):
    """Impersonates a given user.

    Args:
      username: str Super user's login.
      token: str Super user's authentication token.
      user_to_impersonate: str User to impersonate.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((username, (str, unicode)),
                               (token, (str, unicode)),
                               (user_to_impersonate, (str, unicode))))

    method_name = 'impersonateUser'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(username, 'username')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(token, 'token')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                user_to_impersonate, 'username'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
