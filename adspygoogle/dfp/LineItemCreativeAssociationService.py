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

"""Methods to access LineItemCreativeAssociationService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class LineItemCreativeAssociationService(ApiService):

  """Wrapper for LineItemCreativeAssociationService.

  The LineItemCreativeAssociation Service provides operations for creating,
  updating and retrieving line item creative associations (LICA).
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits LineItemCreativeAssociationService.

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
    super(LineItemCreativeAssociationService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateLineItemCreativeAssociation(self, lica):
    """Create a new line item creative association.

    Args:
      lica: dict Line item creative association to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, lica,
                               'LineItemCreativeAssociation')

    method_name = 'createLineItemCreativeAssociation'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              lica, 'lineItemCreativeAssociation', self._wsdl_types_map, False,
              'LineItemCreativeAssociation')))
    elif self._config['soap_lib'] == ZSI:
      lica = self._transformation.MakeZsiCompatible(
          lica, 'LineItemCreativeAssociation', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'lineItemCreativeAssociation': lica},)),
          'LineItemCreativeAssociation', self._loc, request)

  def CreateLineItemCreativeAssociations(self, licas):
    """Create a list of new line item creative associations.

    Args:
      licas: list Line item creative associations to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((licas, list),))
    for lica in licas:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, lica,
                                 'LineItemCreativeAssociation')

    method_name = 'createLineItemCreativeAssociations'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              licas, 'lineItemCreativeAssociations', self._wsdl_types_map,
              False, 'ArrayOf_LineItemCreativeAssociation')))
    elif self._config['soap_lib'] == ZSI:
      licas = self._transformation.MakeZsiCompatible(
          licas, 'ArrayOf_LineItemCreativeAssociation', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'lineItemCreativeAssociations': licas},)),
          'LineItemCreativeAssociation', self._loc, request)

  def GetLineItemCreativeAssociation(self, line_item_id, creative_id):
    """Return the line item creative association uniquely identified by the
    given line item id and creative id.

    Args:
      line_item_id: str ID of the line item, which must already exist.
      creative_id: str ID of the creative, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((line_item_id, (str, unicode)),
                               (creative_id, (str, unicode))))

    method_name = 'getLineItemCreativeAssociation'
    if self._config['soap_lib'] == SOAPPY:
      line_item_id = self._message_handler.PackVarAsXml(
          line_item_id, 'lineItemId')
      creative_id = self._message_handler.PackVarAsXml(
          creative_id, 'creativeId')
      return self.__service.CallMethod(
          method_name, (''.join([line_item_id, creative_id])))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name,
          (({'lineItemId': line_item_id}, {'creativeId': creative_id},)),
          'LineItemCreativeAssociation', self._loc, request)

  def GetLineItemCreativeAssociationsByStatement(self, filter_statement):
    """Return the line item creative associations that match the given
    statement.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of line item creative associations

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getLineItemCreativeAssociationsByStatement'
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
          method_name, (({'filterStatement': filter_statement},)),
          'LineItemCreativeAssociation', self._loc, request)

  def PerformLineItemCreativeAssociationAction(self, action, filter_statement):
    """Perform action on line item creative associations that match the given
    statement.

    Args:
      action: dict Action to perform.
      filter_statement: dict Publisher Query Language statement.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, action,
                               'LineItemCreativeAssociationAction')
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'performLineItemCreativeAssociationAction'
    if self._config['soap_lib'] == SOAPPY:
      action = self._message_handler.PackVarAsXml(
          action, 'lineItemCreativeAssociationAction', self._wsdl_types_map,
          False, 'LineItemCreativeAssociationAction')
      filter_statement = self._message_handler.PackVarAsXml(
          filter_statement, 'filterStatement', self._wsdl_types_map, False,
          'Statement')
      return self.__service.CallMethod(method_name,
                                       (''.join([action, filter_statement])))
    elif self._config['soap_lib'] == ZSI:
      action = self._transformation.MakeZsiCompatible(
          action, 'LineItemCreativeAssociationAction', self._wsdl_types_map,
          self._web_services)
      filter_statement = self._transformation.MakeZsiCompatible(
          filter_statement, 'Statement', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'lineItemCreativeAssociationAction': action},
                         {'filterStatement': filter_statement})),
          'LineItemCreativeAssociation', self._loc, request)

  def UpdateLineItemCreativeAssociation(self, lica):
    """Update the specified line item creative associations.

    Args:
      lica: dict Line item creative association to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, lica,
                               'LineItemCreativeAssociation')

    method_name = 'updateLineItemCreativeAssociation'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              lica, 'lineItemCreativeAssociation', self._wsdl_types_map, False,
              'LineItemCreativeAssociation')))
    elif self._config['soap_lib'] == ZSI:
      lica = self._transformation.MakeZsiCompatible(
          lica, 'LineItemCreativeAssociation',
          self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'lineItemCreativeAssociation': lica},)),
          'LineItemCreativeAssociation', self._loc, request)

  def UpdateLineItemCreativeAssociations(self, licas):
    """Update a list of specified line item creative associations.

    Args:
      licas: list the line item creative associations to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((licas, list),))
    for lica in licas:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, lica,
                                 'LineItemCreativeAssociation')

    method_name = 'updateLineItemCreativeAssociations'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              licas, 'lineItemCreativeAssociations', self._wsdl_types_map,
              False, 'ArrayOf_LineItemCreativeAssociation')))
    elif self._config['soap_lib'] == ZSI:
      licas = self._transformation.MakeZsiCompatible(
          licas, 'ArrayOf_LineItemCreativeAssociation', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'lineItemCreativeAssociations': licas},)),
          'LineItemCreativeAssociation', self._loc, request)
