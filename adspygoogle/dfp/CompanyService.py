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

"""Methods to access CompanyService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.dfp import WSDL_MAP
from adspygoogle.dfp.DfpWebService import DfpWebService


class CompanyService(ApiService):

  """Wrapper for CompanyService.

  The Company Service provides operations for creating, updating and retrieving
  companies.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CompanyService.

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
    super(CompanyService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfp', lock, logger)

  def CreateCompany(self, company):
    """Create a new company.

    Args:
      company: dict Company to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, company, 'Company')

    method_name = 'createCompany'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              company, 'company', self._wsdl_types_map, False, 'Company')))
    elif self._config['soap_lib'] == ZSI:
      company = self._transformation.MakeZsiCompatible(
          company, 'Company', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'company': company},)),
                                       'Company', self._loc, request)

  def CreateCompanies(self, companies):
    """Create a list of new companies.

    Args:
      companies: list Companies to create.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((companies, list),))
    for company in companies:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, company, 'Company')

    method_name = 'createCompanies'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              companies, 'companies', self._wsdl_types_map, False,
              'ArrayOf_Company')))
    elif self._config['soap_lib'] == ZSI:
      companies = self._transformation.MakeZsiCompatible(
          companies, 'ArrayOf_Company', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'companies': companies},)),
                                       'Company', self._loc, request)

  def GetCompany(self, company_id):
    """Return the company uniquely identified by the given id.

    Args:
      company_id: str ID of the company, which must already exist.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((company_id, (str, unicode)),))

    method_name = 'getCompany'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(company_id,
                                                           'companyId')))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'companyId': company_id},)),
                                       'Company', self._loc, request)

  def GetCompaniesByStatement(self, filter_statement):
    """Return the companies that match the given filter.

    Args:
      filter_statement: dict Publisher Query Language statement used to filter a
                        set of companies.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, filter_statement, 'Statement')

    method_name = 'getCompaniesByStatement'
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
          'Company', self._loc, request)

  def UpdateCompany(self, company):
    """Update the specified company.

    Args:
      company: dict Company to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.NewSanityCheck(self._wsdl_types_map, company, 'Company')

    method_name = 'updateCompany'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              company, 'company', self._wsdl_types_map, False, 'Company')))
    elif self._config['soap_lib'] == ZSI:
      company = self._transformation.MakeZsiCompatible(
          company, 'Company', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'company': company},)),
                                       'Company', self._loc, request)

  def UpdateCompanies(self, companies):
    """Update a list of specified companies.

    Args:
      companies: list Companies to update.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((companies, list),))
    for item in companies:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, item, 'Company')

    method_name = 'updateCompanies'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._message_handler.PackVarAsXml(
              companies, 'companies', self._wsdl_types_map, False,
              'ArrayOf_Company')))
    elif self._config['soap_lib'] == ZSI:
      companies = self._transformation.MakeZsiCompatible(
          companies, 'ArrayOf_Company', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'companies': companies},)),
                                       'Company', self._loc, request)
