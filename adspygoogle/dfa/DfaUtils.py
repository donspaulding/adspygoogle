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

import math
import os

from adspygoogle.common import Utils
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
