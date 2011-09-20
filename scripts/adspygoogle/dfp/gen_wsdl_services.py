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

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import re
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))

from adspygoogle.common import Utils
from adspygoogle.dfp import LIB_HOME
from scripts.adspygoogle.common import FILE_HEADER
from scripts.adspygoogle.common import wsdl_auto_obj
from scripts.adspygoogle.dfp import API_TARGETS


def DfpWsdlToUrl(wsdl_info, service_name):
  return '/'.join([wsdl_info['server'], 'apis/ads/publisher',
                   wsdl_info['version'], service_name + '?wsdl'])

# Clean up any old classes.
for target in API_TARGETS:
  if os.path.exists(os.path.abspath(target['location'])):
    for f_name in os.listdir(os.path.abspath(target['location'])):
      os.unlink(os.path.abspath(os.path.join(target['location'], f_name)))
  else:
    os.mkdir(os.path.abspath(target['location']))

# Generate client interface from WSDL.
print 'Generating and patching client interface from WSDL definitions ...'
for target in API_TARGETS:
  items = [FILE_HEADER,
           '\n\n"""Modules and classes generated via wsdl2py."""\n']

  for service in target['services']:
    wsdl_url = DfpWsdlToUrl(target, service)
    res = os.system('python2.4 `which wsdl2py` --url=%s --output-dir=%s' % (
        wsdl_url, target['location']))
    if res > 0:
      res = raw_input('Unable to locate WSDL \'%s\' remotely, trying local '
                      'search at [%s]: ' % (wsdl_url, os.getcwd()))
      f_path = os.path.join(res, service + '?wsdl')
      if os.path.abspath(res) and f_path:
        os.system('python2.4 `which wsdl2py` --file=%s --output-dir=%s' %
                  (f_path, target['location']))
  f_path = os.path.abspath('/'.join([target['location'], '__init__.py']))
  fh = open(f_path, 'w')
  try:
    fh.write(''.join(items))
  finally:
    fh.close()

# Patch client interface.
for target in API_TARGETS:
  # Patch v*/*_services_types.py:
  #   - Make all elements optional.
  #   - Make all elements nillable.
  #   - ZSI.TCtimes.gDate uses default timezone, which may be different from
  #     account's timezone (e.g., 2008-01-01Z), use ZSI.TC.String instead.
  #   - Use ZSI.TC.String instead of ZSI.TCnumbers.Iint.
  #   - Use ZSI.TC.String instead of ZSI.TCnumbers.Ilong.
  #   - Use ZSI.TC.String instead of ZSI.TCnumbers.FPdouble.
  #   - Use ZSI.TC.String instead of ZSI.TC.Boolean.
  for f_name in os.listdir(os.path.abspath(target['location'])):
    f_path = os.path.join(os.path.abspath(target['location']), f_name)
    if os.path.exists(f_path):
      fh = open(f_path, 'r')
      try:
        data = fh.read()
        data = data.replace('minOccurs=1', 'minOccurs=0')
        data = data.replace('nillable=False', 'nillable=True')
        data = data.replace('ZSI.TCtimes.gDate', 'ZSI.TC.String')
        data = data.replace('ZSI.TC.StringTime', 'ZSI.TC.String')
        data = data.replace('ZSI.TCnumbers.Iint', 'ZSI.TC.String')
        data = data.replace('ZSI.TCnumbers.Ilong', 'ZSI.TC.String')
        data = data.replace('ZSI.TCnumbers.FPdouble', 'ZSI.TC.String')
        data = data.replace('ZSI.TC.Boolean', 'ZSI.TC.String')
      finally:
        fh.close()
      fh = open(f_path, 'w')
      try:
        fh.write(data)
      finally:
        fh.close()

  # Patch v*/*.py:
  #   - In local instances, whenever we encounter 'get' or 'mutate', we use
  #     'getXxx' or 'mutateXxx' respectively. The Xxx refer to the name of the
  #     service (i.e. Company, LineItem).
  #
  # This patch allows Python to import generated types with out collision.
  # Otherwise, we end up with types like 'mutate_Dec', 'mutate', etc. which
  # show up in all services and cause invalid instance of a service to be
  # invoked (defaults to the first instance that is found). So, if you invoke
  # an instance of CampaignService and AdGroupService and then try to add an
  # ad group, it will invoke 'mutate' from wrong service (CampaignService in
  # this case) resulting in a failure.
  for f_name in os.listdir(os.path.abspath(target['location'])):
    f_path = os.path.join(os.path.abspath(target['location']), f_name)
    f_parts = f_name.split('Service_')
    if os.path.exists(f_path):
      fh = open(f_path, 'r')
    try:
      data = fh.read()
      ops = ['get', 'mutate']
      if f_name.find('_services.py') > -1:
        for op in ops:
          data = data.replace('def %s(' % op, 'def %s%s(' % (op, f_parts[0]))
          data = data.replace('# op: %s' % op,
                              '# %s: get%s' % (op, f_parts[0]))
          data = data.replace('%sRequest' % op,
                              '%s%sRequest' % (op, f_parts[0]))
          data = data.replace('%sResponse' % op,
                              '%s%sResponse' % (op, f_parts[0]))
      elif f_name.find('_types.py') > -1:
        for op in ops:
          data = data.replace('= "%s"' % op, '= "%s%s"' % (op, f_parts[0]))
          data = data.replace('= "%sResponse"' % op,
                              '= "%s%sResponse"' % (op, f_parts[0]))
          data = data.replace('%sResponse_' % op,
                              '%s%sResponse_' % (op, f_parts[0]))

      for op in ops:
        data = data.replace('%s_Dec' % op, '%s%s_Dec' % (op, f_parts[0]))

      # Duplicate class name clean up.
      data = data.replace('%s%s' % (f_parts[0], f_parts[0]), f_parts[0])
    finally:
      fh.close()
    fh = open(f_path, 'w')
    try:
      fh.write(data)
    finally:
      fh.close()

  print '  [+] %s' % os.path.abspath(target['location'])

# Fetch error types.
print 'Generating error types from client interface ...'
old_error_types = []
for item in Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                                  'error_types.csv')):
  old_error_types.append(item[0])
error_types = []
for target in API_TARGETS:
  for f_name in os.listdir(os.path.abspath(target['location'])):
    f_path = os.path.join(os.path.abspath(target['location']), f_name)
    if f_path.find('_services_types.py') < 0 or f_path.endswith('pyc'): continue

    data = Utils.ReadFile(f_path)
    for type in re.compile('class (\w+)_Def\(').findall(data):
      if type.endswith('Error') and type not in error_types:
        if type not in old_error_types:
          print '  [+] found new error type, %s' % type
        error_types.append(type)

# Write error types to a CSV file.
data = ['Type']
for type in sorted(set(error_types)):
  data.append('%s' % type)
data.append('')
f_path = os.path.abspath(os.path.join(LIB_HOME, 'data', 'error_types.csv'))
fh = open(f_path, 'w')
try:
  fh.write('\n'.join(data))
finally:
  fh.close()

# Generate WSDL definitions pickle.
print 'Generating WSDL definitions pickle...'
pickle_location = os.path.join('..', '..', '..', 'adspygoogle', 'dfp', 'data')
types_filename = 'wsdl_type_defs.pkl'
operation_filename = 'wsdl_ops_defs.pkl'

wsdl_auto_obj.GenPickles(pickle_location, types_filename, operation_filename,
                         API_TARGETS, DfpWsdlToUrl)

print '... done.'
