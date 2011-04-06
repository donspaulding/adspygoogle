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

"""Interface for accessing all other services."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import thread

from adspygoogle.common import SOAPPY
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Client import Client
from adspygoogle.common.Errors import AuthTokenError
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.Logger import Logger
from adspygoogle.dfa import LIB_SIG
from adspygoogle.dfa import MIN_API_VERSION
from adspygoogle.dfa import REQUIRED_SOAP_HEADERS
from adspygoogle.dfa import DfaSanityCheck
from adspygoogle.dfa.AdRemoteService import AdRemoteService
from adspygoogle.dfa.AdvertiserGroupRemoteService import AdvertiserGroupRemoteService
from adspygoogle.dfa.AdvertiserRemoteService import AdvertiserRemoteService
from adspygoogle.dfa.CampaignRemoteService import CampaignRemoteService
from adspygoogle.dfa.ChangeLogRemoteService import ChangeLogRemoteService
from adspygoogle.dfa.ContentCategoryRemoteService import ContentCategoryRemoteService
from adspygoogle.dfa.CreativeFieldRemoteService import CreativeFieldRemoteService
from adspygoogle.dfa.CreativeGroupRemoteService import CreativeGroupRemoteService
from adspygoogle.dfa.CreativeRemoteService import CreativeRemoteService
from adspygoogle.dfa.DfaWebService import DfaWebService
from adspygoogle.dfa.LoginRemoteService import LoginRemoteService
from adspygoogle.dfa.NetworkRemoteService import NetworkRemoteService
from adspygoogle.dfa.PlacementRemoteService import PlacementRemoteService
from adspygoogle.dfa.ReportRemoteService import ReportRemoteService
from adspygoogle.dfa.SiteRemoteService import SiteRemoteService
from adspygoogle.dfa.SizeRemoteService import SizeRemoteService
from adspygoogle.dfa.SpotlightRemoteService import SpotlightRemoteService
from adspygoogle.dfa.StrategyRemoteService import StrategyRemoteService
from adspygoogle.dfa.SubnetworkRemoteService import SubnetworkRemoteService
from adspygoogle.dfa.UserRemoteService import UserRemoteService
from adspygoogle.dfa.UserRoleRemoteService import UserRoleRemoteService


class DfaClient(Client):

  """Provides entry point to all web services.

  Allows instantiation of all DFA API web services.
  """

  auth_pkl_name = 'dfa_api_auth.pkl'
  config_pkl_name = 'dfa_api_config.pkl'

  def __init__(self, headers=None, config=None, path=None):
    """Inits DfaClient.

    Args:
      [optional]
      headers: dict Object with populated authentication credentials.
      config: dict Object with client configuration values.
      path: str Relative or absolute path to home directory (i.e. location of
            pickles and logs/).

      Example:
        headers = {
          'Username': 'johndoe@example.com',
          'Password': 'secret',
          'AuthToken': '...'
        }
        config = {
          'home': '/path/to/home',
          'log_home': '/path/to/logs/home',
          'xml_parser': PYXML,
          'debug': 'n',
          'raw_debug': 'n',
          'xml_log': 'y',
          'request_log': 'y',
          'raw_response': 'n',
          'strict': 'y',
          'pretty_xml': 'y',
          'compress': 'y',
          'force_data_inject': 'y'
        }
        path = '/path/to/home'
    """
    super(DfaClient, self).__init__(headers, config, path)

    self.__lock = thread.allocate_lock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of DfaClient, based on
      # provided relative path.
      if os.path.isabs(path):
        DfaClient.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to DfaClient.home. Otherwise, may break when
        # multiple instances of DfaClient exist during program run.
        DfaClient.home = os.path.join(os.getcwd(), path)

      # If pickles don't exist at given location, default to "~".
      if (not headers and not config and
          (not os.path.exists(os.path.join(DfaClient.home,
                                           DfaClient.auth_pkl_name)) or
           not os.path.exists(os.path.join(DfaClient.home,
                                           DfaClient.config_pkl_name)))):
        DfaClient.home = os.path.expanduser('~')
    else:
      DfaClient.home = os.path.expanduser('~')

    # Update location for both pickles.
    DfaClient.auth_pkl = os.path.join(DfaClient.home,
                                      DfaClient.auth_pkl_name)
    DfaClient.config_pkl = os.path.join(DfaClient.home,
                                        DfaClient.config_pkl_name)

    # Only load from the pickle if config wasn't specified.
    self._config = config or self.__LoadConfigValues()
    self._config = self.__SetMissingDefaultConfigValues(self._config)
    self._config['home'] = DfaClient.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self._config['xml_parser'])

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self._headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self._config['strict']):
        SanityCheck.ValidateRequiredHeaders(headers, REQUIRED_SOAP_HEADERS)
      self._headers = headers

    # Initialize logger.
    self.__logger = Logger(LIB_SIG, self._config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from dfa_api_auth.pkl.

    Returns:
      dict Dictionary object with populated authentication credentials.
    """
    return super(DfaClient, self)._LoadAuthCredentials()

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in dfa_api_auth.pkl.

    Args:
      key: str Key to update.
      new_value: str New value to update the key with.
    """
    super(DfaClient, self)._WriteUpdatedAuthValue(key, new_value)

  def __LoadConfigValues(self):
    """Load existing configuration values from dfa_api_config.pkl.

    Returns:
      dict Dictionary object with populated configuration values.
    """
    return super(DfaClient, self)._LoadConfigValues()

  def __SetMissingDefaultConfigValues(self, config={}):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict Object with client configuration values.
    """
    config = super(DfaClient, self)._SetMissingDefaultConfigValues(config)

    # Ensure that the 'force_data_inject' value is set for the DFA library to
    # function properly.
    self._config['force_data_inject'] = 'y'
    # TODO(api.jdilallo) Remove the following line once ZSI support is added.
    self._config['soap_lib'] = SOAPPY

    default_config = {
        'home': DfaClient.home,
        'log_home': os.path.join(DfaClient.home, 'logs')
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]
    return config

  def __SetAuthToken(self, server, version, http_proxy):
    """Return auth token.

    Args:
      server: str API server to access for this API call.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      dict Authentiaction credentials.
    """
    # Load/set authentication token.
    try:
      if (self._headers and 'AuthToken' in self._headers and
          self._headers['AuthToken']):
        self._headers['AuthToken'] = self._headers['AuthToken']
      elif 'Username' in self._headers and 'Password' in self._headers:
        self._headers['AuthToken'] = self.GetLoginService(
            server, version, http_proxy).Authenticate(
                self._headers['Username'],
                self._headers['Password'])[0]['token']
      else:
        msg = 'Authentication data, username or/and password, is missing.'
        raise ValidationError(msg)
    except AuthTokenError:
      # We would end up here if non-valid DFA Account's credentials were
      # specified.
      self._headers['AuthToken'] = None

  def CallRawMethod(self, soap_message, url, server, http_proxy):
    """Call API method directly, using raw SOAP message.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      soap_message: str SOAP XML message.
      url: str URL of the API service for the method to call.
      server: str API server to access for this API call.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple Response from the API method (SOAP XML response message).
    """
    headers = self._headers

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
        'http_proxy': http_proxy,
        'server': server
    }

    service = DfaWebService(headers, self._config, op_config, url,
                            self.__lock, self.__logger)
    return service.CallRawMethod(soap_message)

  def GetAdService(self, server='http://advertisersapi.doubleclick.net',
                   version=None, http_proxy=None):
    """Call API method in AdRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdRemoteService New instance of AdRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return AdRemoteService(headers, self._config, op_config, self.__lock,
                           self.__logger)

  def GetAdvertiserService(self, server='http://advertisersapi.doubleclick.net',
                           version=None, http_proxy=None):
    """Call API method in AdvertiserRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdvertiserRemoteService New instance of AdvertiserRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return AdvertiserRemoteService(headers, self._config, op_config,
                                   self.__lock, self.__logger)

  def GetAdvertiserGroupService(self,
                                server='http://advertisersapi.doubleclick.net',
                                version=None, http_proxy=None):
    """Call API method in AdvertiserGroupRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdvertiserGroupRemoteService New instance of AdvertiserGroupRemoteService
                                   object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return AdvertiserGroupRemoteService(headers, self._config, op_config,
                                        self.__lock, self.__logger)

  def GetCampaignService(self, server='http://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Call API method in CampaignRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CampaignRemoteService New instance of CampaignRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CampaignRemoteService(headers, self._config, op_config, self.__lock,
                                 self.__logger)

  def GetChangeLogService(self, server='http://advertisersapi.doubleclick.net',
                          version=None, http_proxy=None):
    """Call API method in ChangeLogRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ChangeLogRemoteService New instance of ChangeLogRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return ChangeLogRemoteService(headers, self._config, op_config, self.__lock,
                                  self.__logger)

  def GetContentCategoryService(self,
                                server='http://advertisersapi.doubleclick.net',
                                version=None, http_proxy=None):
    """Call API method in ContentCategoryRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ContentCategoryRemoteService New instance of ContentCategoryRemoteService
                                   object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return ContentCategoryRemoteService(headers, self._config, op_config,
                                        self.__lock, self.__logger)

  def GetCreativeService(self, server='http://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Call API method in CreativeRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CreativeRemoteService New instance of CreativeRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CreativeRemoteService(headers, self._config, op_config, self.__lock,
                                 self.__logger)

  def GetCreativeFieldService(self,
                              server='http://advertisersapi.doubleclick.net',
                              version=None, http_proxy=None):
    """Call API method in CreativeFieldRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CreativeFieldRemoteService New instance of CreativeFieldRemoteService
                                 object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CreativeFieldRemoteService(headers, self._config, op_config,
                                      self.__lock, self.__logger)

  def GetCreativeGroupService(self,
                              server='http://advertisersapi.doubleclick.net',
                              version=None, http_proxy=None):
    """Call API method in CreativeGroupRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CreativeGroupRemoteService New instance of CreativeGroupRemoteService
                                 object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return CreativeGroupRemoteService(headers, self._config, op_config,
                                      self.__lock, self.__logger)

  def GetLoginService(self, server='http://advertisersapi.doubleclick.net',
                      version=None, http_proxy=None):
    """Call API method in LoginRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      LoginRemoteService New instance of LoginRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    self._config['wsse'] = 'n'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return LoginRemoteService(headers, self._config, op_config, self.__lock,
                              self.__logger)

  def GetNetworkService(self, server='http://advertisersapi.doubleclick.net',
                        version=None, http_proxy=None):
    """Call API method in NetworkRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      NetworkRemoteService New instance of NetworkRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return NetworkRemoteService(headers, self._config, op_config, self.__lock,
                                self.__logger)

  def GetPlacementService(self, server='http://advertisersapi.doubleclick.net',
                          version=None, http_proxy=None):
    """Call API method in PlacementRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      PlacementRemoteService New instance of PlacementRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return PlacementRemoteService(headers, self._config, op_config, self.__lock,
                                  self.__logger)

  def GetReportService(self, server='http://advertisersapi.doubleclick.net',
                       version=None, http_proxy=None):
    """Call API method in ReportRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ReportingRemoteService New instance of ReportRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return ReportRemoteService(headers, self._config, op_config, self.__lock,
                               self.__logger)

  def GetSiteService(self, server='http://advertisersapi.doubleclick.net',
                      version=None, http_proxy=None):
    """Call API method in SiteRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      SiteRemoteService New instance of SiteRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return SiteRemoteService(headers, self._config, op_config, self.__lock,
                             self.__logger)

  def GetSizeService(self, server='http://advertisersapi.doubleclick.net',
                     version=None, http_proxy=None):
    """Call API method in SizeRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      SizeRemoteService New instance of SizeRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return SizeRemoteService(headers, self._config, op_config, self.__lock,
                             self.__logger)

  def GetSpotlightService(self, server='http://advertisersapi.doubleclick.net',
                          version=None, http_proxy=None):
    """Call API method in SpotlightRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      SpotlightRemoteService New instance of SpotlightRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return SpotlightRemoteService(headers, self._config, op_config, self.__lock,
                                  self.__logger)

  def GetStrategyService(self, server='http://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Call API method in StrategyRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      StrategyRemoteService New instance of StrategyRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return StrategyRemoteService(headers, self._config, op_config, self.__lock,
                                 self.__logger)

  def GetSubnetworkService(self, server='http://advertisersapi.doubleclick.net',
                           version=None, http_proxy=None):
    """Call API method in SubnetworkRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      SubnetworkRemoteService New instance of SubnetworkRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return SubnetworkRemoteService(headers, self._config, op_config,
                                   self.__lock, self.__logger)

  def GetUserService(self, server='http://advertisersapi.doubleclick.net',
                     version=None, http_proxy=None):
    """Call API method in UserRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      UserRemoteService New instance of UserRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return UserRemoteService(headers, self._config, op_config, self.__lock,
                             self.__logger)

  def GetUserRoleService(self, server='http://advertisersapi.doubleclick.net',
                         version=None, http_proxy=None):
    """Call API method in UserRoleRemoteService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'http://advertisersapi.doubleclick.net' for production
              site, 'http://advertisersapitest.doubleclick.net' for test, and
              'http://betaadvertisersapi.doubleclick.net' for beta. The default
              behavior is to access production site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      UserRoleRemoteService New instance of UserRoleRemoteService object.
    """
    headers = self._headers

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfaSanityCheck.ValidateServer(server, version)

    self.__SetAuthToken(server, version, http_proxy)

    # Load additional configuration data.
    self._config['wsse'] = 'y'
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }
    return UserRoleRemoteService(headers, self._config, op_config, self.__lock,
                                 self.__logger)
