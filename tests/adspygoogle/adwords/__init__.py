#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Settings and configuration for the unit tests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.adwords.AdWordsClient import AdWordsClient


HTTP_PROXY = None
SERVER_V201209 = 'https://adwords.google.com'
SERVER_V201302 = 'https://adwords.google.com'
SERVER_V201306 = 'https://adwords.google.com'
TEST_VERSION_V201209 = True
TEST_VERSION_V201302 = True
TEST_VERSION_V201306 = True
VERSION_V201209 = 'v201209'
VERSION_V201302 = 'v201302'
VERSION_V201306 = 'v201306'
client = AdWordsClient(path=os.path.join('..', '..', '..'))
