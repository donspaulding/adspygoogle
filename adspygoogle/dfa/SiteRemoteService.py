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

"""Methods to access SiteRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class SiteRemoteService(ApiService):

  """Wrapper for SiteRemoteService.

  The Site Service allows you to create and retrieve sites.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits SiteRemoteService.

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
           'api/dfa-api/site']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(SiteRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def GetAvailableDfaSiteContactTypes(self):
    """Return available site contact types.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAvailableDfaSiteContactTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetContacts(self, search_criteria):
    """Return list of site directory contacts matching the given criteria.

    Args:
      search_criteria: dict Contact search criteria.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateContactSearchCriteria(search_criteria)

    method_name = 'getContacts'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                  'contactSearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDfaSite(self, dfa_site_id):
    """Return DFA site for a given id.

    Args:
      dfa_site_id: str Id of the DFA site to return.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((dfa_site_id, (str, unicode)),))

    method_name = 'getDfaSite'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(dfa_site_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDfaSites(self, search_criteria):
    """Return DFA sites matching the given criteria.

    Args:
      search_criteria: dict Search criteria to match DFA sites.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateDfaSiteSearchCriteria(search_criteria)

    method_name = 'getDfaSites'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(search_criteria,
                                                  'dfaSiteSearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSitesByCriteria(self, site_search_criteria):
    """Return sites matching the given criteria.

    Args:
      site_search_criteria: dict Search criteria to match sites.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSiteSearchCriteria(site_search_criteria)

    method_name = 'getSitesByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(site_search_criteria,
                                                  'siteSearchCriteria', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ImportSiteDirectorySites(self, requests):
    """Import site directory sites into the network.

    Args:
      requests: list Site directory sites to import.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((requests, list),))
    for item in requests:
      self._sanity_check.ValidateSiteDirectorySiteImportRequest(item)

    method_name = 'importSiteDirectorySites'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(requests,
                                                  'siteDirectoryImportRequest',
                                                  [], [], False))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def LinkDfaSiteToSiteDirectorySite(self, dfa_site_id, site_directory_site_id):
    """Link DFA site to a site directory site.

    Args:
      dfa_site_id: str Id of the DFA site to link.
      site_directory_site_id: str Id of the site directory site.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((dfa_site_id, (str, unicode)),
                               (site_directory_site_id, (str, unicode))))

    method_name = 'linkDfaSiteToSiteDirectorySite'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(dfa_site_id, 'dfaSiteId')),
           self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(site_directory_site_id,
                                                  'siteDirectorySiteId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def LinkDfaSitesToSiteDirectorySites(
      self, site_directory_dfa_site_mapping_requests):
    """Link DFA sites to site directory sites.

    Args:
      site_directory_dfa_site_mapping_requests: list DFA sites to link.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((site_directory_dfa_site_mapping_requests,
                                list),))
    for item in site_directory_dfa_site_mapping_requests:
      self._sanity_check.ValidateSiteDirectoryDfaSiteMappingRequest(item)

    method_name = 'linkDfaSitesToSiteDirectorySites'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  site_directory_dfa_site_mapping_requests, 'requests', [], [],
                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveDfaSite(self, dfa_site):
    """Save given DFA site.

    Args:
      dfa_site: dict DFA site to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateDfaSite(dfa_site)

    method_name = 'saveDfaSite'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(dfa_site, 'dfaSite', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
