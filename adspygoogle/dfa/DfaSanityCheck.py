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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfa import API_VERSIONS_MAP


def ValidateServer(server, version):
  """Sanity check for API server.

  Args:
    server: str API server to access for this API call.
    version: str API version being used to access the server.
  """
  # Map of supported API servers and versions.
  prod = {'v1.13': 'http://advertisersapi.doubleclick.net',
          'v1.14': 'http://advertisersapi.doubleclick.net',
          'v1.15': 'http://advertisersapi.doubleclick.net'}
  beta = {'v1.13': 'http://betaadvertisersapi.doubleclick.net',
          'v1.14': 'http://betaadvertisersapi.doubleclick.net',
          'v1.15': 'http://betaadvertisersapi.doubleclick.net'}
  test = {'v1.13': 'http://advertisersapitest.doubleclick.net',
          'v1.14': 'http://advertisersapitest.doubleclick.net',
          'v1.15': 'http://advertisersapitest.doubleclick.net'}

  if (server not in prod.values() and server not in beta.values() and
      server not in test.values()):
    msg = ('Given API server, \'%s\', is not valid. Expecting one of %s.'
           % (server,
              sorted(prod.values() + beta.values() + test.values())[1:]))
    raise ValidationError(msg)

  if (version not in prod.keys() and version not in beta.keys() and
      version not in test.keys()):
    msg = ('Given API version, \'%s\', is not valid. Expecting one of %s.'
           % (version, sorted(set(prod.keys() + beta.keys() + test.keys()))))
    raise ValidationError(msg)

  if (server != prod[version] and server != beta[version] and
      server != test[version]):
    msg = ('Given API version, \'%s\', is not compatible with given server, '
           '\'%s\'.' % (version, server))
    raise ValidationError(msg)


def IsJaxbApi(version):
  """Check if request is being made against API that used JAXB.

  Args:
    version: str Version of the API being used.

  Returns:
    bool True if request is made against an API that used JAXB, False otherwise.
  """
  valid_versions = []
  for api_version, is_jaxb in API_VERSIONS_MAP:
    valid_versions.append(api_version)
    if api_version == version:
      return is_jaxb
  msg = ('Given API version, \'%s\' is not valid. Expecting one of %s.'
         % (version, valid_versions))
  raise ValidationError(msg)
