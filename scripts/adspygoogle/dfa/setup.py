#!/usr/bin/python
#
# Copyright 2011 Google Inc.
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

"""Setup script for the DFA API Python Client Library."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
from distutils.core import setup

from adspygoogle.dfa import LIB_AUTHOR
from adspygoogle.dfa import LIB_AUTHOR_EMAIL
from adspygoogle.dfa import LIB_NAME
from adspygoogle.dfa import LIB_URL
from adspygoogle.dfa import LIB_VERSION


PACKAGES = ['adspygoogle', 'adspygoogle.common', 'adspygoogle.common.https',
            'adspygoogle.common.soappy', 'adspygoogle.dfa',
            'adspygoogle.SOAPpy', 'adspygoogle.SOAPpy.wstools']
PACKAGE_DATA = {'adspygoogle.dfa': [os.path.join('data', '*')]}


setup(name='adspygoogle.dfa',
      version=LIB_VERSION,
      description=LIB_NAME,
      author=LIB_AUTHOR,
      author_email=LIB_AUTHOR_EMAIL,
      maintainer=LIB_AUTHOR,
      maintainer_email=LIB_AUTHOR_EMAIL,
      url=LIB_URL,
      license='Apache License 2.0',
      long_description='For additional information, please see %s' % LIB_URL,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      platforms='any')
