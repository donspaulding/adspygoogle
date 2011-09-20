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

"""Methods to access ReportService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import gzip
import StringIO
import time
import urllib

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class ReportService(ApiService):

  """Wrapper for ReportService.

  The Report Service provides operations for executing a report job and
  retrieving performance and statistics about ad campaigns, networks, inventory
  and sales.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ReportService.

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
    super(ReportService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def GetReportDownloadURL(self, report_job_id, export_format):
    """Return the URL at which the report file can be downloaded.

    Args:
      report_job_id: str Id of the report job.
      export_format: str Export format for the report file.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))
    SanityCheck.NewSanityCheck(self._wsdl_types_map, export_format,
                               'ExportFormat')

    method_name = 'getReportDownloadURL'
    if self._config['soap_lib'] == SOAPPY:
      report_job_id = self._message_handler.PackVarAsXml(
          report_job_id, 'reportJobId')
      export_format = self._message_handler.PackVarAsXml(
          export_format, 'exportFormat')
      return self.__service.CallMethod(
          method_name, (''.join([report_job_id, export_format])))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},
                                         {'exportFormat': export_format})),
                                       'Report', self._loc, request)

  def GetReportJob(self, report_job_id):
    """Return report job uniquely identified by the given id.

    Args:
      report_job_id: str Id of the report job.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getReportJob'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              report_job_id, 'reportJobId')))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self._loc, request)

  def RunReportJob(self, report_job):
    """Initiate the execution of a report query on the server.

    Args:
      report_job: dict Report job to run.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, report_job, 'ReportJob')

    method_name = 'runReportJob'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              report_job, 'reportJob', self._wsdl_types_map, False,
              'ReportJob')))
    elif self._config['soap_lib'] == ZSI:
      report_job = self._transformation.MakeZsiCompatible(
          report_job, 'ReportJob', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(
          method_name, (({'reportJob': report_job},)), 'Report', self._loc,
          request)

  def DownloadReport(self, report_job_id, export_format):
    """Download and return report data.

    Args:
      report_job_id: str ID of the report job.
      export_format: str Export format for the report file.

    Returns:
      str Report data or empty string if report failed.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    # Wait for report to complete.
    status = self.GetReportJob(report_job_id)[0]['reportJobStatus']
    while status != 'COMPLETED' and status != 'FAILED':
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Report job status: %s' % status
      time.sleep(30)
      status = self.GetReportJob(report_job_id)[0]['reportJobStatus']

    if status == 'FAILED':
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Report process failed'
      return ''
    else:
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Report has completed successfully'

    # Get report download URL.
    report_url = self.GetReportDownloadURL(report_job_id, export_format)[0]

    # Download report.
    data = urllib.urlopen(report_url).read()
    data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
    return data
