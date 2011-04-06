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

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
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
    super(CreativeFieldRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeleteCreativeField(self, creative_field_id):
    """Delete the creative field with the given id.

    Args:
      creative_field_id: str Id of the creative field to delete.
    """
    SanityCheck.ValidateTypes(((creative_field_id, (str, unicode)),))

    method_name = 'deleteCreativeField'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(creative_field_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteCreativeFieldValue(self, creative_field_value_id):
    """Delete the creative field value object with the given id.

    Args:
      creative_field_value_id: str Id of the creative field to delete.
    """
    SanityCheck.ValidateTypes(((creative_field_value_id, (str, unicode)),))

    method_name = 'deleteCreativeFieldValue'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(creative_field_value_id,
                                                  'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeField(self, creative_field_id):
    """Return creative field for a given id.

    Args:
      creative_field_id: str Id of the creative field to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((creative_field_id, (str, unicode)),))

    method_name = 'getCreativeField'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(creative_field_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeFieldValue(self, creative_field_value_id):
    """Return creative field value for a given id.

    Args:
      creative_field_value_id: str Id of the creative field value to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((creative_field_value_id, (str, unicode)),))

    method_name = 'getCreativeFieldValue'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(creative_field_value_id,
                                                  'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeFieldValues(self, creative_field_value_search_criteria):
    """Return the creative field values matching the given criteria.

    Args:
      creative_field_value_search_criteria: dict Search criteria to match
                                            creative field values.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCreativeFieldValueSearchCriteria(
        creative_field_value_search_criteria)

    method_name = 'getCreativeFieldValues'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  creative_field_value_search_criteria,
                  'creativeFieldValueSearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeFields(self, creative_field_search_criteria):
    """Return the creative fields matching the given criteria.

    Args:
      creative_field_search_criteria: dict Search criteria to match creative
                                      fields.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCreativeFieldSearchCriteria(
        creative_field_search_criteria)

    method_name = 'getCreativeFields'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  creative_field_search_criteria,
                  'creativeFieldSearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreativeField(self, creative_field):
    """Save given creative field.

    Args:
      creative_field: dict Creative field to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCreativeField(creative_field)

    method_name = 'saveCreativeField'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(creative_field,
                                                  'creativeField', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreativeFieldValue(self, creative_field_value):
    """Save given creative field value.

    Args:
      creative_field_value: dict Creative field value to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCreativeFieldValue(creative_field_value)

    method_name = 'saveCreativeFieldValue'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(creative_field_value,
                                                  'creativeFieldValue', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
