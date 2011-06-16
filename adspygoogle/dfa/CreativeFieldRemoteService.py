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

"""Methods to access CreativeFieldRemoteService service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa import WSDL_MAP
from adspygoogle.dfa.DfaWebService import DfaWebService


class CreativeFieldRemoteService(ApiService):

  """Wrapper for CreativeFieldRemoteService.

  The Creative Field Service allows you to create, update, and retrieve creative
  field and creative field values.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CreativeRemoteService.

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
           'api/dfa-api/creativefield']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(CreativeFieldRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeleteCreativeField(self, creative_field_id):
    """Deletes the creative field with the given id.

    Args:
      creative_field_id: str Id of the creative field to delete.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_field_id, (str, unicode)),))

    method_name = 'deleteCreativeField'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_field_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteCreativeFieldValue(self, creative_field_value_id):
    """Deletes the creative field value object with the given id.

    Args:
      creative_field_value_id: str Id of the creative field to delete.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_field_value_id, (str, unicode)),))

    method_name = 'deleteCreativeFieldValue'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_field_value_id,
                                                 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeField(self, creative_field_id):
    """Returns the creative field for a given id.

    Args:
      creative_field_id: str Id of the creative field to return.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_field_id, (str, unicode)),))

    method_name = 'getCreativeField'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_field_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeFieldValue(self, creative_field_value_id):
    """Returns the creative field value for a given id.

    Args:
      creative_field_value_id: str Id of the creative field value to return.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_field_value_id, (str, unicode)),))

    method_name = 'getCreativeFieldValue'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_field_value_id,
                                                 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeFieldValues(self, creative_field_value_search_criteria):
    """Returns the creative field values matching the given criteria.

    Args:
      creative_field_value_search_criteria: dict Search criteria to match
                                            creative field values.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_field_value_search_criteria,
        'CreativeFieldValueSearchCriteria')

    method_name = 'getCreativeFieldValues'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_field_value_search_criteria,
                  'creativeFieldValueSearchCriteria',
                  self._wsdl_types_map, True,
                  'CreativeFieldValueSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeFields(self, creative_field_search_criteria):
    """Returns the creative fields matching the given criteria.

    Args:
      creative_field_search_criteria: dict Search criteria to match creative
                                      fields.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_field_search_criteria,
        'CreativeFieldSearchCriteria')

    method_name = 'getCreativeFields'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_field_search_criteria, 'creativeFieldSearchCriteria',
                  self._wsdl_types_map, True, 'CreativeFieldSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreativeField(self, creative_field):
    """Saves the given creative field.

    Args:
      creative_field: dict Creative field to save.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_field, 'CreativeField')

    method_name = 'saveCreativeField'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_field, 'creativeField',
                  self._wsdl_types_map, True, 'CreativeField'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreativeFieldValue(self, creative_field_value):
    """Saves the given creative field value.

    Args:
      creative_field_value: dict Creative field value to save.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_field_value, 'CreativeFieldValue')

    method_name = 'saveCreativeFieldValue'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_field_value, 'creativeFieldValue',
                  self._wsdl_types_map, True, 'CreativeFieldValue'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
