#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""Tests to cover AdWordsSanityCheck."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))
import unittest

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.common.Errors import ValidationError


class AdWordsSanityCheckTest(unittest.TestCase):
  """Tests for AdWordsSanityCheck."""

  def testValidateService_bmjsAllowed(self):
    AdWordsSanityCheck.ValidateService('BulkMutateJobService', 'v201206')
    AdWordsSanityCheck.ValidateService('BulkMutateJobService', 'v201109_1')
    AdWordsSanityCheck.ValidateService('BulkMutateJobService', 'v201109')

  def testValidateService_bmjsNotAllowed(self):
    self.assertRaises(ValidationError, AdWordsSanityCheck.ValidateService,
                      'BulkMutateJobService', 'v201209')
    self.assertRaises(ValidationError, AdWordsSanityCheck.ValidateService,
                      'BulkMutateJobService', 'v201301')


if __name__ == '__main__':
  unittest.main()