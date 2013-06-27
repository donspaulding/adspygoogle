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

"""Script to configure DFA API Python client library."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle


from adspygoogle.dfa import REQUIRED_SOAP_HEADERS
from adspygoogle.common import SanityCheck
from adspygoogle.common.Errors import InvalidInputError
from adspygoogle.common.Logger import Logger


HOME = os.path.expanduser('~')
AUTH_PKL = os.path.join(HOME, 'dfa_api_auth.pkl')
CONFIG_PKL = os.path.join(HOME, 'dfa_api_config.pkl')
LOG_HOME = os.path.join(HOME, 'logs')
LOG_NAME = 'dfa_api_lib'


logger = Logger(os.path.join(LOG_HOME))

# Load existing authentication credentials from dfa_api_auth.pkl.
old_auth = {}
if os.path.exists(AUTH_PKL):
  try:
    fh = open(AUTH_PKL, 'r')
    try:
      old_auth = pickle.load(fh)
    finally:
      fh.close()
  except IOError, e:
    logger.Log(LOG_NAME, e, log_level=Logger.ERROR)

# Prompt user for authentication and configuration values.
print """
--~--~---------~--~----~------------~-------~--~----~
All requests to the non-LoginService that are sent to
the DFA API web services must include SOAP header
elements. Currently accepted header elements are
Username and OAuth 2.0 access token. We use clientId,
clientSecret, and refreshToken to enable this feature.

To overwrite an existing header element, explicitly
type new value (or 'none' to clear) at the prompt.
The default behavior is to keep old values.
-~----------~----~----~----~------~----~------~--~---\n"""
prompts = (('Your DFA account\'s username', 'Username',
            'auth'),
           ('OAuth 2.0 client ID (retrieved from '
            'code.google.com/apis/console under the API Access tab)',
            'clientId', 'auth'),
           ('OAuth 2.0 client secret (retrieved from '
            'code.google.com/apis/console under the API Access tab)',
            'clientSecret', 'auth'),
           ('OAuth 2.0 refresh token (if you don\'t already have one, run '
            'scripts/common/generate_refresh_token.py', 'refreshToken', 'auth'),
           ('Select XML parser [1=PyXML (recommended), 2=ElementTree]',
            'xml_parser', 'config'),
           ('Enable debugging mode', 'debug', 'config'),
           ('Enable SOAP XML logging mode', 'xml_log', 'config'),
           ('Enable API request logging mode', 'request_log', 'config'),
           ('Enter an application name', 'app_name', 'config'))
auth = {}
config = {
    'home': HOME,
    'log_home': LOG_HOME
}
for prompt_msg, header, source in prompts:
  if source == 'auth':
    # Construct prompt message.
    try:
      prompt_msg = '%s [%s]: ' % (prompt_msg, old_auth[header])
    except (NameError, KeyError), e:
      prompt_msg = '%s: ' % prompt_msg

    # Prompt user to keep/update authentication credentials.
    auth[header] = raw_input(prompt_msg).rstrip('\r')
    if header in old_auth:
      if auth[header] == 'none':
        auth[header] = ''
      elif not auth[header]:
        auth[header] = old_auth[header]
    else:
      if auth[header] == 'none':
        auth[header] = ''
  elif source == 'config':
    # Prompt user to update configuration values.
    if header == 'xml_parser':
      res = raw_input('%s: ' % prompt_msg).rstrip('\r')
      if not SanityCheck.IsConfigUserInputValid(res, ['1', '2']):
        msg = 'Possible values are \'1\' or \'2\'.'
        raise InvalidInputError(msg)
    elif header == 'app_name':
      res = raw_input('%s : ' % prompt_msg).rstrip('\r')
    else:
      res = raw_input('%s [y/n]: ' % prompt_msg).rstrip('\r')
      if not SanityCheck.IsConfigUserInputValid(res, ['y', 'n']):
        msg = 'Possible values are \'y\' or \'n\'.'
        raise InvalidInputError(msg)
    config[header] = res

# Raise an exception, if required headers are missing.
SanityCheck.ValidateRequiredHeaders(auth, REQUIRED_SOAP_HEADERS)

# Load new authentication credentials into dfa_api_auth.pkl.
try:
  fh = open(AUTH_PKL, 'w')
  try:
    pickle.dump(auth, fh)
  finally:
    fh.close()
except IOError, e:
  logger.Log(LOG_NAME, e, log_level=Logger.ERROR)

# Load new configuratation values into dfa_api_config.pkl.
try:
  fh = open(CONFIG_PKL, 'w')
  try:
    pickle.dump(config, fh)
  finally:
    fh.close()
except IOError, e:
  logger.Log(LOG_NAME, e, log_level=Logger.ERROR)
