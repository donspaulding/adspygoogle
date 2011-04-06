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

"""Methods for sending and recieving SOAP XML requests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import re
import time

from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common.Errors import Error
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.WebService import WebService
from adspygoogle.common.soappy import MessageHandler
from adspygoogle.common.soappy.HTTPTransportHandler import HTTPTransportHandler
from adspygoogle.dfa import LIB_SIG
from adspygoogle.dfa import LIB_URL
from adspygoogle.dfa import WSSE_NS
from adspygoogle.dfa import DfaSanityCheck
from adspygoogle.dfa.DfaErrors import ERRORS
from adspygoogle.dfa.DfaErrors import DfaApiError
from adspygoogle.dfa.DfaErrors import DfaError
from adspygoogle.dfa.DfaSoapBuffer import DfaSoapBuffer


class DfaWebService(WebService):

  """Implements DfaWebService.

  Responsible for sending and recieving SOAP XML requests.
  """

  def __init__(self, headers, config, op_config, url, lock, logger=None):
    """Inits DfaWebService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      url: str URL of the web service to call.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    self.__config = config
    self.__service = url.split('/')[-1]
    super(DfaWebService, self).__init__(LIB_SIG, headers, config, op_config,
                                        url, lock, logger)

  def __GetLogHandlers(self, buf):
    """Gets a list of log handlers for the DFA library.

    Args:
      buf: SoapBuffer SOAP buffer from which calls are retrieved for logging.

    Returns:
      list Log handlers for the DFA library.
    """
    return [
        {
            'tag': 'xml_log',
            'name': 'soap_xml',
            'data': ''
        },
        {
            'tag': 'request_log',
            'name': 'request_info',
            'data': str('host=%s service=%s method=%s'
                        % (Utils.GetNetLocFromUrl(self._url),
                           buf.GetServiceName(), buf.GetCallName()))
        },
        {
            'tag': '',
            'name': 'dfa_api_lib',
            'data': ''
        }
    ]

  def __ManageSoap(self, buf, start_time, stop_time, error={}):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      start_time: str Time before service call was invoked.
      stop_time: str Time after service call was invoked.
      [optional]
      error: dict Error, if any.
    """
    try:
      handlers = self.__GetLogHandlers(buf)

      fault = super(DfaWebService, self)._ManageSoap(
          buf, handlers, LIB_URL, ERRORS, start_time, stop_time, error)
      if fault:
        # Raise a specific error, subclass of DfaApiError.
        if fault['detail'] is None: del fault['detail']
        if 'detail' in fault:
          if ('doubleclick' in fault['detail'] and
              'errorCode' in fault['detail']['doubleclick']):
            code = int(fault['detail']['doubleclick']['errorCode'])
            if code in ERRORS: raise ERRORS[code](fault)
        if isinstance(fault, str):
          raise DfaApiError(fault)
        elif isinstance(fault, dict):
          raise DfaApiError(fault)
    except DfaApiError, e:
      raise e
    except DfaError, e:
      raise e
    except Error, e:
      if error: e = error
      raise Error(e)

  def CallMethod(self, method_name, params, service_name=None, loc=None,
                 request=None):
    """Make an API call to specified method.

    Args:
      method_name: str API method name.
      params: list List of parameters to send to the API method.
      [optional]
      service_name: str API service name.
      loc: service Locator.
      request: instance Holder of the SOAP request.

    Returns:
      tuple/str Response from the API method. If 'raw_response' flag enabled a
                string is returned, tuple otherwise.
    """
    self._lock.acquire()

    try:
      headers = self._headers
      config = self._config
      config['data_injects'] = ()
      error = {}

      # Load/set authentication token.
      if config['soap_lib'] == SOAPPY:
        if Utils.BoolTypeConvert(config['wsse']):
          headers = {
              'UsernameToken': {
                  'Username': headers['Username'],
                  'Password': headers['AuthToken']
              }
          }
          config['ns_target'] = (WSSE_NS, 'Security')
        else:
          headers = {}

      default_ns = '/'.join(['http://www.doubleclick.net/dfa-api',
                             self._op_config['version']])

      if (config['soap_lib'] == SOAPPY):
        data_injects = []
        # If the version is not v1.11, inject the RequestHeader header in before
        # the Header section ends.
        if not self._op_config['version'] == 'v1.11':
          data_injects.append(
              ('</SOAP-ENV:Header>', '<ns2:RequestHeader '
               'xmlns:ns2="%s">\n<ns2:applicationName>%s'
               '</ns2:applicationName>\n</ns2:RequestHeader>\n'
               '</SOAP-ENV:Header>' % (default_ns, '%s|%s' %
                                       (LIB_SIG, config['app_name']))))

        # Remove the automatic SOAPpy wrapping of variables with <v1>, <v2>,
        # etc. Our MessageHandler.PackDictAsXml function will provide all the
        # wrapping necessary.
        data_injects.append(('<v1>', ''))
        data_injects.append(('</v1>', ''))
        data_injects.append(('<v2>', ''))
        data_injects.append(('</v2>', ''))
        data_injects.append(('<v3>', ''))
        data_injects.append(('</v3>', ''))
        data_injects.append(('<v4>', ''))
        data_injects.append(('</v4>', ''))

        # Add the wsdl namespace to the SOAP Envelope
        data_injects.append(('<SOAP-ENV:Envelope',
                             '<SOAP-ENV:Envelope xmlns:wsdl="%s"' % (
                                 default_ns)))

        # Put all xsi_types into the wsdl namespace
        data_injects.append(('xsi3:type="', 'xsi3:type="wsdl:'))

        config['data_injects'] = tuple(data_injects)

      buf = DfaSoapBuffer(
          xml_parser=self._config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self._config['pretty_xml']))

      start_time = time.strftime('%Y-%m-%d %H:%M:%S')
      response = super(DfaWebService, self).CallMethod(
          headers, config, method_name, params, buf,
          DfaSanityCheck.IsJaxbApi(self._op_config['version']), LIB_SIG,
          LIB_URL, service_name, loc, request)
      stop_time = time.strftime('%Y-%m-%d %H:%M:%S')

      # Restore list type which was overwritten by SOAPpy.
      if config['soap_lib'] == SOAPPY and isinstance(response, tuple):
        holder = []
        for element in response:
          holder.append(MessageHandler.RestoreListType(element, ('value',)))
        response = tuple(holder)

      if isinstance(response, dict) or isinstance(response, Error):
        error = response

      if not Utils.BoolTypeConvert(self.__config['raw_debug']):
        self.__ManageSoap(buf, start_time, stop_time, error)
    finally:
      if self._lock.locked():
        self._lock.release()

    if Utils.BoolTypeConvert(self._config['raw_response']):
      return response
    return response


  def CallRawMethod(self, soap_message):
    """Make an API call by posting raw SOAP XML message.

    Args:
      soap_message: str SOAP XML message.

    Returns:
      tuple Response from the API method.
    """
    self._lock.acquire()

    try:
      buf = DfaSoapBuffer(
          xml_parser=self._config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self._config['pretty_xml']))

      super(DfaWebService, self).CallRawMethod(
          buf, Utils.GetNetLocFromUrl(self._op_config['server']), soap_message)

      self.__ManageSoap(buf, self._start_time, self._stop_time,
                        {'data': buf.GetBufferAsStr()})
    finally:
      if self._lock.locked():
        self._lock.release()
    return (self._response,)
