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

"""Handy utility functions."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os

from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfa import LIB_HOME


def GetErrorCodes():
  """Get a list of available error codes.

  Returns:
    list Available error codes.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'error_codes.csv'))


def GetAdXsiTypes():
  """Gets a dictionary of ad xsi_types indexed by their 'typeId' values.

  Returns:
    dict Ad xsi_types indexed by 'typeId'.
  """
  return Utils.GetDictFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'ad_types.csv'))


def GetCreativeXsiTypes():
  """Gets a dictionary of creative xsi_types indexed by their 'typeId' values.

  Returns:
    dict Creative xsi_types indexed by 'typeId'.
  """
  return Utils.GetDictFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'creative_types.csv'))


def TransformDates(obj):
  """Transforms tuple-represented dates within the given object to strings.

  Args:
    obj: dict The object whose dates need to all be strings.
  """
  for key in obj:
    if key in ('startDate', 'startTime', 'endDate', 'endTime'):
      if isinstance(obj[key], tuple):
        if len(obj[key]) == 6:
          obj[key] = '%04s-%02d-%02dT%02d:%02d:%02d' % (
              obj[key][0], obj[key][1], obj[key][2], obj[key][3],
              obj[key][4], obj[key][5])
        else:
          raise ValidationError('The date in field %s is malformed.' % key)


def AssignAdXsi(ad):
  """Assigns an xsi type to an Ad object if one is not present.

  Args:
    ad: dict Ad object.

  Raises:
    ValidationError: The ad object is lacking enough information to determine
                     what concrete class it represents.
  """
  if 'xsi_type' not in ad:
    if 'typeId' in ad:
      ad['xsi_type'] = GetAdXsiTypes()[ad['typeId']]
    else:
      raise ValidationError('The type of the ad is missing.')


def AssignCreativeXsi(creative):
  """Assigns an xsi type to a creative object if one is not present.

  Args:
    creative: dict CreativeBase object.

  Raises:
    ValidationError: The creative object is lacking enough information to
                     determine what concrete class it represents.
  """
  if 'xsi_type' not in creative:
    if 'typeId' in creative:
      creative['xsi_type'] = GetCreativeXsiTypes()[creative['typeId']]
    else:
      raise ValidationError('The type of the creative is missing.')
