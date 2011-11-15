#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.adwords import AUTH_TOKEN_SERVICE
from adspygoogle.adwords import DEFAULT_API_VERSION
from adspygoogle.adwords import LIB_SHORT_NAME
from adspygoogle.adwords import LIB_SIG
from adspygoogle.adwords import REQUIRED_SOAP_HEADERS
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.GenericAdWordsService import GenericAdWordsService
from adspygoogle.adwords.GenericV13AdWordsService import GenericV13AdWordsService
from adspygoogle.adwords.ReportDownloader import ReportDownloader
from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Client import Client
from adspygoogle.common.Errors import AuthTokenError
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.Logger import Logger


# Minimum version to support TrafficEstimatorService for.
TES_MIN_VER = 'v201008'

class AdWordsClient(Client):

  """Provides entry point to all web services.

  Allows instantiation of all AdWords API web services.
  """

  auth_pkl_name = 'adwords_api_auth.pkl'
  config_pkl_name = 'adwords_api_config.pkl'

  def __init__(self, headers=None, config=None, path=None):
    """Inits AdWordsClient.

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
        'clientEmail': 'client_1+johndoe@example.com',
        'clientCustomerId': '1234567890',
        'userAgent': 'GoogleTest',
        'developerToken': 'johndoe@example.com++USD',
        'validateOnly': 'n',
        'partialFailure': 'n'
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
    super(AdWordsClient, self).__init__(headers, config, path)

    self.__lock = thread.allocate_lock()
    self.__loc = None

    if path is not None:
      # Update absolute path for a given instance of AdWordsClient, based on
      # provided relative path.
      if os.path.isabs(path):
        AdWordsClient.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to AdWordsClient.home. Otherwise, may break when
        # multiple instances of AdWordsClient exist during program run.
        AdWordsClient.home = os.path.join(os.getcwd(), path)

      # If pickles don't exist at given location, default to "~".
      if (not headers and not config and
          (not os.path.exists(os.path.join(AdWordsClient.home,
                                           AdWordsClient.auth_pkl_name)) or
           not os.path.exists(os.path.join(AdWordsClient.home,
                                           AdWordsClient.config_pkl_name)))):
        AdWordsClient.home = os.path.expanduser('~')
    else:
      AdWordsClient.home = os.path.expanduser('~')

    # Update location for both pickles.
    AdWordsClient.auth_pkl = os.path.join(AdWordsClient.home,
                                          AdWordsClient.auth_pkl_name)
    AdWordsClient.config_pkl = os.path.join(AdWordsClient.home,
                                            AdWordsClient.config_pkl_name)

    # Only load from the pickle if config wasn't specified.
    self._config = config or self.__LoadConfigValues()
    self._config = self.__SetMissingDefaultConfigValues(self._config)
    self._config['home'] = AdWordsClient.home

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self._config['xml_parser'])

    # Initialize units and operations for current instance of AdWordsClient
    # object (using list to take advantage of Python's pass-by-reference).
    self._config['units'] = [0]
    self._config['operations'] = [0]
    self._config['last_units'] = [0]
    self._config['last_operations'] = [0]

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self._headers = self.__LoadAuthCredentials()
    else:
      if Utils.BoolTypeConvert(self._config['strict']):
        SanityCheck.ValidateRequiredHeaders(headers, REQUIRED_SOAP_HEADERS)
      self._headers = headers

    # Internally, store user agent as 'userAgent'.
    if 'useragent' in self._headers:
      self._headers['userAgent'] = self._headers['useragent']
      self._headers = Utils.UnLoadDictKeys(self._headers, ['useragent'])
    if Utils.BoolTypeConvert(self._config['strict']):
      SanityCheck.ValidateRequiredHeaders(self._headers,
                                          REQUIRED_SOAP_HEADERS)

    # Load validateOnly header, if one was set.
    if 'validateOnly' in self._headers:
      self._headers['validateOnly'] = str(Utils.BoolTypeConvert(
          self._headers['validateOnly']))

    # Load partialFailure header, if one was set.
    if 'partialFailure' in self._headers:
      self._headers['partialFailure'] = str(Utils.BoolTypeConvert(
          self._headers['partialFailure']))

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

    # Insert library's signature into user agent.
    if self._headers['userAgent'].rfind(LIB_SIG) == -1:
      # Make sure library name shows up only once.
      if self._headers['userAgent'].rfind(LIB_SHORT_NAME) > -1:
        pattern = re.compile('.*\|')
        self._headers['userAgent'] = pattern.sub(
            '', self._headers['userAgent'], 1)
      self._headers['userAgent'] = (
          '%s|%s' % (LIB_SIG, self._headers['userAgent']))

      # Sync library's version in the new user agent with the one in the pickle.
      if headers is None:
        self.__WriteUpdatedAuthValue('userAgent', self._headers['userAgent'])

    self.__is_mcc = False

    # Initialize logger.
    self.__logger = Logger(LIB_SIG, self._config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from adwords_api_auth.pkl.

    Returns:
      dict Dictionary object with populated authentication credentials.
    """
    return super(AdWordsClient, self)._LoadAuthCredentials()

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in adwords_api_auth.pkl.

    Args:
      key: str Key to update.
      new_value: str New value to update the key with.
    """
    super(AdWordsClient, self)._WriteUpdatedAuthValue(key, new_value)

  def __LoadConfigValues(self):
    """Load existing configuration values from adwords_api_config.pkl.

    Returns:
      dict Dictionary object with populated configuration values.
    """
    return super(AdWordsClient, self)._LoadConfigValues()

  def __SetMissingDefaultConfigValues(self, config=None):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict Object with client configuration values.

    Returns:
      dict A config dictionary with default values set.
    """
    if config is None: config = {}
    config = super(AdWordsClient, self)._SetMissingDefaultConfigValues(config)
    default_config = {
        'home': AdWordsClient.home,
        'log_home': os.path.join(AdWordsClient.home, 'logs')
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]
    return config

  def GetUnits(self):
    """Return number of API units consumed by current instance of AdWordsClient
    object.

    Returns:
      int Number of API units.
    """
    return self._config['units'][0]

  def GetOperations(self):
    """Return number of API ops performed by current instance of AdWordsClient
    object.

    Returns:
      int Number of API operations.
    """
    return self._config['operations'][0]

  def GetLastUnits(self):
    """Return number of API units consumed by last API call.

    Returns:
      int Number of API units.
    """
    return self._config['last_units'][0]

  def GetLastOperations(self):
    """Return number of API ops performed by last API call.

    Returns:
      int Number of API operations.
    """
    return self._config['last_operations'][0]

  def UseMcc(self, state):
    """Choose to make an API request against MCC account or a sub-account.

    Args:
      state: bool State of the API request, whether to use MCC.
    """
    self.__is_mcc = False
    if state:
      self.__is_mcc = True

  def __GetUseMcc(self):
    """Return current state of the API request.

    Returns:
      bool State of the API request, whether to use MCC.
    """
    return self.__is_mcc

  def __SetUseMcc(self, state):
    """Chooses to make an API request against MCC account or a sub-account.

    Args:
      state: bool State of the API request, whether to use MCC.
    """
    self.__is_mcc = state

  use_mcc = property(__GetUseMcc, __SetUseMcc)

  def SetClientEmail(self, client_email):
    """Temporarily change client email for a given AdWordsClient instance.

    Args:
      client_email: str New client email to use.
    """
    if ('clientEmail' not in self._headers or
        self._headers['clientEmail'] != client_email):
      self._headers['clientEmail'] = client_email
      self._headers['clientCustomerId'] = ''

  def SetClientCustomerId(self, client_customer_id):
    """Temporarily change client customer id for a given AdWordsClient instance.

    Args:
      client_customer_id: str New client customer id to use.
    """
    if ('clientCustomerId' not in self._headers or
        self._headers['clientCustomerId'] != client_customer_id):
      self._headers['clientCustomerId'] = client_customer_id
      self._headers['clientEmail'] = ''

  def __GetValidateOnly(self):
    """Return current state of the validation mode.

    Returns:
      bool State of the validation mode.
    """
    return self._headers['validateOnly']

  def __SetValidateOnly(self, new_state):
    """Temporarily change validation mode for a given AdWordsClient instance.

    Args:
      new_state: bool New state of the validation mode.
    """
    self._headers['validateOnly'] = str(new_state)

  validate_only = property(__GetValidateOnly, __SetValidateOnly)

  def __GetPartialFailure(self):
    """Return current state of the partial failure mode.

    Returns:
      bool State of the partial failure mode.
    """
    return self._headers['partialFailure']

  def __SetPartialFailure(self, new_state):
    """Temporarily change partial failure mode for a given AdWordsClient
    instance.

    Args:
      new_state: bool New state of the partial failure mode.
    """
    self._headers['partialFailure'] = str(new_state)

  partial_failure = property(__GetPartialFailure, __SetPartialFailure)

  def __GetAuthCredentialsForAccessLevel(self):
    """Return auth credentials based on the access level of the request.

    Request can have an MCC level access or a sub account level access.

    Returns:
      dict Authentiaction credentials.
    """
    old_headers = self.GetAuthCredentials()
    new_headers = {}
    is_mcc = self.__is_mcc

    for key, value in old_headers.iteritems():
      new_headers[key] = value
      if key == 'clientEmail' or key == 'clientCustomerId':
        if is_mcc and 'email' in old_headers:
          new_headers[key] = None

    if (('clientEmail' in new_headers and 'clientCustomerId' in new_headers) and
        new_headers['clientEmail'] == new_headers['clientCustomerId']):
      new_headers['clientCustomerId'] = None
    return new_headers

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

  def GetAccountService(self, server='https://adwords.google.com', version=None,
                        http_proxy=None):
    """Call API method in AccountService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AccountService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = 'v13'
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericV13AdWordsService(headers, self._config, op_config,
                                    self.__lock, self.__logger,
                                    'AccountService')

  def GetAdExtensionOverrideService(self, server='https://adwords.google.com',
                                    version=None, http_proxy=None):
    """Call API method in AdExtensionOverrideService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AdExtensionOverrideService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'AdExtensionOverrideService')

  def GetAdGroupAdService(self, server='https://adwords.google.com',
                          version=None, http_proxy=None):
    """Call API method in AdGroupAdService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AdGroupAdService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'AdGroupAdService')

  def GetAdGroupCriterionService(self, server='https://adwords.google.com',
                                 version=None, http_proxy=None):
    """Call API method in AdGroupCriterionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AdGroupCriterionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'AdGroupCriterionService')

  def GetAdGroupService(self, server='https://adwords.google.com',
                        version=None, http_proxy=None):
    """Call API method in AdGroupService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AdGroupService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'AdGroupService')

  def GetAdParamService(self, server='https://adwords.google.com',
                        version=None, http_proxy=None):
    """Call API method in AdParamService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AdParamService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'AdParamService')

  def GetAlertService(self, server='https://adwords.google.com', version=None,
                      http_proxy=None):
    """Call API method in AlertService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of AlertService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'mcm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'AlertService')

  def GetBidLandscapeService(self, server='https://adwords.google.com',
                             version=None, http_proxy=None):
    """Call API method in BidLandscapeService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of BidLandscapeService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'BidLandscapeService')

  def GetBulkMutateJobService(self, server='https://adwords.google.com',
                              version=None, http_proxy=None):
    """Call API method in BulkMutateJobService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of BulkMutateJobService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'BulkMutateJobService')

  def GetMutateJobService(self, server='https://adwords.google.com',
                              version=None, http_proxy=None):
    """Call API method in MutateJobService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of BulkMutateJobService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'MutateJobService')

  def GetCampaignAdExtensionService(self, server='https://adwords.google.com',
                                    version=None, http_proxy=None):
    """Call API method in CampaignAdExtensionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of CampaignAdExtensionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'CampaignAdExtensionService')

  def GetCampaignCriterionService(self, server='https://adwords.google.com',
                                  version=None, http_proxy=None):
    """Call API method in CampaignCriterionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of CampaignCriterionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'CampaignCriterionService')

  def GetCampaignService(self, server='https://adwords.google.com',
                         version=None, http_proxy=None):
    """Call API method in CampaignService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of CampaignService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'CampaignService')

  def GetCampaignTargetService(self, server='https://adwords.google.com',
                               version=None, http_proxy=None):
    """Call API method in CampaignTargetService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of CampaignTargetService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'CampaignTargetService')

  def GetConstantDataService(self, server='https://adwords.google.com',
                             version=None, http_proxy=None):
    """Call API method in ConstantDataService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of ConstantDataService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'ConstantDataService')

  def GetCustomerSyncService(self, server='https://adwords.google.com',
                             version=None, http_proxy=None):
    """Call API method in CustomerSyncService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of CustomerSyncService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'ch',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'CustomerSyncService')

  def GetExperimentService(self, server='https://adwords.google.com',
                           version=None, http_proxy=None):
    """Call API method in ExperimentService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of ExperimentService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'ExperimentService')

  def GetGeoLocationService(self, server='https://adwords.google.com',
                            version=None, http_proxy=None):
    """Call API method in GeoLocationService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of GeoLocationService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'GeoLocationService')

  def GetInfoService(self, server='https://adwords.google.com', version=None,
                     http_proxy=None):
    """Call API method in InfoService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of InfoService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'info',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'InfoService')

  def GetLocationCriterionService(self, server='https://adwords.google.com',
                                  version=None, http_proxy=None):
    """Call API method in LocationCriterionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      LocationCriterionService New instance of LocationCriterionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'LocationCriterionService')

  def GetMediaService(self, server='https://adwords.google.com', version=None,
                      http_proxy=None):
    """Call API method in MediaService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of MediaService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'MediaService')

  def GetReportDefinitionService(self, server='https://adwords.google.com',
                                 version=None, http_proxy=None):
    """Call API method in ReportDefinitionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of ReportDefinitionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'ReportDefinitionService')

  def GetReportDownloader(self, server='https://adwords.google.com',
                          version=None, http_proxy=None):
    """Returns an instance of ReportDownloader, used to download reports.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ReportService New instance of ReportDownloader object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return ReportDownloader(headers, self._config, op_config)

  def GetReportService(self, server='https://adwords.google.com', version=None,
                       http_proxy=None):
    """Call API method in ReportService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of ReportService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = 'v13'
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'http_proxy': http_proxy
    }
    return GenericV13AdWordsService(headers, self._config, op_config,
                                    self.__lock, self.__logger, 'ReportService')

  def GetServicedAccountService(self, server='https://adwords.google.com',
                                version=None, http_proxy=None):
    """Call API method in ServicedAccountService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of ServicedAccountService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'mcm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'ServicedAccountService')

  def GetTargetingIdeaService(self, server='https://adwords.google.com',
                              version=None, http_proxy=None):
    """Call API method in TargetingIdeaService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of TargetingIdeaService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'o',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'TargetingIdeaService')

  def GetTrafficEstimatorService(self, server='https://adwords.google.com',
                                 version=None, http_proxy=None):
    """Call API method in TrafficEstimatorService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of TrafficEstimatorService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version < TES_MIN_VER:
      raise AdWordsError('TrafficEstimatorService is not available for %s.'
                         % version)

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'o',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'TrafficEstimatorService')

  def GetUserListService(self, server='https://adwords.google.com',
                         version=None, http_proxy=None):
    """Call API method in UserListService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of UserListService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'UserListService')

  def GetBulkOpportunityService(self, server='https://adwords.google.com',
                                version=None, http_proxy=None):
    """Call API method in BulkOpportunityService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of BulkOpportunityService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'o',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'BulkOpportunityService')

  def GetConversionTrackerService(self, server='https://adwords.google.com',
                                  version=None, http_proxy=None):
    """Call API method in ConversionTrackerService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of ConversionTrackerService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'ConversionTrackerService')

  def GetDataService(self, server='https://adwords.google.com',
                     version=None, http_proxy=None):
    """Call API method in DataService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GenericAdWordsService New instance of DataService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = DEFAULT_API_VERSION
    if Utils.BoolTypeConvert(self._config['strict']):
      AdWordsSanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
        'server': server,
        'version': version,
        'group': 'cm',
        'default_group': 'cm',
        'http_proxy': http_proxy
    }
    return GenericAdWordsService(headers, self._config, op_config, self.__lock,
                                 self.__logger, 'DataService')

  def _GetOAuthScope(self, server='https://adwords.google.com'):
    """Retrieves the OAuth Scope to use.

    Args:
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
    Returns:
      str Full scope to use for OAuth.
    """
    return server + '/api/adwords/'