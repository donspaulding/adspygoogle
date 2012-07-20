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

"""Script to pack the client library into a .tar.gz ball.

Usage:
  $ python pack_it.py adwords
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

from adspygoogle.adwords import DEFAULT_API_VERSION as ADWORDS_MAX_VER
from adspygoogle.dfa import DEFAULT_API_VERSION as DFA_MAX_VER
from adspygoogle.dfp import DEFAULT_API_VERSION as DFP_MAX_VER
import os
import platform
import re
import shutil
import subprocess
import sys
sys.path.insert(0, os.path.join('..', '..', '..'))


LIBS = ['adwords', 'adxbuyer', 'dfa', 'dfp']
TARGET_DIR_BASE = '/tmp/google-py'
ADWORDS_ONLY_REGEX = 'Api:.*AdWordsOnly'
MAX_VERSIONS = {
    'adwords': ADWORDS_MAX_VER,
    'dfa': DFA_MAX_VER,
    'dfp': DFP_MAX_VER
}

def FileMatches(filename, regex=ADWORDS_ONLY_REGEX):
  """Runs the regex against the provided file.

  Args:
    filename: str Name of the file to regex.
    regex: str Regex to run against this file. Defaults to ADWORDS_ONLY_REGEX.

  Returns:
    bool True if the regex matches the file.
  """
  f = open(filename, 'r')
  try:
    text = f.read()
    matches = re.search(regex, text)
    return matches
  finally:
    f.close()


def UpdateSOAPpy():
  """Runs download_and_patch_soappy.py to make sure SOAPpy is up to date."""
  cur_dir = os.curdir
  os.chdir(os.path.join(cur_dir, 'adspygoogle', 'SOAPpy'))
  _ = subprocess.call(['python', 'download_and_patch_soappy.py'])
  os.chdir(cur_dir)


def Main(argv):
  """Builds a gzipped tarball containing the api library you specified.

  Args:
    argv: list Commandline args with script name removed.
  """
  release_tests = None
  if '--test' in argv:
    release_tests = os.path.abspath('releasetests.sh')
    argv.remove('--test')

  if not argv or len(argv) != 1 or argv[0] not in LIBS:
    print ('Nothing was done. Make sure to pass in the right argument: %s'
           % LIBS)
    return

  effective_target = actual_target = argv[0]
  if actual_target == 'adxbuyer': effective_target = 'adwords'

  LIB_NAME = LIB_URL = LIB_VERSION = ''
  exec 'from adspygoogle.%s import LIB_NAME' % effective_target
  exec 'from adspygoogle.%s import LIB_URL' % effective_target
  exec 'from adspygoogle.%s import LIB_VERSION' % effective_target

  lib_tag = '%s_api_python_%s' % (actual_target, LIB_VERSION)
  source_dir = os.path.abspath('.')
  UpdateSOAPpy()
  target_dir = '%s/%s' % (TARGET_DIR_BASE, lib_tag)
  # If temp base dir exists, remove it so we start fresh
  if os.path.exists(target_dir):
    os.system('rm -rf %s*' % target_dir)
  # Create the target directory
  os.makedirs(target_dir)
  target_pkg_dir = os.path.join(target_dir, 'adspygoogle')
  target_lib_dir = os.path.join(target_pkg_dir, effective_target)
  target_docs_dir = os.path.join(target_dir, 'docs')
  target_examples_dir = os.path.join(target_dir, 'examples', 'adspygoogle',
                                     effective_target)
  target_logs_dir = os.path.join(target_dir, 'logs')
  target_scripts_dir = os.path.join(target_dir, 'scripts', 'adspygoogle',
                                    effective_target)
  target_common_scripts_dir = os.path.join(target_dir, 'scripts', 'adspygoogle',
                                           'common')
  target_tests_dir = os.path.join(target_dir, 'tests')

  # If there is an existing copy of the target directory, remove it.
  if os.path.exists(os.path.abspath(target_dir)):
    shutil.rmtree(os.path.abspath(target_dir))

  # Recursively copy client library code into target package directory.
  shutil.copytree(os.path.join(source_dir, 'adspygoogle', effective_target),
                  target_lib_dir)
  shutil.copytree(os.path.join(source_dir, 'adspygoogle', 'common'),
                  os.path.join(target_pkg_dir, 'common'))
  shutil.copyfile(os.path.join(source_dir, 'adspygoogle', '__init__.py'),
                  os.path.join(target_pkg_dir, '__init__.py'))

  # Copy examples.  Need to handle AdX as a special case.
  if actual_target == 'adxbuyer':
    adx_source_dir = os.path.join(source_dir, 'examples', 'adspygoogle',
                                  actual_target)
    adwords_source_dir = os.path.join(source_dir, 'examples', 'adspygoogle',
                                      effective_target)
    # Copy over AdX examples, this creates the directory structure we need.
    shutil.copytree(adx_source_dir, target_examples_dir)

    # Need to copy examples from adwords for all versions that AdX has.
    for version_dir in os.listdir(adx_source_dir):
      # Skip non-directories (README)
      if not os.path.isdir(os.path.join(adwords_source_dir, version_dir)):
        continue
      for category_dir in os.listdir(os.path.join(adwords_source_dir,
                                                  version_dir)):
        # Skip non-directories (README)
        if not os.path.isdir(os.path.join(adwords_source_dir, version_dir,
                                          category_dir)):
          continue
        if not os.path.exists(os.path.join(target_examples_dir, version_dir,
                                           category_dir)):
          os.makedirs(os.path.join(target_examples_dir, version_dir,
                                   category_dir))
        for filename in os.listdir(os.path.join(adwords_source_dir, version_dir,
                                                category_dir)):
          source_file = os.path.join(adwords_source_dir, version_dir,
                                     category_dir, filename)
          if not os.path.exists(source_file): continue
          dest_file = os.path.join(target_examples_dir, version_dir,
                                   category_dir, filename)
          # Only copy over if it doesn't match our exclusion list.
          if FileMatches(source_file,
                         ADWORDS_ONLY_REGEX) or os.path.exists(dest_file):
            pass
          else:
            shutil.copy(source_file, dest_file)
  else:
    shutil.copytree(os.path.join(source_dir, 'examples', 'adspygoogle',
                                 effective_target), target_examples_dir)
  # Copy __init.py__ files in examples
  shutil.copyfile(os.path.join(source_dir, 'examples', '__init__.py'),
                  os.path.join(target_dir, 'examples', '__init__.py'))
  shutil.copyfile(os.path.join(source_dir, 'examples', 'adspygoogle',
                               '__init__.py'),
                  os.path.join(target_dir, 'examples', 'adspygoogle',
                               '__init__.py'))

  # Copy the rest of the data that comes with client library.
  shutil.copytree(os.path.join(source_dir, 'docs'), target_docs_dir)
  shutil.copytree(os.path.join(source_dir, 'logs'), target_logs_dir)
  shutil.copytree(os.path.join(source_dir, 'scripts', 'adspygoogle',
                               effective_target), target_scripts_dir)
  shutil.copytree(os.path.join(source_dir, 'scripts', 'adspygoogle', 'common'),
                               target_common_scripts_dir)
  shutil.copyfile(os.path.join(source_dir, 'scripts', 'README'),
                  os.path.join(target_dir, 'scripts', 'README'))
  shutil.copyfile(os.path.join(source_dir, 'scripts', '__init__.py'),
                  os.path.join(target_dir, 'scripts', '__init__.py'))
  shutil.copyfile(os.path.join(source_dir, 'scripts', 'adspygoogle',
                               '__init__.py'),
                  os.path.join(target_dir, 'scripts', 'adspygoogle',
                               '__init__.py'))
  shutil.move(os.path.join(target_scripts_dir, 'config.py'),
              os.path.join(target_dir, 'config.py'))
  shutil.move(os.path.join(target_scripts_dir, 'setup.py'),
              os.path.join(target_dir, 'setup.py'))
  shutil.copytree(os.path.join(source_dir, 'tests', 'adspygoogle',
                               effective_target),
                  os.path.join(target_tests_dir, 'adspygoogle',
                               effective_target))
  shutil.copytree(os.path.join(source_dir, 'tests', 'adspygoogle', 'common'),
                  os.path.join(target_tests_dir, 'adspygoogle', 'common'))
  shutil.copyfile(os.path.join(source_dir, 'tests', '__init__.py'),
                  os.path.join(target_tests_dir, '__init__.py'))
  shutil.copyfile(os.path.join(source_dir, 'tests', 'adspygoogle',
                               '__init__.py'),
                  os.path.join(target_tests_dir, 'adspygoogle', '__init__.py'))
  shutil.copyfile(os.path.join(source_dir, 'COPYING'),
                  os.path.join(target_dir, 'COPYING'))
  shutil.move(os.path.join(target_lib_dir, 'README'),
              os.path.join(target_dir, 'README'))
  shutil.move(os.path.join(target_pkg_dir, 'common', 'README.Common'),
              os.path.join(target_dir, 'README.Common'))

  # Perform clean up, generate docs, and adjust permissions.
  os.chdir(target_dir)
  # Remove files (especially .pyc) before generating docs.
  os.system('find . \( -name \'*auth.pkl\' -or -name \'*config.pkl\' '
            '-or -name \'*.log\' -or -name \'*.pyc*\''
            ' -or -name \'.project\' -or -name \'.pydevproject\' -or -name '
            '\'.settings\' \) | xargs rm -fr')
  os.system('find docs \( -not -name \'docs\' -and -not -name \'README\' \) | '
            'xargs rm')
  os.system('epydoc -q --name "%s" --url "%s" --html adspygoogle '
            '--exclude=_services -o docs' % (LIB_NAME, LIB_URL))
  os.system('perl -pi -e \'s/Generated by Epydoc (\d+\.\d+\.\d+) .*/Generated '
            'by Epydoc $1/\' docs/*')

  # Now that docs are generated, copy over SOAPpy.
  shutil.copytree(os.path.join(source_dir, 'adspygoogle', 'SOAPpy'),
                  os.path.join(target_pkg_dir, 'SOAPpy'))

  # Remove any .pyc files that may have been created during docs generation.
  os.system('find . -name \'*.pyc*\' | xargs rm -fr')

  # Remove any ._* files.
  if platform.system() == 'Darwin' and platform.mac_ver()[0] >= '10.5':
    os.system('dot_clean --keep=native .')

  # Package target directory into .tar.gz and adjust permissions.
  os.chdir(os.path.abspath(os.path.join(target_dir, '..')))
  os.system('tar -cf %s.tar %s/' % (lib_tag, lib_tag))
  os.system('gzip %s.tar' % lib_tag)

  # Optionally run tests.
  if release_tests:
    os.system('/bin/bash %s %s %s %s' % (release_tests, target_dir,
                                         effective_target,
                                         MAX_VERSIONS[effective_target]))

  print 'Built %s at %s' % (actual_target, TARGET_DIR_BASE)


if __name__ == '__main__':
  Main(sys.argv[1:])
