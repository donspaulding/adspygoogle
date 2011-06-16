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

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa import WSDL_MAP
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
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(SiteRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def GetAvailableDfaSiteContactTypes(self):
    """Returns available site contact types.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
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
    """Returns a list of site directory contacts matching the given criteria.

    Args:
      search_criteria: dict Contact search criteria.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, search_criteria, 'ContactSearchCriteria')

    method_name = 'getContacts'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  search_criteria, 'contactSearchCriteria',
                  self._wsdl_types_map, True, 'ContactSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDfaSite(self, dfa_site_id):
    """Returns the DFA site for a given id.

    Args:
      dfa_site_id: str Id of the DFA site to return.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((dfa_site_id, (str, unicode)),))

    method_name = 'getDfaSite'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(dfa_site_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDfaSites(self, search_criteria):
    """Returns DFA sites matching the given criteria.

    Args:
      search_criteria: dict Search criteria to match DFA sites.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, search_criteria, 'DfaSiteSearchCriteria')

    method_name = 'getDfaSites'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  search_criteria, 'dfaSiteSearchCriteria',
                  self._wsdl_types_map, True, 'DfaSiteSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSitesByCriteria(self, site_search_criteria):
    """Returns sites matching the given criteria.

    Args:
      site_search_criteria: dict Search criteria to match sites.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, site_search_criteria, 'SiteSearchCriteria')

    method_name = 'getSitesByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  site_search_criteria, 'siteSearchCriteria',
                  self._wsdl_types_map, True, 'SiteSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ImportSiteDirectorySites(self, requests):
    """Imports the site directory sites into the network.

    Args:
      requests: list Site directory sites to import.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((requests, list),))
    for item in requests:
      SanityCheck.NewSanityCheck(
          self._wsdl_types_map, item, 'SiteDirectorySiteImportRequest')

    method_name = 'importSiteDirectorySites'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  requests, 'siteDirectoryImportRequest', self._wsdl_types_map,
                  True, 'ArrayOfSiteDirectoryImportRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def LinkDfaSiteToSiteDirectorySite(self, dfa_site_id, site_directory_site_id):
    """Links a DFA site to a site directory site.

    Args:
      dfa_site_id: str Id of the DFA site to link.
      site_directory_site_id: str Id of the site directory site.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((dfa_site_id, (str, unicode)),
                               (site_directory_site_id, (str, unicode))))

    method_name = 'linkDfaSiteToSiteDirectorySite'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(dfa_site_id, 'dfaSiteId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                site_directory_site_id,
                                'siteDirectorySiteId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def LinkDfaSitesToSiteDirectorySites(
      self, site_directory_dfa_site_mapping_requests):
    """Links DFA sites to site directory sites.

    Args:
      site_directory_dfa_site_mapping_requests: list DFA sites to link.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((site_directory_dfa_site_mapping_requests,
                                list),))
    for item in site_directory_dfa_site_mapping_requests:
      SanityCheck.NewSanityCheck(
          self._wsdl_types_map, item, 'SiteDirectoryDfaSiteMappingRequest')

    method_name = 'linkDfaSitesToSiteDirectorySites'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  site_directory_dfa_site_mapping_requests, 'requests',
                  self._wsdl_types_map, True,
                  'ArrayOfSiteDirectoryDfaSiteMappingRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveDfaSite(self, dfa_site):
    """Saves a given DFA site.

    Args:
      dfa_site: dict DFA site to save.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, dfa_site, 'DfaSite')

    method_name = 'saveDfaSite'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  dfa_site, 'dfaSite', self._wsdl_types_map, True, 'DfaSite'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
