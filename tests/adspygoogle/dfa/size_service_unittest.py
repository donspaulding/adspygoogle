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

"""Unit tests to cover SizeService."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import datetime
import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from adspygoogle.dfa.DfaErrors import DfaRequestError
from tests.adspygoogle.dfa import client
from tests.adspygoogle.dfa import HTTP_PROXY
from tests.adspygoogle.dfa import SERVER_V1_12
from tests.adspygoogle.dfa import SERVER_V1_13
from tests.adspygoogle.dfa import SERVER_V1_14
from tests.adspygoogle.dfa import TEST_VERSION_V1_12
from tests.adspygoogle.dfa import TEST_VERSION_V1_13
from tests.adspygoogle.dfa import TEST_VERSION_V1_14
from tests.adspygoogle.dfa import VERSION_V1_12
from tests.adspygoogle.dfa import VERSION_V1_13
from tests.adspygoogle.dfa import VERSION_V1_14


class SizeServiceTestV1_14(unittest.TestCase):

  """Unittest suite for SizeService using v1_14."""

  SERVER = SERVER_V1_14
  VERSION = VERSION_V1_14
  client.debug = False
  service = None
  SIZE_EXISTS_CODE = 101010
  size = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSizeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetSize(self):
    """Test whether we can fetch a size by id"""
    if self.__class__.size is None:
      self.testSaveSize()
    size_id = self.__class__.size['id']
    self.assert_(isinstance(self.__class__.service.GetSizeById(
        size_id), tuple))

  def testSaveSize(self):
    """Test whether we can save a size"""
    dt = datetime.datetime.now()
    size = {
        'width': '1%s' % (dt.minute),
        'height': '1%s' % (dt.second),
        'id' : '-1'
    }
    try:
      size = self.__class__.service.SaveSize(size)
      self.__class__.size = size[0]
      self.__class__.size['width'] = '1%s' % (dt.minute)
      self.__class__.size['height'] = '1%s' % (dt.second)
      self.assert_(isinstance(size, tuple))
    except DfaRequestError, e:
      self.assertEqual(e.code, self.__class__.SIZE_EXISTS_CODE)
      self.__class__.size = self.__class__.service.GetSizeByWidthHeight(
          '1%s' % (dt.minute), '1%s' % (dt.second))[0]


  def testGetSizeByWidthHeight(self):
    """Test whether we can fetch sizes by width and height."""
    if self.__class__.size is None:
      self.testSaveSize()
    self.assert_(isinstance(self.__class__.service.GetSizeByWidthHeight(
        self.__class__.size['width'], self.__class__.size['height']), tuple))

  def testGetSizes(self):
    """Test whether we can fetch sizes by criteria."""
    if self.__class__.size is None:
      self.testSaveSize()
    search_criteria = {
        'ids': [self.__class__.size['id']],
        'width': '-1',
        'height': '-1'
    }
    self.assert_(isinstance(self.__class__.service.GetSizes(
        search_criteria), tuple))


class SizeServiceTestV1_13(unittest.TestCase):

  """Unittest suite for SizeService using v1_13."""

  SERVER = SERVER_V1_13
  VERSION = VERSION_V1_13
  client.debug = False
  service = None
  SIZE_EXISTS_CODE = 101010
  size = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSizeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetSize(self):
    """Test whether we can fetch a size by id"""
    if self.__class__.size is None:
      self.testSaveSize()
    size_id = self.__class__.size['id']
    self.assert_(isinstance(self.__class__.service.GetSizeById(
        size_id), tuple))

  def testSaveSize(self):
    """Test whether we can save a size"""
    dt = datetime.datetime.now()
    size = {
        'width': '1%s' % (dt.minute),
        'height': '1%s' % (dt.second),
        'id' : '-1'
    }
    try:
      size = self.__class__.service.SaveSize(size)
      self.__class__.size = size[0]
      self.__class__.size['width'] = '1%s' % (dt.minute)
      self.__class__.size['height'] = '1%s' % (dt.second)
      self.assert_(isinstance(size, tuple))
    except DfaRequestError, e:
      self.assertEqual(e.code, self.__class__.SIZE_EXISTS_CODE)
      self.__class__.size = self.__class__.service.GetSizeByWidthHeight(
          '1%s' % (dt.minute), '1%s' % (dt.second))[0]


  def testGetSizeByWidthHeight(self):
    """Test whether we can fetch sizes by width and height."""
    if self.__class__.size is None:
      self.testSaveSize()
    self.assert_(isinstance(self.__class__.service.GetSizeByWidthHeight(
        self.__class__.size['width'], self.__class__.size['height']), tuple))

  def testGetSizes(self):
    """Test whether we can fetch sizes by criteria."""
    if self.__class__.size is None:
      self.testSaveSize()
    search_criteria = {
        'ids': [self.__class__.size['id']],
        'width': '-1',
        'height': '-1'
    }
    self.assert_(isinstance(self.__class__.service.GetSizes(
        search_criteria), tuple))


class SizeServiceTestV1_12(unittest.TestCase):

  """Unittest suite for SizeService using v1_12."""

  SERVER = SERVER_V1_12
  VERSION = VERSION_V1_12
  client.debug = False
  service = None
  SIZE_EXISTS_CODE = 101010
  size = None
  width = '0'
  height = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetSizeService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetSize(self):
    """Test whether we can fetch a size by id"""
    if self.__class__.size is None:
      self.testSaveSize()
    size_id = self.__class__.size['id']
    self.assert_(isinstance(self.__class__.service.GetSizeById(
        size_id), tuple))

  def testSaveSize(self):
    """Test whether we can save a size"""
    dt = datetime.datetime.now()
    size = {
        'width': '1%s' % (dt.minute),
        'height': '1%s' % (dt.second),
        'id' : '-1'
    }
    try:
      size = self.__class__.service.SaveSize(size)
      self.__class__.size = size[0]
      self.__class__.size['width'] = '1%s' % (dt.minute)
      self.__class__.size['height'] = '1%s' % (dt.second)
      self.assert_(isinstance(size, tuple))
    except DfaRequestError, e:
      self.assertEqual(e.code, self.__class__.SIZE_EXISTS_CODE)
      self.__class__.size = self.__class__.service.GetSizeByWidthHeight(
          '1%s' % (dt.minute), '1%s' % (dt.second))[0]


  def testGetSizeByWidthHeight(self):
    """Test whether we can fetch sizes by width and height."""
    if self.__class__.size is None:
      self.testSaveSize()
    self.assert_(isinstance(self.__class__.service.GetSizeByWidthHeight(
        self.__class__.size['width'], self.__class__.size['height']), tuple))

  def testGetSizes(self):
    """Test whether we can fetch sizes by criteria."""
    if self.__class__.size is None:
      self.testSaveSize()
    search_criteria = {
        'ids': [self.__class__.size['id']],
        'width': '-1',
        'height': '-1'
    }
    self.assert_(isinstance(self.__class__.service.GetSizes(
        search_criteria), tuple))


def makeTestSuiteV1_14():
  """Set up test suite using v1_14.

  Returns:
    TestSuite test suite using v1_14.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SizeServiceTestV1_14))
  return suite


def makeTestSuiteV1_13():
  """Set up test suite using v1_13.

  Returns:
    TestSuite test suite using v1_13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SizeServiceTestV1_13))
  return suite


def makeTestSuiteV1_12():
  """Set up test suite using v1_12.

  Returns:
    TestSuite test suite using v1_12.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SizeServiceTestV1_12))
  return suite


if __name__ == '__main__':
  suites = []
  if TEST_VERSION_V1_14:
    suites.append(makeTestSuiteV1_14())
  if TEST_VERSION_V1_13:
    suites.append(makeTestSuiteV1_13())
  if TEST_VERSION_V1_12:
    suites.append(makeTestSuiteV1_12())
  if suites:
    alltests = unittest.TestSuite(suites)
    unittest.main(defaultTest='alltests')
