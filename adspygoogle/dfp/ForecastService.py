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

"""Methods to access ForecastService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class ForecastService(ApiService):

  """Wrapper for ForecastService.

  The Forecast Service provides operations for estimating traffic
  (clicks/impressions) for line items.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ForecastService.

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
    super(ForecastService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def GetForecast(self, line_item):
    """Return a forecast on a hypothetical line item.

    Args:
      line_item: dict Target of the forecast.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, line_item, 'LineItem')

    method_name = 'getForecast'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              line_item, 'lineItem', self._wsdl_types_map, False, 'LineItem')))
    elif self._config['soap_lib'] == ZSI:
      line_item = self._transformation.MakeZsiCompatible(
          line_item, 'LineItem', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItem': line_item},)),
                                       'Forecast', self._loc, request)

  def GetForecastById(self, line_item_id):
    """Return a forecast for an existing line item.

    Args:
      line_item_id: str ID of the line item to run the forecast on.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((line_item_id, (str, unicode)),))

    method_name = 'getForecastById'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(line_item_id,
                                                           'lineItemId')))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'lineItemId': line_item_id},)),
                                       'Forecast', self._loc, request)
