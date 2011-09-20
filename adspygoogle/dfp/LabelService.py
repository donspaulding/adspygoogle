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

"""Methods to access LabelService service."""

__author__ = 'api.shamjeff@gmail.com (Jeff Sham)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class LabelService(ApiService):

  """Wrapper for LabelService.

  The LabelService Service provides methods for the creation and management of
  Labels.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits LabelService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'apis/ads/publisher', op_config['version'],
           self.__class__.__name__]
    self.__service = DfpWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(LabelService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateLabel(self, label):
    """Create a new label.

    Args:
      label: dict Label to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, label, 'Label')

    method_name = 'createLabel'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              label, 'label', self._wsdl_types_map, False, 'Label')))
    elif self._config['soap_lib'] == ZSI:
      label = self._transformation.MakeZsiCompatible(
          label, 'Label', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'label': label},)),
                                       'Label', self._loc, request)

  def CreateLabels(self, labels):
    """Create a list of new labels.

    Args:
      labels: list Labels to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((labels, list),))
    for label in labels:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, label, 'Label')

    method_name = 'createLabels'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              labels, 'labels', self._wsdl_types_map, False, 'ArrayOf_Label')))
    elif self._config['soap_lib'] == ZSI:
      labels = self._transformation.MakeZsiCompatible(
          labels, 'ArrayOf_Label', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'labels': labels},)),
                                       'Label', self._loc, request)

  def GetLabel(self, label_id):
    """Return the label uniquely identified by the given id.

    Args:
      label_id: str ID of the label, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((label_id, (str, unicode)),))

    method_name = 'getLabel'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(label_id,
                                                           'labelId')))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'labelId': label_id},)),
                                       'Label', self._loc, request)

  def GetLabelsByStatement(self, filter_statement):
    """Return the labels that match the given statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of labels.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getLabelsByStatement'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              filter_statement, 'filterStatement', self._wsdl_types_map, False,
              'Statement')))
    elif self._config['soap_lib'] == ZSI:
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'filterStatement': filter_statement},)), 'Label',
          self._loc, request)

  def PerformLabelAction(self, action, filter_statement):
    """Perform action on labels that match the given statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, action, 'LabelAction')
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'performLabelAction'
    if self._config['soap_lib'] == SOAPPY:
      action = self._message_handler.PackVarAsXml(
          action, 'labelAction', self._wsdl_types_map, False,
          'LabelAction')
      filter_statement = self._message_handler.PackVarAsXml(
          filter_statement, 'filterStatement', self._wsdl_types_map, False,
          'Statement')
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._transformation.MakeZsiCompatible(
          action, 'LabelAction', self._wsdl_types_map,
          self._web_services)
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'labelAction': action},
                         {'filterStatement': filter_statement})),
          'Label', self._loc, request)

  def UpdateLabel(self, label):
    """Update the specified label.

    Args:
      label: dict Label to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, label, 'Label')

    method_name = 'updateLabel'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              label, 'label', self._wsdl_types_map, False, 'Label')))
    elif self._config['soap_lib'] == ZSI:
      label = self._transformation.MakeZsiCompatible(
          label, 'Label', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'label': label},)),
                                       'Label', self._loc, request)

  def UpdateLabels(self, labels):
    """Update a list of specified labels.

    Args:
      labels: list Labels to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((labels, list),))
    for label in labels:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, label, 'Label')

    method_name = 'updateLabels'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              labels, 'labels', self._wsdl_types_map, False, 'ArrayOf_Label')))
    elif self._config['soap_lib'] == ZSI:
      labels = self._transformation.MakeZsiCompatible(
          labels, 'ArrayOf_Label', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'labels': labels},)),
                                       'Label', self._loc, request)
