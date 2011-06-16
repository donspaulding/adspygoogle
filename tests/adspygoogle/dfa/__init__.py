#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Settings and configuration for the unit tests."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.dfa.DfaClient import DfaClient


HTTP_PROXY = None
TEST_VERSION_V1_12 = False
SERVER_V1_12 = 'http://advertisersapitest.doubleclick.net'
VERSION_V1_12 = 'v1.12'
TEST_VERSION_V1_13 = True
SERVER_V1_13 = 'http://advertisersapitest.doubleclick.net'
VERSION_V1_13 = 'v1.13'
TEST_VERSION_V1_14 = True
SERVER_V1_14 = 'http://advertisersapitest.doubleclick.net'
VERSION_V1_14 = 'v1.14'
client = DfaClient(path=os.path.join('..', '..', '..'))
client.soap_lib = SOAPPY
