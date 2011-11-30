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
import re
import thread
import time

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Client import Client
from adspygoogle.common.Errors import AuthTokenError
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.Logger import Logger
from adspygoogle.dfp import AUTH_TOKEN_SERVICE
from adspygoogle.dfp import DEFAULT_API_VERSION
from adspygoogle.dfp import DfpSanityCheck
from adspygoogle.dfp import LIB_SHORT_NAME
from adspygoogle.dfp import LIB_SIG
from adspygoogle.dfp import REQUIRED_SOAP_HEADERS
from adspygoogle.dfp.GenericDfpService import GenericDfpService


class DfpClient(Client):

  """Provides entry point to all web services.

  Allows instantiation of all DFP API web services.
  """

  auth_pkl_name = 'dfp_api_auth.pkl'
  config_pkl_name = 'dfp_api_config.pkl'

  def __init__(self, headers=None, config=None, path=None):
    """Inits Client.

    Args:
      [optional]
      headers: dict Object with populated authentication credentials.
      config: dict Object with client configuration values.
      path: str Relative or absolute path to home directory (i.e. location of
            pickles and logs/).

    Example:
      headers = {
        'email': 'johndoe@example.com',
        'password': 'secret',
        'authToken': '...',
        'applicationName': 'GoogleTest',
        'networkCode': 'ca-01234567',
      }
      config = {
        'home': '/path/to/home',
        'log_home': '/path/to/logs/home',
        'proxy': 'http://example.com:8080',
        'xml_parser': PYXML,
        'debug': 'n',
        'raw_debug': 'n',
        'xml_log': 'y',
        'request_log': 'y',
        'raw_response': 'n',
        'strict': 'y',
        'pretty_xml': 'y',
        'compress': 'y',
        'access': ''
      }
      path = '/path/to/home'
    """
    super(DfpClient, self).__init__(headers, config, path)

    self.__lock = thread.allocate_lock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of DfpClient, based on
      # provided relative path.
      if os.path.isabs(path):
        DfpClient.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to DfpClient.home. Otherwise, may break when
        # multiple instances of DfpClient exist during program run.
        DfpClient.home = os.path.join(os.getcwd(), path)

      # If pickles don't exist at given location, default to "~".
      if (not headers and not config and
          (not os.path.exists(os.path.join(DfpClient.home,
                                           DfpClient.auth_pkl_name)) or
           not os.path.exists(os.path.join(DfpClient.home,
                                           DfpClient.config_pkl_name)))):
        DfpClient.home = os.path.expanduser('~')
    else:
      DfpClient.home = os.path.expanduser('~')

    # Update location for both pickles.
    DfpClient.auth_pkl = os.path.join(DfpClient.home,
                                      DfpClient.auth_pkl_name)
    DfpClient.config_pkl = os.path.join(DfpClient.home,
                                        DfpClient.config_pkl_name)

    # Only load from the pickle if config wasn't specified.
    self._config = config or self.__LoadConfigValues()
    self._config = self.__SetMissingDefaultConfigValues(self._config)
    self._config['home'] = DfpClient.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self._config['xml_parser'])

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self._headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self._config['strict']):
        SanityCheck.ValidateRequiredHeaders(headers, REQUIRED_SOAP_HEADERS)
      self._headers = headers

    # Load/set authentication token.
    try:
      if headers and 'authToken' in headers and headers['authToken']:
        self._headers['authToken'] = headers['authToken']
      elif 'email' in self._headers and 'password' in self._headers:
        self._headers['authToken'] = Utils.GetAuthToken(
            self._headers['email'], self._headers['password'],
            AUTH_TOKEN_SERVICE, LIB_SIG, self._config['proxy'])
      else:
        msg = 'Authentication data, email or/and password, is missing.'
        raise ValidationError(msg)
      self._config['auth_token_epoch'] = time.time()
    except AuthTokenError:
      # We would end up here if non-valid Google Account's credentials were
      # specified.
      self._headers['authToken'] = None
      self._config['auth_token_epoch'] = 0

    # Insert library's signature into application name.
    if self._headers['applicationName'].rfind(LIB_SIG) == -1:
      # Make sure library name shows up only once.
      if self._headers['applicationName'].rfind(LIB_SHORT_NAME) > -1:
        pattern = re.compile('.*\|')
        self._headers['applicationName'] = pattern.sub(
            '', self._headers['applicationName'], 1)
      self._headers['applicationName'] = (
          '%s|%s' % (LIB_SIG, self._headers['applicationName']))

      # Sync library's version in the new application name with the one in the
      # pickle.
      if headers is None:
        self.__WriteUpdatedAuthValue('applicationName',
                                     self._headers['applicationName'])

    # Initialize logger.
    self.__logger = Logger(LIB_SIG, self._config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from dfp_api_auth.pkl.

    Returns:
      dict Dictionary object with populated authentication credentials.
    """
    return super(DfpClient, self)._LoadAuthCredentials()

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in dfp_api_auth.pkl.

    Args:
      key: str Key to update.
      new_value: str New value to update the key with.
    """
    super(DfpClient, self)._WriteUpdatedAuthValue(key, new_value)

  def __LoadConfigValues(self):
    """Load existing configuration values from dfp_api_config.pkl.

    Returns:
      dict Dictionary object with populated configuration values.
    """
    return super(DfpClient, self)._LoadConfigValues()

  def __SetMissingDefaultConfigValues(self, config=None):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict Object with client configuration values.

    Returns:
      dict The config dictionary with default values added.
    """
    if config is None: config = {}
    config = super(DfpClient, self)._SetMissingDefaultConfigValues(config)
    default_config = {
        'home': DfpClient.home,
        'log_home': os.path.join(DfpClient.home, 'logs')
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]
    return config

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
    service_name = url.split('/')[-1]
    service = getattr(self, 'Get' + service_name)(server=server,
                                                  http_proxy=http_proxy)
    return service.CallRawMethod(soap_message)

  def GetCompanyService(self, server='https://sandbox.google.com', version=None,
                        http_proxy=None):
    """Call API method in CompanyService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of CompanyService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'CompanyService')

  def GetContentService(self, server='https://sandbox.google.com', version=None,
                        http_proxy=None):
    """Call API method in ContentService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of ContentService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'ContentService')

  def GetCreativeService(self, server='https://sandbox.google.com',
                         version=None, http_proxy=None):
    """Call API method in CreativeService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of CreativeService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'CreativeService')

  def GetCreativeTemplateService(self, server='https://sandbox.google.com',
                                 version=None, http_proxy=None):
    """Call API method in CreativeTemplateService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of CreativeTemplateService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger,
                             'CreativeTemplateService')

  def GetCustomTargetingService(self, server='https://sandbox.google.com',
                                version=None, http_proxy=None):
    """Call API method in CustomTargetingService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of CustomTargetingService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger,
                             'CustomTargetingService')

  def GetForecastService(self, server='https://sandbox.google.com',
                         version=None, http_proxy=None):
    """Call API method in ForecastService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of ForecastService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'ForecastService')

  def GetInventoryService(self, server='https://sandbox.google.com',
                          version=None, http_proxy=None):
    """Call API method in InventoryService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of InventoryService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'InventoryService')

  def GetLabelService(self, server='https://sandbox.google.com',
                      version=None, http_proxy=None):
    """Call API method in LineItemCreativeAssociationService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of LabelService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'LabelService')

  def GetLineItemCreativeAssociationService(self,
                                            server='https://sandbox.google.com',
                                            version=None, http_proxy=None):
    """Call API method in LineItemCreativeAssociationService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of LineItemCreativeAssociationService
                        object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger,
                             'LineItemCreativeAssociationService')

  def GetLineItemService(self, server='https://sandbox.google.com',
                         version=None, http_proxy=None):
    """Call API method in LineItemService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of LineItemService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'LineItemService')

  def GetNetworkService(self, server='https://sandbox.google.com', version=None,
                        http_proxy=None):
    """Call API method in NetworkService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of NetworkService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'NetworkService')

  def GetOrderService(self, server='https://sandbox.google.com', version=None,
                      http_proxy=None):
    """Call API method in OrderService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of OrderService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'OrderService')

  def GetPlacementService(self, server='https://sandbox.google.com',
                          version=None, http_proxy=None):
    """Call API method in PlacementService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of PlacementService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'PlacementService')

  def GetPublisherQueryLanguageService(self,
                                       server='https://sandbox.google.com',
                                       version=None, http_proxy=None):
    """Call API method in PublisherQueryLanguageService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of PublisherQueryLanguageService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger,
                             'PublisherQueryLanguageService')

  def GetReportService(self, server='https://sandbox.google.com',
                       version=None, http_proxy=None):
    """Call API method in ReportService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of ReportService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'ReportService')

  def GetSuggestedAdUnitService(self, server='https://sandbox.google.com',
                                version=None, http_proxy=None):
    """Call API method in SuggestedAdUnitService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of SuggestedAdUnitService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger,
                             'SuggestedAdUnitService')

  def GetUserService(self, server='https://sandbox.google.com', version=None,
                     http_proxy=None):
    """Call API method in UserService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible values
              are: 'https://www.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior is
              to access sandbox site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericDfpService New instance of UserService object.
    """
    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      DfpSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericDfpService(self._headers, self._config, op_config,
                             self.__lock, self.__logger, 'UserService')
