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

"""Script to auto generate client interface code from WSDL definitions."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))

from scripts.adspygoogle.common import wsdl_auto_obj
from scripts.adspygoogle.dfa import API_TARGETS


def DfaWsdlToUrl(wsdl_info, service):
  return '/'.join([wsdl_info['server'], wsdl_info['version'], 'api/dfa-api',
                   service + '?wsdl'])


# Generate WSDL definitions pickle.
print 'Generating WSDL definitions pickle...'
pickle_location = os.path.join('..', '..', '..', 'adspygoogle', 'dfa', 'data')
types_filename = 'wsdl_type_defs.pkl'
operation_filename = 'wsdl_ops_defs.pkl'

wsdl_auto_obj.GenPickles(pickle_location, types_filename, operation_filename,
                         API_TARGETS, DfaWsdlToUrl)

print '... done.'
