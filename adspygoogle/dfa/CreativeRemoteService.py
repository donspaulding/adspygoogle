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

"""Methods to access CreativeRemoteService service."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ApiVersionNotSupportedError
from adspygoogle.dfa import DfaUtils
from adspygoogle.dfa import WSDL_MAP
from adspygoogle.dfa.DfaWebService import DfaWebService


class CreativeRemoteService(ApiService):

  """Wrapper for CreativeRemoteService.

  The Creative Service allows you to create, update, delete, and retrieve
  creatives.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits CreativeRemoteService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], op_config['version'],
           'api/dfa-api/creative']
    self.__service = DfaWebService(headers, config, op_config, '/'.join(url),
                                   lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(CreativeRemoteService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.dfa', lock, logger)

  def AssignCreativeGroupsToCreative(self, campaign_id, creative_id,
                                     creative_group_ids):
    """Assigns creative groups to a creative within the campaign.

    Args:
      campaign_id: str Id of the campaign.
      creative_id: str Id of the creative.
      creative_group_ids: list Creative group ids to assign.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),
                               (creative_id, (str, unicode)),
                               (creative_group_ids, list),))
    for item in creative_group_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'assignCreativeGroupsToCreative'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(campaign_id, 'campaignId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                creative_id, 'creativeId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                creative_group_ids, 'creativeGroupIds', [],
                                True)),))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def AssignCreativesToPlacements(self, creative_placement_assignments):
    """Assigns the creatives to placements.

    A unique ad will be created for each such assignment.

    Args:
      creative_placement_assignments: list Creative placement assignments.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_placement_assignments, list),))
    for item in creative_placement_assignments:
      SanityCheck.NewSanityCheck(
          self._wsdl_types_map, item, 'CreativePlacementAssignment')

    method_name = 'assignCreativesToPlacements'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_placement_assignments, 'creativePlacementAssignment',
                  self._wsdl_types_map, True,
                  'ArrayOfCreativePlacementAssignment'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def AssociateCreativesToCampaign(self, campaign_id, creative_ids):
    """Associates the given creatives to the campaign.

    Args:
      campaign_id: str Id of the campaign to which creatives to be assigned.
      creative_ids: list Ids of creatives to be assigned.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),
                               (creative_ids, list)))
    for item in creative_ids:
      SanityCheck.ValidateTypes(((item, (str, unicode)),))

    method_name = 'associateCreativesToCampaign'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(campaign_id, 'campaignId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                creative_ids, 'creativeIds', [], True))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def CopyCreative(self, copy_requests):
    """Creates copies for given creatives.

    Args:
      copy_requests: list Creative copy requests.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((copy_requests, list),))
    for item in copy_requests:
      SanityCheck.NewSanityCheck(
          self._wsdl_types_map, item, 'CreativeCopyRequest')

    method_name = 'copyCreative'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  copy_requests, 'creativeCopyRequests', self._wsdl_types_map,
                  True, 'ArrayOfCreativeCopyRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def CreateCreativesFromCreativeUploadSession(self, creative_upload_session):
    """Creates creatives from files uploaded in a creative upload session.

    Args:
      creative_upload_session: dict Creative upload session.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map,
        creative_upload_session,
        'CreativeUploadSession')

    method_name = 'createCreativesFromCreativeUploadSession'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_upload_session, 'creativeUploadSession',
                  self._wsdl_types_map, True, 'CreativeUploadSession'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteCreative(self, creative_id):
    """Deletes the creative with the given id.

    Args:
      creative_id: str Id of the creative to delete.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_id, (str, unicode)),))

    method_name = 'deleteCreative'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def DeleteRichMediaAsset(self, creative_id, asset_file_name):
    """Deletes the rich media asset.

    Args:
      creative_id: str Id of the creative from which to delete asset.
      asset_file_name: str File name of the asset to be deleted.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_id, (str, unicode)),
                               (asset_file_name, (str, unicode))))

    method_name = 'deleteRichMediaAsset'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_id, 'id')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                asset_file_name, 'assetFileName'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GenerateCreativeUploadSession(self, creative_upload_session_request):
    """Generates new creative upload session.

    A new session can be created based off of a advertiser identifier
    (advertiser level) or campaign identifier (campaign level).

    Args:
      creative_upload_session_request: dict Request to obtain a new creative
                                       upload session.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_upload_session_request,
        'CreativeUploadSessionRequest')

    method_name = 'generateCreativeUploadSession'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_upload_session_request,
                  'creativeUploadSessionRequest', self._wsdl_types_map, True,
                  'CreativeUploadSessionRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetAssignedCreativeGroupsToCreative(self, campaign_id, creative_id):
    """Returns assigned creative group to the given creative in a campaign.

    Args:
      campaign_id: str Id of the campaign.
      creative_id: str Id of the creative.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),
                               (creative_id, (str, unicode))))

    method_name = 'getAssignedCreativeGroupsToCreative'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(campaign_id, 'campaignId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                creative_id, 'creativeId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCompleteCreativeUploadSession(self, upload_session):
    """Returns complete creative upload session information.

    Args:
      upload_session: dict Creative upload session.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, upload_session, 'CreativeUploadSessionSummary')

    method_name = 'getCompleteCreativeUploadSession'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  upload_session, 'uploadSession', self._wsdl_types_map, True,
                  'CreativeUploadSessionSummary'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreative(self, creative_id):
    """Returns the creative for a given id.

    Args:
      creative_id: str Id of the creative to return.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_id, (str, unicode)),))

    method_name = 'getCreative'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeAssets(self, creative_asset_search_criteria):
    """Returns the assets matching the given criteria.

    Args:
      creative_asset_search_criteria: dict Search criteria to match creatives
                                      assets.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_asset_search_criteria,
        'CreativeAssetSearchCriteria')

    method_name = 'getCreativeAssets'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_asset_search_criteria, 'creativeAssetSearchCriteria',
                  self._wsdl_types_map, True, 'CreativeAssetSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeTypes(self):
    """Returns the types of creatives.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    method_name = 'getCreativeTypes'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreatives(self, creative_search_criteria):
    """Returns a single page of creatives matching the given criteria.

    Args:
      creative_search_criteria: dict Search criteria to match creatives.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_search_criteria,
        'CreativeSearchCriteria')

    method_name = 'getCreatives'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_search_criteria, 'creativeSearchCriteria',
                  self._wsdl_types_map, True, 'CreativeSearchCriteria'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetCreativeRenderings(self, creative_rendering_request):
    """Returns the creative for a given id.

    Args:
      creative_rendering_request: str Request to see a creative rendering.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_rendering_request,
        'CreativeRenderingRequest')

    method_name = 'getCreativeRenderings'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_rendering_request, 'creativeRenderingRequest',
                  self._wsdl_types_map, True, 'CreativeRenderingRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def GetRichMediaPreviewURL(self, creative_id):
    """Returns generated default external preview URL for a rich media creative.

    Args:
      creative_id: str Id of the creative.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_id, (str, unicode)),))

    method_name = 'getRichMediaPreviewURL'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_id, 'id'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ReplaceRichMediaAsset(self, old_asset_file_name, replace_request):
    """Replaces a rich media asset for a rich media creative.

    Args:
      old_asset_file_name: str Name of asset to replace.
      replace_request: dict New asset to set.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((old_asset_file_name, (str, unicode)),))
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, replace_request, 'RichMediaAssetUploadRequest')

    method_name = 'replaceRichMediaAsset'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  old_asset_file_name, 'assetFileName')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                replace_request, 'replaceRequest',
                                self._wsdl_types_map, True,
                                'RichMediaAssetUploadRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def ReplaceRichMediaCreativePackage(self, creative_id, file_data):
    """Replaces the given creative package for the specified creative.

    Args:
      creative_id: str Id of the creative.
      file_data: str File content in bytes.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes(((creative_id, (str, unicode)),
                               (file_data, (str, unicode))))

    method_name = 'replaceRichMediaCreativePackage'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(creative_id, 'creativeId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                file_data, 'fileData'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreative(self, creative_base, campaign_id):
    """Saves the given creative.

    Args:
      creative_base: dict Creative to save.
      campaign_id: str Id of the campaign in which to save creative.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    DfaUtils.AssignCreativeXsi(creative_base)
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_base, 'CreativeBase')
    SanityCheck.ValidateTypes(((campaign_id, (str, unicode)),))

    method_name = 'saveCreative'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_base, 'creativeBase', self._wsdl_types_map, True,
                  'CreativeBase')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                campaign_id, 'campaignId'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def SaveCreativeAsset(self, creative_asset):
    """Saves the given creative asset.

    Args:
      creative_asset: dict Creative asset to save.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_asset, 'CreativeAsset')

    method_name = 'saveCreativeAsset'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_asset, 'creativeAsset', self._wsdl_types_map, True,
                  'CreativeAsset'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UploadCreativeFiles(self, creative_upload_request):
    """Uploads creative files in the given creative upload session.

    Args:
      creative_upload_request: dict Creative upload request.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, creative_upload_request, 'CreativeUploadRequest')

    method_name = 'uploadCreativeFiles'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  creative_upload_request, 'creativeUploadRequest',
                  self._wsdl_types_map, True, 'CreativeUploadRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UploadRichMediaAsset(self, upload_request):
    """Uploads a new rich media asset for a rich media creative.

    Args:
      upload_request: dict Rich media asset to upload

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, upload_request, 'RichMediaAssetUploadRequest')

    method_name = 'uploadRichMediaAsset'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(
                  upload_request, 'richMediaAssetUploadRequest',
                  self._wsdl_types_map, True, 'RichMediaAssetUploadRequest'))))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)

  def UploadRichMediaCreativePackage(self, advertiser_id, file_data,
                                     upload_as_flash_in_flash_creative):
    """Uploads the given rich media creative package.

    Args:
      advertiser_id: str Id of the advertiser.
      file_data: str File content.
      upload_as_flash_in_flash_creative: str Whether to upload Flash-In-Flash
                                         creative.

    Returns:
      tuple Response from the API method.

    Raises:
      ApiVersionNotSupportedError: Fails if the common framework is configured
                                   to use ZSI.
    """
    SanityCheck.ValidateTypes((
        (advertiser_id, (str, unicode)), (file_data, (str, unicode)),
        (upload_as_flash_in_flash_creative, (str, unicode))))

    method_name = 'uploadRichMediaCreativePackage'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(
          method_name, (self._sanity_check.SoappySanityCheck.UnType(
              self._message_handler.PackVarAsXml(advertiser_id,
                                                 'advertiserId')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                file_data, 'fileData')),
                        self._sanity_check.SoappySanityCheck.UnType(
                            self._message_handler.PackVarAsXml(
                                upload_as_flash_in_flash_creative,
                                'uploadAsFlashInFlashCreative', [], True)),))
    elif self._config['soap_lib'] == ZSI:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with ZSI toolkit.' % (Utils.GetCurrentFuncName(),
                                        self._op_config['version']))
      raise ApiVersionNotSupportedError(msg)
