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
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.dfa.DfaClient import DfaClient


HTTP_PROXY = None
TEST_VERSION_V1_14 = False
SERVER_V1_14 = 'http://advertisersapitest.doubleclick.net'
VERSION_V1_14 = 'v1.14'
TEST_VERSION_V1_15 = True
SERVER_V1_15 = 'http://advertisersapitest.doubleclick.net'
VERSION_V1_15 = 'v1.15'
TEST_VERSION_V1_16 = True
SERVER_V1_16 = 'http://advertisersapitest.doubleclick.net'
VERSION_V1_16 = 'v1.16'
client = DfaClient(path=os.path.join('..', '..', '..'))
