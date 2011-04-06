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

"""Methods to access SpotlightRemoteService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa.DfaWebService import DfaWebService


class SpotlightRemoteService(ApiService):

  """Wrapper for SpotlightRemoteService.

  The Spotlight Service allows you to create, update, delete, or retrieve
  spotlights.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits SpotlightRemoteService.

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
           'api/dfa-api/spotlight']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    super(SpotlightRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def DeleteSpotlightActivity(self, spotlight_activity_id):
    """Delete the spotlight activity with the given id.

    Args:
      spotlight_activity_id: str Id of the spotlight activity to delete.
    """
    SanityCheck.ValidateTypes(((spotlight_activity_id, (str, unicode)),))

    method_name = 'deleteSpotlightActivity'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(spotlight_activity_id,
                                                  'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteSpotlightActivityGroup(self, spotlight_activity_group_id):
    """Delete the spotlight activity group with the given id.

    Args:
      spotlight_activity_group_id: str Id of the spotlight activity group to
                                   delete.
    """
    SanityCheck.ValidateTypes(((spotlight_activity_group_id, (str, unicode)),))

    method_name = 'deleteSpotlightActivityGroup'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  spotlight_activity_group_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GenerateTags(self, activity_ids):
    """Return string consisting of the spotlight activity tags.

    Args:
      activity_ids: list Ids of spotlight activities.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((activity_ids, list),))
    for item in activity_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'generateTags'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(activity_ids, 'activityIds',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAvailableCustomSpotlightVariables(self):
    """Return available custom spotlight variables.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAvailableCustomSpotlightVariables'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAvailableStandardVariables(self):
    """Return available standard variables.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAvailableStandardVariables'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCountriesByCriteria(self, country_search_criteria):
    """Return countries matching the given criteria.

    Args:
      country_search_criteria: dict Search criteria to match countries.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateCountriesSearchCriteria(country_search_criteria)

    method_name = 'getCountriesByCriteria'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(country_search_criteria,
                                                  'countrySearchCriteria', [],
                                                  [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightActivities(self, spotlight_activity_search_criteria):
    """Return single page of Spotlight Activities matching the given criteria.

    Args:
      spotlight_activity_search_criteria: dict Search criteria to match
                                          spotlight activities.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSpotlightActivitySearchCriteria(
        spotlight_activity_search_criteria)

    method_name = 'getSpotlightActivities'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  spotlight_activity_search_criteria,
                  'spotlightActivitySearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightActivity(self, spotlight_activity_id):
    """Return spotlight activity for a given id.

    Args:
      spotlight_activity_id: str Id of the spotlight activity.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((spotlight_activity_id, (str, unicode)),))

    method_name = 'getSpotlightActivity'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(spotlight_activity_id,
                                                  'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightActivityGroups(self,
                                 spotlight_activity_group_search_criteria):
    """Return spotlight activity groups matching the given criteria.

    Args:
      spotlight_activity_group_search_criteria: dict Search criteria to match
                                                spotlight activity groups.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSpotlightActivityGroupSearchCriteria(
        spotlight_activity_group_search_criteria)

    method_name = 'getSpotlightActivityGroups'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(
                  spotlight_activity_group_search_criteria,
                  'spotlightActivityGroupSearchCriteria', [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightActivityTypes(self):
    """Return types of spotlight activities.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getSpotlightActivityTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightConfiguration(self, id):
    """Return spotlight configuration for a given id.

    Args:
      id: str Id of the spotlight configuration.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((id, (str, unicode)),))

    method_name = 'getSpotlightConfiguration'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightTagCodeTypes(self):
    """Return types of spotlight tag codes.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getSpotlightTagCodeTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightTagFormatTypes(self):
    """Return types of spotlight tag formats.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getSpotlightTagFormatTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetSpotlightTagMethodTypes(self):
    """Return types of spotlight tag methods.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getSpotlightTagMethodTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveSpotlightActivity(self, spotlight_activity):
    """Save given spotlight activity.

    Args:
      spotlight_activity: dict Spotlight activity to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSpotlightActivity(spotlight_activity)

    method_name = 'saveSpotlightActivity'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(spotlight_activity,
                                                  'spotlightActivity', [], [],
                                                  True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveSpotlightActivityGroup(self, spotlight_activity_group):
    """Save given spotlight activity group.

    Args:
      spotlight_activity_group: dict Spotlight activity group to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidateSpotlightActivityGroup(spotlight_activity_group)

    method_name = 'saveSpotlightActivityGroup'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(spotlight_activity_group,
                                                  'spotlightActivityGroup',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveSpotlightConfiguration(self, spotlight_configuration):
    """Save given spotlight configuration.

    Args:
      spotlight_configuration: dict Spotlight configuration to save.

    Returns:
      tuple Response from the API method.
    """
    self._sanity_check.ValidatePlacementUpdateRequest(spotlight_configuration)

    method_name = 'saveSpotlightConfiguration'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name,
          (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackDictAsXml(spotlight_configuration,
                                                  'spotlightConfiguration',
                                                  [], [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
