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

"""Methods to access AdvertiserGroupRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class AdvertiserGroupRemoteService(ApiService):

  """Wrapper for AdvertiserGroupRemoteService.

  The AdvertiserGroup Service allows you to create, update, and delete
  advertiser group objects.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AdvertiserGroupRemoteService.

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
           'api/dfa-api/advertisergroup']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(AdvertiserGroupRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def AssignAdvertisersToAdvertiserGroup(self, advertiser_group_id,
                                         advertiser_ids):
    """Assign one or more advertisers to one or more advertiser groups.

    Args:
      advertiser_group_id: str Advertiser group id.
      advertiser_ids: list Advertiser ids.
    """
    SanityCheck.ValidateTypes(((advertiser_group_id, (str, unicode)),))
    SanityCheck.ValidateTypes(((advertiser_ids, list),))
    for item in advertiser_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'assignAdvertisersToAdvertiserGroup'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_group_id, 'id')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_ids, 'ids', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)


  def DeleteAdvertiserGroup(self, advertiser_group_id):
    """Delete advertiser group with the given id.

    Args:
      advertiser_group_id: str Advertiser group id.
    """
    SanityCheck.ValidateTypes(((advertiser_group_id, (str, unicode)),))

    method_name = 'deleteAdvertiserGroup'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_group_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAdvertiserGroup(self, advertiser_group_id):
    """Return advertiser group with the given id.

    Args:
      advertiser_group_id: str Id of the advertiser group to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((advertiser_group_id, (str, unicode)),))

    method_name = 'getAdvertiserGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_group_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAdvertiserGroups(self, advertiser_group_search_criteria):
    """Return advertiser groups in the user's network based on the criteria
    object passed in.

    Args:
      advertiser_group_search_criteria: dict Search criteria for retrieving
                                        advertiser groups.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateAdvertiserGroupSearchCriteria(
        advertiser_group_search_criteria)

    method_name = 'getAdvertiserGroups'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  advertiser_group_search_criteria,
                  'advertiserGroupSearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveAdvertiserGroup(self, advertiser_group):
    """Save given advertiser group object.

    Args:
      advertiser_group: dict Advertiser group object to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateAdvertiserGroup(advertiser_group)

    method_name = 'saveAdvertiserGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_group,
                                                  'advertiserGroup', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
