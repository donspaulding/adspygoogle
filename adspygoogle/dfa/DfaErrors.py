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

"""Classes for handling errors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common.Errors import DetailError
from adspygoogle.common.Errors import Error


class DfaError(Error):

  """Implements DfaError.

  Responsible for handling error.
  """

  def __init(self, msg):
    super(DfaError, self).__init__()

  def __str__(self):
    return super(DfaError, self).__str__()

  def __call__(self):
    return super(DfaError, self).__call__()


class DfaDetailError(DetailError):

  """Implements DfaDetailError.

  Responsible for handling detailed ApiException error.
  """

  def __init__(self, **error):
    super(DfaDetailError, self).__init__()
    self.__error = error
    for key in self.__error:
      self.__dict__.__setitem__(key, self.__error[key])

  def __call__(self):
    return (self.__error,)


class DfaApiError(DfaError):

  """Implements DfaApiError.

  Responsible for handling API exception.
  """

  def __init__(self, fault):
    (self.__fault, self.fault_code, self.fault_string) = (fault, '', '')
    if 'faultcode' in fault: self.fault_code = fault['faultcode']
    if 'faultstring' in fault: self.fault_string = fault['faultstring']

    (self.code, self.error_message, self.localized_message, self.message,
     self.hostname) = (-1, '', '', '', '')
    if 'detail' in fault and 'doubleclick' in fault['detail']:
      if 'errorCode' in fault['detail']['doubleclick']:
        self.code = int(fault['detail']['doubleclick']['errorCode'])
      if 'errorMessage' in fault['detail']['doubleclick']:
        self.error_message = fault['detail']['doubleclick']['errorMessage']
      if 'localizedMessage' in fault['detail']['doubleclick']:
        self.localized_message = \
            fault['detail']['doubleclick']['localizedMessage']
      if 'message' in fault['detail']['doubleclick']:
        self.message = fault['detail']['doubleclick']['message']
      if 'hostname' in fault['detail']:
        self.hostname = fault['detail']['hostname']
    if not self.message: self.message = self.fault_string

  def __str__(self):
    if self.code > -1:
      return 'Code %s: %s' % (self.code, self.message)
    else:
      return self.fault_string

  def __call__(self):
    return (self.__fault,)


class DfaRequestError(DfaApiError):

  """Implements DfaRequestError.

  Responsible for handling request error."""

  pass


class DfaGoogleInternalError(DfaApiError):

  """Implements DfaGoogleInternalError.

  Responsible for handling Google internal error.
  """

  pass


class DfaAuthenticationError(DfaApiError):

  """Implements DfaAuthenticationError.

  Responsible for handling authentication error.
  """

  pass


class DfaAccountError(DfaApiError):

  """Implements DfaAccountError.

  Responsible for handling account error.
  """

  pass


# Map error codes to their corresponding classes.
ERRORS = {}
ERROR_CODES = [x for x in xrange(0, 200005)]
for index in ERROR_CODES:
  if (index == 2 or index == 3 or (index >= 13 and index <= 26) or
      (index >= 33 and index <= 14019) or (index >= 14023 and index <= 64024) or
      (index >= 64100 and index <= 200005)):
    ERRORS[index] = DfaRequestError
  elif (index == 1 or index == 6 or index == 10):
    ERRORS[index] = DfaGoogleInternalError
  elif ((index >= 14020 and index <= 14022) or index == 64025):
    ERRORS[index] = DfaAccountError
  elif (index == 4 or index == 5 or index == 7 or
        (index >= 27 and index <= 32)):
    ERRORS[index] = DfaAuthenticationError
