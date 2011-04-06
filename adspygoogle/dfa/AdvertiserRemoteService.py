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

"""Methods to access AdvertiserRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class AdvertiserRemoteService(ApiService):

  """Wrapper for AdvertiserRemoteService.

  The Advertiser Service allows you to create, update, and retrieve advertiser
  objects.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AdvertiserRemoteService.

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
           'api/dfa-api/advertiser']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(AdvertiserRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeleteAdvertiser(self, advertiser_id):
    """Delete advertiser with the given id.

    Args:
      advertiser_id: str Advertiser Id.
    """
    SanityCheck.ValidateTypes(((advertiser_id, (str, unicode)),))

    method_name = 'deleteAdvertiser'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAdvertisers(self, advertiser_search_criteria):
    """Return record set with advertiser objects that satisfy the given search
    criteria.

    Args:
      advertiser_search_criteria: dict Search criteria.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateAdvertiserSearchCriteria(
        advertiser_search_criteria)

    method_name = 'getAdvertisers'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser_search_criteria,
                                                  'advertiserSearchCriteria',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveAdvertiser(self, advertiser):
    """Save specified advertiser.

    Args:
      advertiser: dict Advertiser to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateAdvertiser(advertiser)

    method_name = 'saveAdvertiser'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(advertiser, 'advertiser', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
