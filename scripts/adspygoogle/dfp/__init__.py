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

"""Contains common constants for DFP scripts."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

import os

API_TARGETS = [
    {
        'version': 'v201103',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'dfp', 'zsi',
                                 'v201103'),
        'server': 'https://www.google.com',
        'services': ('CompanyService', 'CreativeService',
                     'CustomTargetingService', 'ForecastService',
                     'InventoryService', 'LineItemCreativeAssociationService',
                     'LineItemService', 'NetworkService', 'OrderService',
                     'PlacementService', 'PublisherQueryLanguageService',
                     'ReportService', 'UserService')
    },
    {
        'version': 'v201104',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'dfp', 'zsi',
                                 'v201104'),
        'server': 'https://www.google.com',
        'services': ('CompanyService', 'CreativeService',
                     'CustomTargetingService', 'ForecastService',
                     'InventoryService', 'LineItemCreativeAssociationService',
                     'LineItemService', 'NetworkService', 'OrderService',
                     'PlacementService', 'PublisherQueryLanguageService',
                     'ReportService', 'UserService')
    },
    {
        'version': 'v201107',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'dfp', 'zsi',
                                 'v201107'),
        'server': 'https://www.google.com',
        'services': ('CompanyService', 'CreativeService',
                     'CustomTargetingService', 'ForecastService',
                     'InventoryService', 'LabelService',
                     'LineItemCreativeAssociationService', 'LineItemService',
                     'NetworkService', 'OrderService', 'PlacementService',
                     'PublisherQueryLanguageService', 'ReportService',
                     'UserService')
    },
    {
        'version': 'v201108',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'dfp', 'zsi',
                                 'v201108'),
        'server': 'https://www.google.com',
        'services': ('CompanyService', 'CreativeService',
                     'CustomTargetingService', 'ForecastService',
                     'InventoryService', 'LabelService',
                     'LineItemCreativeAssociationService', 'LineItemService',
                     'NetworkService', 'OrderService', 'PlacementService',
                     'PublisherQueryLanguageService', 'ReportService',
                     'ThirdPartySlotService', 'UserService')
    }
]
