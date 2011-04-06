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

"""Methods to access ChangeLogRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class ChangeLogRemoteService(ApiService):

  """Wrapper for ChangeLogRemoteService.

  The ChangeLog Service allows you to update and retrieve change log records.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ChangeLogRemoteService.

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
           'api/dfa-api/changelog']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(ChangeLogRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def GetChangeLogObjectTypes(self):
    """Return list of object types that support change logs.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getChangeLogObjectTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetChangeLogRecordForObjectType(self, id, object_type_id):
    """Return change log record for given id and object type.

    Args:
      id: str Id of the change log record.
      object_type_id: str Id of the object type.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),
                               (object_type_id, (str, unicode))))

    method_name = 'getChangeLogRecordForObjectType'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'objectId')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(object_type_id,
                                                  'objectTypeId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetChangeLogRecord(self, change_log_record_id):
    """Return change log record for a given id.

    Args:
      change_log_record_id: str Id of the change log record.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((change_log_record_id, (str, unicode)),))

    method_name = 'getChangeLogRecord'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(change_log_record_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetChangeLogRecords(self, change_log_record_search_criteria):
    """Return change log records matching the given criteria.

    Args:
      change_log_record_search_criteria: dict Change log record search crtieria.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateChangeLogRecordSearchCriteria(
        change_log_record_search_criteria)

    method_name = 'getChangeLogRecords'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  change_log_record_search_criteria,
                  'changeLogRecordSearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UpdateChangeLogRecordComments(self, change_log_record_id, comments):
    """Update comments for the given change log record.

    Args:
      change_log_record_id: str Id of the change log record.
      comments: str Comments to assign to a change record.
    """
    SanityCheck.ValidateTypes(((change_log_record_id, (str, unicode)),
                               (comments, (str, unicode))))

    method_name = 'updateChangeLogRecordComments'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(change_log_record_id, 'id')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(comments, 'comments'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UpdateChangeLogRecordCommentsForObjectType(self, change_log_record_id,
                                                 comments, object_type_id):
    """Update comments for the given change log record.

    Args:
      change_log_record_id: str Id of the change log record.
      comments: str Comments to assign to a change record.
      object_type_id: str Id of the object type.
    """
    SanityCheck.ValidateTypes(((change_log_record_id, (str, unicode)),
                               (comments, (str, unicode)),
                               (object_type_id, (str, unicode))))

    method_name = 'updateChangeLogRecordCommentsForObjectType'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(change_log_record_id,
                                                  'changeLogRecordId')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(comments, 'comments')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(object_type_id,
                                                  'objectTypeId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
