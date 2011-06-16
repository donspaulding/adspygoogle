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

"""Methods to access AdRemoteService service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa import DfaUtils
from adspygoogle.dfa import WSDL_MAP
from adspygoogle.dfa.DfaWebService import DfaWebService


class AdRemoteService(ApiService):

  """Wrapper for AdRemoteService.

  The Ad Service allows you to create, modify, and delete ads and ad properties.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AdRemoteService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], op_config['version'], 'api/dfa-api/ad']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(AdRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def CopyAds(self, ad_copy_requests):
    """Creates copies of ads in bulk.

    Args:
      ad_copy_requests: list Object containing copy request parameters.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((ad_copy_requests, list),))
    for item in ad_copy_requests:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, item, 'AdCopyRequest')

    method_name = 'copyAds'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  ad_copy_requests, 'adCopyRequest', self._wsdl_types_map, True,
                  'ArrayOfAdCopyRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteAd(self, ad_id):
    """Deletes the ad with the given id.

    Args:
      ad_id: str Id of the ad to delete.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((ad_id, (str, unicode)),))

    method_name = 'deleteAd'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(ad_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAd(self, ad_id):
    """Returns the ad with the given id.

    Args:
      ad_id: str Id of the ad to retrieve.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((ad_id, (str, unicode)),))

    method_name = 'getAd'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(ad_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAdTypes(self):
    """Returns all available ad types.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getAdTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAds(self, ad_search_criteria):
    """Returns a single page of ads matching the given criteria.

    Args:
      ad_search_criteria: dict Search criteria specifying what ads to return.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, ad_search_criteria, 'AdSearchCriteria')

    method_name = 'getAds'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  ad_search_criteria, 'adSearchCriteria',
                  self._wsdl_types_map, True, 'AdSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAreaCodes(self, country_ids):
    """Returns an array of area codes that DFA can target ads to.

    Args:
      country_ids: list Country IDs to get area codes for.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((country_ids, list),))
    for item in country_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'getAreaCodes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(country_ids, 'countryIds',
                                                 [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetBandwidths(self):
    """Returns a localized list of bandwidths that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getBandwidths'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetBrowsers(self):
    """Returns a localized list of browsers that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getBrowsers'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCities(self, city_search_criteria):
    """Returns cities in given countries and/or regions that can be targeted.

    Args:
      city_search_criteria: dict Search criteria object encapsulating search
                            parameters.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, city_search_criteria, 'CitySearchCriteria')

    method_name = 'getCities'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  city_search_criteria, 'citySearchCriteria',
                  self._wsdl_types_map, True, 'CitySearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCountries(self):
    """Returns a list of countries that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getCountries'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDesignatedMarketAreas(self):
    """Returns a list of designated market areas that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getDesignatedMarketAreas'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDomainNamesBySearchCriteria(self, search_criteria):
    """Returns a set of domain names for the given search criteria.

    Args:
      search_criteria: dict Object to specify search parameters.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, search_criteria, 'DomainNameSearchCriteria')

    method_name = 'getDomainNamesBySearchCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  search_criteria, 'domainNameSearchCriteria',
                  self._wsdl_types_map, True, 'DomainNameSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetDomainTypes(self):
    """Returns an array of Domain Types that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getDomainTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetISPs(self):
    """Returns an array of Internet Service Providers that DFA can target.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getISPs'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetMobilePlatforms(self):
    """Returns an array of mobile platforms that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getMobilePlatforms'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetOSPs(self):
    """Returns an array of Online Service Providers that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getOSPs'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetOperatingSystems(self):
    """Returns a list of operating systems that can be targeted by DFA.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getOperatingSystems'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetRegions(self, country_ids):
    """Returns an array of regions that DFA can target for given country ids.

    Args:
      country_ids: list Country ids that will be used to find Regions.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((country_ids, list),))
    for item in country_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'getRegions'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(country_ids, 'countryIds',
                                                 [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetStates(self, country_ids):
    """Returns an array of states that DFA can target for given country ids.

    Args:
      country_ids: list Country ids.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((country_ids, list),))
    for item in country_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'getStates'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(country_ids, 'countryIds',
                                                 [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetUserListGroupsByCriteria(self, search_criteria):
    """Returns an array of remarketing user list groups by search criteria.

    Args:
      search_criteria: dict Object containing search parameters.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, search_criteria, 'UserListSearchCriteria')

    method_name = 'getUserListGroupsByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  search_criteria, 'userListSearchCriteria',
                  self._wsdl_types_map, True, 'UserListSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetUserListsByCriteria(self, search_criteria):
    """Returns remarketing user lists based on search criteria.

    Args:
      search_criteria: dict Object containing search parameters.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, search_criteria, 'UserListSearchCriteria')

    method_name = 'getUserListsByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  search_criteria, 'userListSearchCriteria',
                  self._wsdl_types_map, True, 'UserListSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def OverrideAdProperties(self, overridable_ad_properties):
    """Saves overridden ad properties for given placement and ad combination.

    Args:
      overridable_ad_properties: dict Overridable ad properties.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, overridable_ad_properties,
        'OverridableAdProperties')

    method_name = 'overrideAdProperties'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  overridable_ad_properties, 'overridableAdProperties',
                  self._wsdl_types_map, True, 'OverridableAdProperties'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveAd(self, ad):
    """Saves the given ad object.

    Args:
      ad: dict Ad to save.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, ad, 'AdBase')
    DfaUtils.AssignAdXsi(ad)

    method_name = 'saveAd'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  ad, 'Ad', self._wsdl_types_map, True, 'AdBase'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UpdateCreativeAssignmentProperties(self, association_update_request):
    """Updates properties of creative-ad associations.

    Args:
      association_update_request: dict Request to update ad creative
                                  associations.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, association_update_request,
        'CreativeAdAssociationUpdateRequest')

    method_name = 'updateCreativeAssignmentProperties'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  association_update_request, 'request', self._wsdl_types_map,
                  True, 'CreativeAdAssociationUpdateRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
