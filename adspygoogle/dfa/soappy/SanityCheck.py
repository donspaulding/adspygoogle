#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Validation and type conversion functions."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.dfa import DfaUtils
from adspygoogle.common import SanityCheck
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck


def ValidateAdvertiser(advertiser):
  """Valdidate Advertiser object.

  Args:
    advertiser: dict Advertiser object.
  """
  ValidateOneLevelObject(advertiser)


def ValidateAdvertiserSearchCriteria(criteria):
  """Validate AdvertiserSearchCriteria object.

  Args:
    criteria: dict AdvertiserSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('advertiserGroupIds', 'spotIds', 'ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateAdvertiserGroup(advertiser_group):
  """Valdidate AdvertiserGroup object.

  Args:
    advertiser_group: dict Advertiser group object.
  """
  ValidateOneLevelObject(advertiser_group)


def ValidateAdvertiserGroupSearchCriteria(criteria):
  """Validate AdvertiserGroupSearchCriteria object.

  Args:
    criteria: dict AdvertiserGroupSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateLandingPage(page):
  """Validate LandingPage object.

  Args:
    page: dict LandingPage object.
  """
  ValidateOneLevelObject(page)


def ValidateCampaignCopyRequest(request):
  """Validate CampaignCopyRequest object.

  Args:
    request: dict CampaignCopyRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateCampaignSearchCriteria(criteria):
  """Validate CampaignSearchCriteria object.

  Args:
    criteria: dict CampaignSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'advertiserIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder', 'archiveFilter'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateCampaignMigrationRequest(request):
  """Validate CampaignMigrationRequest object.

  Args:
    request: dict CampaignMigrationRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateCampaign(campaign):
  """Validate Campaign object.

  Args:
    campaign: dict Campaign object.
  """
  SanityCheck.ValidateTypes(((campaign, dict),))
  for key in campaign:
    if campaign[key] is None:
      continue
    elif key in ('creativeGroupIds', 'landingPageIds'):
      SanityCheck.ValidateOneLevelList(campaign[key])
    elif key in ('audienceSegmentGroups'):
      SanityCheck.ValidateTypes(((campaign[key], list),))
      for item in campaign[key]:
        if item is None:
          continue
        for sub_key in item:
          if sub_key in ('audienceSegements'):
            SanityCheck.ValidateTypes(((item[sub_key], list),))
            for sub_item in item[sub_key]:
              ValidateOneLevelObject(sub_item)
          else:
            SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
    elif key in ('lookbackWindow', 'reachReportConfiguration'):
      ValidateOneLevelObject(campaign[key])
    elif key in ('creativeOptimizationConfiguration'):
      SanityCheck.ValidateTypes(((campaign[key], dict),))
      for sub_key in campaign[key]:
        if campaign[key][sub_key] is None:
          continue
        if sub_key in ('spotlightActivities',):
          SanityCheck.ValidateTypes(((campaign[key][sub_key], list),))
          for item in campaign[key][sub_key]:
            if item is None:
              continue
            ValidateOneLevelObject(item)
        else:
          SanityCheck.ValidateTypes(((campaign[key][sub_key], (str, unicode)),))
    elif key in ('startDate', 'endDate'):
      campaign[key] = ValidateDateTime(campaign[key])
    else:
      SanityCheck.ValidateTypes(((campaign[key], (str, unicode)),))


def ValidateChangeLogRecordSearchCriteria(criteria):
  """Validate ChangeLogRecordSearchCriteria object.

  Args:
    criteria: dict ChangeLogRecordSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateChangePasswordRequest(request):
  """Validate ChangePasswordRequest object.

  Args:
    request: dict ChangePasswordRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateAd(ad):
  """Validate Ad object.

  Args:
    ad: dict Ad object.
  """
  SanityCheck.ValidateTypes(((ad, dict),))
  if ('xsi_type' not in ad):
    if ('typeId' in ad):
      ad['xsi_type'] = DfaUtils.GetAdXsiTypes()[ad['typeId']]
    else:
      msg = 'The type of the ad is missing.'
      raise ValidationError(msg)
  for key in ad:
    if ad[key] is None:
      continue
    if key in ('placementAssignments'):
      SanityCheck.ValidateTypes(((ad[key], list),))
      for item in ad[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    elif key in ('startTime', 'endTime'):
      ad[key] = ValidateDateTime(ad[key])
    elif key in ('clickThroughUrl', 'creativeGroupAssignment'):
      if ad['xsi_type'] not in ('ClickTracker', 'CreativeAd'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      ValidateOneLevelObject(ad[key])
    elif key in ('creativeAssignment'):
      if ad['xsi_type'] not in ('DefaultAd'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      ValidateCreativeAssignment(ad[key])
    elif key in ('creativeAssignments'):
      if ad['xsi_type'] not in ('TrackingAd', 'MobileAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], list),))
      for item in ad[key]:
        if item is None:
          continue
        ValidateCreativeAssignment(item)
    elif key in ('userLocalTime', 'ratio', 'priority', 'keywordExpression',
                 'hardCutOff', 'deliveryLimitEnabled', 'deliveryLimit'):
      if ad['xsi_type'] not in ('MobileAd', 'CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], (str, unicode)),))
    elif key in ('daysOfWeek', 'hoursOfDay'):
      if ad['xsi_type'] not in ('MobileAd', 'CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateOneLevelList(ad[key])
    elif key in ('mobilePlatforms'):
      if ad['xsi_type'] not in ('MobileAd'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], list),))
      for item in ad[key]:
        if item is None:
          continue
        ValidateOneLevelObject(ad[key])
    elif key in ('countryTargetingCriteria'):
      if ad['xsi_type'] not in ('MobileAd', 'CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], dict),))
      for sub_key in ad[key]:
        if ad[key][sub_key] is None:
          continue
        if sub_key in ('countries',):
          SanityCheck.ValidateTypes(((ad[key][sub_key], list),))
          for item in ad[key][sub_key]:
            if item is None:
              continue
            ValidateOneLevelObject(item)
        else:
          SanityCheck.ValidateTypes(((ad[key][sub_key], (str, unicode)),))
    elif key in ('ISPs', 'OSPs', 'areaCodes', 'bandwidths', 'cities',
                 'designatedMarketAreas', 'domainNames', 'domainTypes',
                 'operatingSystems', 'states'):
      if ad['xsi_type'] not in ('CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], list),))
      for item in ad[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    elif key in ('browserVersions'):
      if ad['xsi_type'] not in ('CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], list),))
      for item in ad[key]:
        if item is None:
          continue
        SanityCheck.ValidateTypes(((item, dict),))
        for sub_key in item:
          if item[sub_key] is None:
            continue
          if sub_key in ('browser'):
            ValidateOneLevelObject(item[sub_key])
          else:
            SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
    elif key in ('audienceSegmentId', 'costType', 'frequencyCap',
                 'frequencyCapPeriod'):
      if ad['xsi_type'] not in ('CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], (str, unicode)),))
    elif key in ('userListExpression'):
      if ad['xsi_type'] not in ('CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      ValidateOneLevelObject(ad[key])
    elif key in ('postalCodes'):
      if ad['xsi_type'] not in ('CreativeAd', 'RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateOneLevelList(ad[key])
    elif key in ('creativeId'):
      if ad['xsi_type'] not in ('CreativeAd'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], (str, unicode)),))
    elif key in ('rotationType', 'creativeOptimizationEnabled'):
      if ad['xsi_type'] not in ('RotationGroup'):
        msg = 'Field "%s" is not in ad type "%s".' % (key, ad['xsi_type'])
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((ad[key], (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((ad[key], (str, unicode)),))


def ValidateCreativeAssignment(creative_assignment):
  """Valdidate CreativeAssignment object.

  Args:
    creative_assignment: dict CreativeAssignment object.
  """
  SanityCheck.ValidateTypes(((creative_assignment, dict),))
  for key in creative_assignment:
    if creative_assignment[key] is None:
      continue
    elif key in ('endDate', 'startDate'):
      creative_assignment[key] = ValidateDateTime(creative_assignment[key])
    elif key in ('clickThroughUrl', 'creativeGroupAssignment'):
      ValidateOneLevelObject(creative_assignment[key])
    elif key in ('richMediaExitOverrides'):
      SanityCheck.ValidateTypes(((creative_assignment[key], list),))
      for item in creative_assignment[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    else:
      SanityCheck.ValidateTypes(((creative_assignment[key], (str, unicode)),))


def ValidateContentCategory(content_category):
  """Valdidate ContentCategory object.

  Args:
    content_category: dict ContentCategory object.
  """
  SanityCheck.ValidateTypes(((content_category, dict),))
  for key in content_category:
    if content_category[key] is None:
      continue
    SanityCheck.ValidateTypes(((content_category[key], (str, unicode)),))


def ValidateCreativeField(creative_field):
  """Valdidate CreativeField object.

  Args:
    creative_field: dict CreativeField object.
  """
  ValidateOneLevelObject(creative_field)


def ValidateCreativeFieldValue(creative_field_value):
  """Valdidate CreativeFieldValue object.

  Args:
    creative_field_value: dict CreativeFieldValue object.
  """
  ValidateOneLevelObject(creative_field_value)


def ValidateCreativeFieldSearchCriteria(criteria):
  """Valdidate CreativeFieldSearchCritera object.

  Args:
    criteria: dict CreativeFieldSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'advertiserIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateCreativeFieldValueSearchCriteria(criteria):
  """Valdidate CreativeFieldValueSearchCritera object.

  Args:
    criteria: dict CreativeFieldValueSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'creativeFieldIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateCreativeGroup(creative_group):
  """Valdidate CreativeGroup object.

  Args:
    creative_group: dict CreativeGroup object.
  """
  ValidateOneLevelObject(creative_group)


def ValidateCreativeGroupSearchCriteria(criteria):
  """Valdidate CreativeGroupSearchCritera object.

  Args:
    criteria: dict CreativeGroupSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'advertiserIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateSizeSearchCriteria(criteria):
  """Valdidate SizeSearchCritera object.

  Args:
    criteria: dict SizeSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidatePlacementStrategy(placement_strategy):
  """Valdidate PlacementStrategy object.

  Args:
    placement_strategy: dict PlacementStrategy object.
  """
  ValidateOneLevelObject(placement_strategy)


def ValidatePlacementStrategySearchCriteria(criteria):
  """Valdidate PlacementStrategySearchCriteria object.

  Args:
    criteria: dict PlacementStrategySearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateUserSearchCriteria(criteria):
  """Valdidate UserSearchCriteria object.

  Args:
    criteria: dict UserSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder', 'activeFilter'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateUser(user):
  """Valdidate User object.

  Args:
    criteria: dict User object.
  """
  SanityCheck.ValidateTypes(((user, dict),))
  for key in user:
    if user[key] is None:
      continue
    if key in ('advertiserUserFilter', 'campaignUserFilter', 'siteUserFilter',
                 'userRoleUserFilter'):
      SanityCheck.ValidateTypes(((user[key], dict),))
      for sub_key in user[key]:
        if sub_key in ('objectFilters'):
          if user[key][sub_key] is None:
            continue
          SanityCheck.ValidateTypes(((user[key][sub_key], list),))
          for item in user[key][sub_key]:
            ValidateOneLevelObject(item)
        else:
          SanityCheck.ValidateTypes(((user[key][sub_key], (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((user[key], (str, unicode)),))


def ValidateUserRole(user_role):
  """Valdidate UserRole object.

  Args:
    user: dict UserRole object.
  """
  SanityCheck.ValidateTypes(((user_role, dict),))
  for key in user_role:
    if user_role[key] is None:
      continue
    if key in ('permissions'):
      SanityCheck.ValidateTypes(((user_role[key], list),))
      for item in user_role[key]:
        ValidatePermission(item)
    else:
      SanityCheck.ValidateTypes(((user_role[key], (str, unicode)),))


def ValidatePermission(permission):
  """Valdidate Permission object.

  Args:
    permission: dict Permission object.
  """
  SanityCheck.ValidateTypes(((permission, dict),))
  for key in permission:
    if key in ('permissionGroup'):
      ValidateOneLevelObject(permission[key])
    else:
      SanityCheck.ValidateTypes(((permission[key], (str, unicode)),))


def ValidateUserRoleSearchCriteria(criteria):
  """Valdidate UserRoleSearchCriteria object.

  Args:
    user_role: dict UserRoleSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateSubnetwork(subnetwork):
  """Valdidate Subnetwork object.

  Args:
    subnetwork: dict Subnetwork object.
  """
  SanityCheck.ValidateTypes(((subnetwork, dict),))
  for key in subnetwork:
    if subnetwork[key] is None:
      continue
    if key in ('availablePermissions'):
      SanityCheck.ValidateOneLevelList(subnetwork[key])
    else:
      SanityCheck.ValidateTypes(((subnetwork[key], (str, unicode)),))


def ValidateSubnetworkSearchCriteria(criteria):
  """Valdidate SubnetworkSearchCriteria object.

  Args:
    criteria: dict SubnetworkSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidatePlacement(placement):
  """Valdidate Placement object.

  Args:
    placement: dict Placement object.
  """
  SanityCheck.ValidateTypes(((placement, dict),))
  for key in placement:
    if placement[key] is None:
      continue
    elif key in ('tagSettings'):
      SanityCheck.ValidateTypes(((placement[key], dict),))
      for sub_key in placement[key]:
        if placement[key][sub_key] is None:
          continue
        if sub_key in ('tagTypes'):
          SanityCheck.ValidateOneLevelList(placement[key][sub_key])
        else:
          SanityCheck.ValidateTypes(((placement[key][sub_key],
                                      (str, unicode)),))
    elif key in ('pricingSchedule'):
      ValidatePricingSchedule(placement[key])
    elif key in ('lookbackWindow'):
      ValidateOneLevelObject(placement[key])
    else:
      SanityCheck.ValidateTypes(((placement[key], (str, unicode)),))


def ValidatePricingSchedule(pricing_schedule):
  """Valdidate PricingSchedule object.

  Args:
    pricing_schedule: dict PricingSchedule object.
  """
  SanityCheck.ValidateTypes(((pricing_schedule, dict),))
  for key in pricing_schedule:
    if key in ('pricingPeriods'):
      SanityCheck.ValidateTypes(((pricing_schedule[key], list),))
      for pricing_period in pricing_schedule[key]:
        ValidatePricingPeriod(pricing_period)
    elif key in ('endDate', 'startDate', 'testingStartDate'):
      pricing_schedule[key] = ValidateDateTime(pricing_schedule[key])
    else:
      SanityCheck.ValidateTypes(((pricing_schedule[key], (str, unicode)),))


def ValidatePricingPeriod(pricing_period):
  """Valdidate PricingPeriod object.

  Args:
    pricing_period: dict PricingPeriod object.
  """
  SanityCheck.ValidateTypes(((pricing_period, dict),))
  for key in pricing_period:
    if pricing_period[key] is None:
      continue
    elif key in ('endDate', 'startDate'):
      pricing_period[key] = ValidateDateTime(pricing_period[key])
    elif key in ('rateOrCost'):
      SanityCheck.ValidateTypes(((pricing_period[key], (str, unicode, float)),))
      if isinstance(pricing_period[key], float):
        pricing_period[key] = '%s' % pricing_period[key]
    else:
      SanityCheck.ValidateTypes(((pricing_period[key], (str, unicode)),))


def ValidatePlacementGroup(placement_group):
  """Valdidate PlacementGroup object.

  Args:
    placement_group: dict PlacementGroup object.
  """
  SanityCheck.ValidateTypes(((placement_group, dict),))
  for key in placement_group:
    if placement_group[key] is None:
      continue
    elif key in ('placementIds'):
      SanityCheck.ValidateOneLevelList(placement_group[key])
    elif key in ('pricingSchedule'):
      ValidatePricingSchedule(placement_group[key])
    else:
      SanityCheck.ValidateTypes(((placement_group[key], (str, unicode)),))


def ValidatePlacementUpdateRequest(placement_update_request):
  """Validate PlacementUpdateRequest object.

  Args:
    placement_update_request: dict PlacementUpdateRequest object.
  """
  SanityCheck.ValidateTypes(((placement_update_request, dict),))
  for key in placement_update_request:
    if key in ('endDate', 'startDate'):
      placement_update_request[key] = ValidateDateTime(
                                          placement_update_request[key])
    else:
      SanityCheck.ValidateTypes(((placement_update_request[key],
                                  (str, unicode)),))


def ValidatePlacementGroupSearchCriteria(criteria):
  """Valdidate PlacementGroupSearchCriteria object.

  Args:
    criteria: dict PlacementGroupSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'campaignIds', 'dfaSiteIds', 'placementStrategyIds',
               'pricingTypeIds', 'siteIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder', 'archiveFilter', 'endDateRange',
                 'startDateRange'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidatePlacementSearchCriteria(criteria):
  """Valdidate PlacementSearchCriteria object.

  Args:
    criteria: dict PlacementSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'campaignIds', 'dfaSiteIds', 'placementStrategyIds',
               'placementTypeIds', 'pricingTypeIds', 'siteIds', 'sizeIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder', 'archiveFilter', 'endDateRange',
                 'startDateRange'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidatePlacementTagCriteria(criteria):
  """Validate PlacementTagCriteria object.

  Args:
    criteria: dict PlacementTagCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('tagOptionIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateSpotlightActivityGroup(activity_group):
  """Valdidate SpotlightActivityGroup object.

  Args:
    activity_group: dict SpotlightActivityGroup object.
  """
  for key in activity_group:
    if activity_group[key] is None:
      continue
    else:
      SanityCheck.ValidateTypes(((activity_group[key], (str, unicode)),))


def ValidateSpotlightActivityGroupSearchCriteria(criteria):
  """Validate SpotlightActivityGroupSearchCriteria object.

  Args:
    criteria: dict SpotlightActivityGroupSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateSpotlightActivity(activity):
  """Valdidate SpotlightActivity object.

  Args:
    activity: dict SpotlightActivity object.
  """
  SanityCheck.ValidateTypes(((activity, dict),))
  for key in activity:
    if activity[key] is None:
      continue
    elif key in ('assignedCustomSpotlightVariableIds'):
      SanityCheck.ValidateOneLevelList(activity[key])
    elif key in ('publisherTags', 'defaultFloodlightTags'):
      SanityCheck.ValidateTypes(((activity[key], list),))
      for item in activity[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    elif key in ('tagProperty'):
      ValidateOneLevelObject(activity[key])
    else:
      SanityCheck.ValidateTypes(((activity[key], (str, unicode)),))


def ValidateSpotlightActivitySearchCriteria(criteria):
  """Validate SpotlightActivitySearchCriteria object.

  Args:
    criteria: dict SpotlightActivitySearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'spotlightActivityGroupIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateCountriesSearchCriteria(criteria):
  """Validate CountriesSearchCriteria object.

  Args:
    criteria: dict CountriesSearchCriteria object.
  """
  ValidateOneLevelObject(criteria)


def ValidateNetworkSearchCriteria(criteria):
  """Validate NetworkSearchCriteria object.

  Args:
    criteria: dict NetworkSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder', 'activeFilter'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateNetwork(network):
  """Validate Network object.

  Args:
    network: dict Network object.
  """
  SanityCheck.ValidateTypes(((network, dict),))
  for key in network:
    if network[key]:
      continue
    elif key in ('availablePermissions', 'networkPermissions'):
      SanityCheck.ValidateOneLevelList(network[key])
    elif key in ('widgetNetworkConfig'):
      for sub_key in network[key]:
        if network[key][sub_key] is None:
          continue
        else:
          SanityCheck.ValidateTypes(((network[key][sub_key], (str, unicode)),))
    elif key in ('frequencyCapGroups'):
      SanityCheck.ValidateTypes(((network[key], list),))
      for item in network[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    elif key in ('richmediaNetworkConfig'):
      ValidateRichmediaNetworkConfiguration(network[key])
    elif key in ('reportsConfiguration'):
      ValidateReportsConfiguration(network[key])
    else:
      SanityCheck.ValidateTypes(((network[key], (str, unicode)),))


def ValidateReportsConfiguration(config):
  """Validate ReportsConfiguration object.

  Args:
    config: dict ReportsConfiguration object.
  """
  SanityCheck.ValidateTypes(((config, dict),))
  for key in config:
    if key in ('advancedReportsConfiguration', 'reachReportConfiguration',
               'exposureToConversionConfiguration', 'lookbackConfiguration'):
      ValidateOneLevelObject(config[key])
    else:
      SanityCheck.ValidateTypes(((config[key], (str, unicode)),))


def ValidateRichmediaNetworkConfiguration(config):
  """Validate RichmediaNetworkConfiguration object.

  Args:
    config: dict RichmediaNetworkConfiguration object.
  """
  SanityCheck.ValidateTypes(((config, dict),))
  for key in config:
    if key in ('billingCustomer'):
      for sub_key in config[key]:
        if config[key][sub_key] is None:
          continue
        elif sub_key in ('expirationDate'):
          config[key][sub_key] = ValidateDateTime(config[key][sub_key])
        else:
          SanityCheck.ValidateTypes(((config[key][sub-key], (str, unicode)),))
    elif key in ('dateAssigned'):
      config[key] = ValidateDateTime(config[key])
    else:
      SanityCheck.ValidateTypes(((config[key], (str, unicode)),))


def ValidateDfaSite(dfa_site):
  """Validate DfaSite object.

  Args:
    dfa_site: dict DfaSite object.
  """
  SanityCheck.ValidateTypes(((dfa_site, dict),))
  for key in dfa_site:
    if dfa_site[key] is None:
      continue
    elif key in ('lookbackWindow'):
      ValidateOneLevelObject(dfa_site[key])
    elif key in ('tagSettings', 'richMediaSettings'):
      for sub_key in dfa_site[key]:
        if dfa_site[key][sub_key] is None:
          continue
        else:
          SanityCheck.ValidateTypes(((dfa_site[key][sub_key], (str, unicode)),))
    elif key in ('dfaSiteContact'):
      SanityCheck.ValidateTypes(((dfa_site[key], list),))
      for item in dfa_site[key]:
        if item is None:
          continue
        for sub_key in item:
          if item[sub_key] is None:
            continue
          else:
            SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((dfa_site[key], (str, unicode)),))


def ValidateDfaSiteSearchCriteria(criteria):
  """Validate DfaSiteSearchCriteria object.

  Args:
    criteria: dict DfaSiteSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('SDSiteIds', 'campaignIds', 'ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateSiteSearchCriteria(criteria):
  """Validate SiteSearchCriteria object.

  Args:
    criteria: dict SiteSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateContactSearchCriteria(criteria):
  """Validate ContactSearchCriteria object.

  Args:
    criteria: dict ValidateContactSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'siteDirectorySiteIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('sortOrder'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateSiteDirectoryDfaSiteMappingRequest(mapping_request):
  """Validate SiteDirectoryDfaSiteMappingRequest object.

  Args:
    mapping_request: dict SiteDirectoryDfaSiteMappingRequest object.
  """
  ValidateOneLevelObject(mapping_request)


def ValidateCreativeAsset(creative_asset):
  """Validate CreativeAsset object.

  Args:
    creative_asset: dict CreativeAsset object.
  """
  ValidateOneLevelObject(creative_asset)


def ValidateCreativeAssetSearchCriteria(criteria):
  """Validate CreativeAssetSearchCriteria object.

  Args:
    criteria: dict CreativeAssetSearchCriteria object.
  """
  ValidateOneLevelObject(criteria)


def ValidateCreativeBase(creative_base):
  """Validate CreativeBase object.

  Args:
    creative_base: dict CreativeBase object.
  """
  SanityCheck.ValidateTypes(((creative_base, dict),))
  if ('xsi_type' not in creative_base):
    if ('typeId' in creative_base):
      creative_base['xsi_type'] = DfaUtils.GetCreativeXsiTypes()[
                                      creative_base['typeId']]
    else:
      msg = 'The type of the creative is missing.'
      raise ValidationError(msg)
  for key in creative_base:
    if creative_base[key] is None:
      continue
    elif key in ('creativeFieldAssignments'):
      SanityCheck.ValidateTypes(((creative_base[key], list),))
      for item in creative_base[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    elif key in ('creativeAssets'):
      if creative_base['xsi_type'] not in ('FlashInpageCreative',
                                           'HTMLCreative',
                                           'HTMLInterstitialCreative',
                                           'MobileDisplayCreative',
                                           'TrackingHTMLCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], list),))
      for item in creative_base[key]:
        if item is None:
          continue
        ValidateOneLevelObject(item)
    elif key in ('HTMLCode'):
      if creative_base['xsi_type'] not in ('FlashInpageCreative',
                                           'HTMLCreative',
                                           'HTMLInterstitialCreative',
                                           'MobileDisplayCreative',
                                           'TrackingHTMLCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('wmode', 'surveyUrl', 'codeLocked', 'backupImageAlternateText',
                 'backupImageClickThroughUrl', 'backgroundColor',
                 'allowedScriptAccess'):
      if creative_base['xsi_type'] not in ('FlashInpageCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('backupImageTargetWindow'):
      if creative_base['xsi_type'] not in ('FlashInpageCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateOneLevelObject(creative_base[key])
    elif key in ('parentFlashAsset', 'FSCommand', 'backupImageAsset'):
      if creative_base['xsi_type'] not in ('FlashInpageCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], dict),))
      for sub_key in creative_base[key]:
        if creative_base[key][sub_key] is None:
          continue
        elif sub_key in ('frameSize', 'windowDimensions'):
          ValidateOneLevelObject(creative_base[key][sub_key])
        elif sub_key in ('clickTags'):
          SanityCheck.ValidateTypes(((creative_base[key][sub_key], list),))
          for item in creative_base[key][sub_key]:
            if item is None:
              continue
            ValidateOneLevelObject(item)
        else:
          SanityCheck.ValidateTypes(((creative_base[key][sub_key],
                                      (str, unicode)),))
    elif key in ('clickTags'):
      if creative_base['xsi_type'] not in ('FlashInpageCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
        SanityCheck.ValidateTypes(((creative_base[key][sub_key], list),))
        for item in creative_base[key]:
          if item is None:
            continue
          ValidateOneLevelObject(item)
    elif key in ('thirdPartyClickTrackingUrl',
                 'thirdPartyImpressionTrackingUrl'):
      if creative_base['xsi_type'] not in ('MobileDisplayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('assetFilename', 'alternateText'):
      if creative_base['xsi_type'] not in ('ImageCreative',
                                           'TrackingImageCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('redirectUrl'):
      if creative_base['xsi_type'] not in ('InternalRedirectCreative',
                                         'InterstitialInternalRedirectCreative',
                                         'RedirectCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('videoLength', 'type', 'totalFileSize',
                 'thirdPartyImpressionUrl', 'thirdPartyFlashImpressionUrl',
                 'thirdPartyClickUrl', 'thirdPartyBackupImageImpressionUrl',
                 'surveyUrl', 'requiredFlashPlayerVersion', 'placementWidth',
                 'placementHeight', 'metaData', 'interstitial', 'flashInFlash',
                 'customKeyValues', 'comments', 'authoringApplication',
                 'adRequestKeys', 'actionScriptVersion'):
      if creative_base['xsi_type'] not in (
          'RichMediaExpandingCreative', 'RichMediaFlashInFlashCreative',
          'RichMediaFloatingCreative', 'RichMediaFloatingWithReminderCreative',
          'RichMediaImageWithFloatingCreative',
          'RichMediaImageWithOverlayCreative', 'RichMediaInPageCreative',
          'RichMediaInPageWithFloatingCreative',
          'RichMediaInPageWithOverlayCreative', 'RichMediaOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('createdDate'):
      if creative_base['xsi_type'] not in (
          'RichMediaExpandingCreative', 'RichMediaFlashInFlashCreative',
          'RichMediaFloatingCreative', 'RichMediaFloatingWithReminderCreative',
          'RichMediaImageWithFloatingCreative',
          'RichMediaImageWithOverlayCreative', 'RichMediaInPageCreative',
          'RichMediaInPageWithFloatingCreative',
          'RichMediaInPageWithOverlayCreative', 'RichMediaOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      creative_base[key] = ValidateDateTime(creative_base[key])
    elif key in ('childAssets', 'counterEvents', 'timerEvent'):
      if creative_base['xsi_type'] not in (
          'RichMediaExpandingCreative', 'RichMediaFlashInFlashCreative',
          'RichMediaFloatingCreative', 'RichMediaFloatingWithReminderCreative',
          'RichMediaImageWithFloatingCreative',
          'RichMediaImageWithOverlayCreative', 'RichMediaInPageCreative',
          'RichMediaInPageWithFloatingCreative',
          'RichMediaInPageWithOverlayCreative', 'RichMediaOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], list),))
      for item in creative_base[key]:
        if item is None:
          continue
        SanityCheck.ValidateTypes(((item, dict),))
        for sub_key in item:
          SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
    elif key in ('exitEvents'):
      if creative_base['xsi_type'] not in (
          'RichMediaExpandingCreative', 'RichMediaFlashInFlashCreative',
          'RichMediaFloatingCreative', 'RichMediaFloatingWithReminderCreative',
          'RichMediaImageWithFloatingCreative',
          'RichMediaImageWithOverlayCreative', 'RichMediaInPageCreative',
          'RichMediaInPageWithFloatingCreative',
          'RichMediaInPageWithOverlayCreative', 'RichMediaOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], list),))
      for item in creative_base[key]:
        if item is None:
          continue
        SanityCheck.ValidateTypes(((item, dict),))
        for sub_key in item:
          if sub_key in ('exitWindowProperties'):
            ValidateOneLevelObject(item[sub_key])
          else:
            SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
    elif key in ('assetType'):
      if creative_base['xsi_type'] not in ('RichMediaFlashInFlashCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))
    elif key in ('flashAsset'):
      if creative_base['xsi_type'] not in ('RichMediaFlashInFlashCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      SanityCheck.ValidateTypes(((creative_base[key], dict),))
    elif key in ('floatingAsset'):
      if creative_base['xsi_type'] not in (
          'RichMediaFloatingCreative',
          'RichMediaImageWithFloatingCreative',
          'RichMediaFloatingWithReminderCreative',
          'RichMediaInPageWithFloatingCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateOneLevelObject(creative_base['key'])
    elif key in ('reminderAsset'):
      if creative_base['xsi_type'] not in (
          'RichMediaFloatingWithReminderCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateOneLevelObject(creative_base['key'])
    elif key in ('imageAsset'):
      if creative_base['xsi_type'] not in ('RichMediaImageWithFloatingCreative',
                                           'RichMediaImageWithOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateRichMediaImageAsset(creative_base['key'])
    elif key in ('overlayAsset'):
      if creative_base['xsi_type'] not in ('RichMediaImageWithOverlayCreative',
                                           'RichMediaInPageWithOverlayCreative',
                                           'RichMediaOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateOneLevelObject(creative_base['key'])
    elif key in ('inPageAsset'):
      if creative_base['xsi_type'] not in ('RichMediaExpandingCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateRichMediaInPageAsset(creative_base['key'])
    elif key in ('expandingAsset'):
      if creative_base['xsi_type'] not in (
          'RichMediaInPageCreative', 'RichMediaInPageWithFloatingCreative',
          'RichMediaInPageWithOverlayCreative'):
        msg = ('Field "%s" is not in creative type "%s".'
               % (key, creative_base['xsi_type']))
        raise ValidationError(msg)
      ValidateRichMediaExpandingAsset(creative_base['key'])
    else:
      SanityCheck.ValidateTypes(((creative_base[key], (str, unicode)),))


def ValidateRichMediaImageAsset(image_asset):
  """Validate RichMediaImageAsset object.

  Args:
    image_asset: dict RichMediaImageAsset object.
  """
  SanityCheck.ValidateTypes(((image_asset, dict),))
  for key in image_asset:
    if image_asset[key] is None:
      continue
    elif key in ('exitEvent'):
      SanityCheck.ValidateTypes(((image_asset[key], dict),))
      for sub_key in image_asset[key]:
        if image_asset[key][sub_key] is None:
          continue
        elif sub_key in ('exitWindowProperties'):
          ValidateOneLevelObject(image_asset[key][sub_key])
        else:
          SanityCheck.ValidateTypes(((image_asset[key][sub_key],
                                      (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((image_asset[key], (str, unicode)),))


def ValidateRichMediaInPageAsset(in_page_asset):
  """Validate RichMediaInPageAsset object.

  Args:
    in_page_asset: dict RichMediaInPageAsset object.
  """
  SanityCheck.ValidateTypes(((in_page_asset, dict),))
  for key in in_page_asset:
    if in_page_asset[key] is None:
      continue
    elif key in ('alternateImageAsset'):
      ValidateRichMediaImageAsset(in_page_asset[key])
    else:
      SanityCheck.ValidateTypes(((in_page_asset[key], (str, unicode)),))


def ValidateRichMediaExpandingAsset(expanding_asset):
  """Validate RichMediaExpandingAsset object.

  Args:
    expanding_asset: dict RichMediaExpandingAsset object.
  """
  SanityCheck.ValidateTypes(((expanding_asset, dict),))
  for key in expanding_asset:
    if expanding_asset[key] is None:
      continue
    elif key in ('alternateImageAsset'):
      ValidateRichMediaImageAsset(expanding_asset[key])
    elif key in ('pushdownAnimationTime'):
      SanityCheck.ValidateTypes(((expanding_asset[key],
                                  (str, unicode, float)),))
      if isinstance(expanding_asset[key], float):
        expanding_asset[key] = '%s' % expanding_asset[key]
    else:
      SanityCheck.ValidateTypes(((expanding_asset[key], (str, unicode)),))


def ValidateCreativePlacementAssignment(assignment):
  """Validate CreativePlacementAssignment object.

  Args:
    assignment: dict CreativePlacementAssignment object.
  """
  SanityCheck.ValidateTypes(((assignment, dict),))
  for key in assignment:
    if (key in ('placementIds') and not key in ('placementId')):
      SanityCheck.ValidateOneLevelList(assignment[key])
    else:
      SanityCheck.ValidateTypes(((assignment[key], (str, unicode)),))


def ValidateCreativeCopyRequest(request):
  """Validate CreativeCopyRequest object.

  Args:
    request: dict CreativeCopyRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateCreativeUploadSessionRequest(request):
  """Validate CreativeUploadSessionRequest object.

  Args:
    request: dict CreativeUploadSessionRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateCreativeUploadRequest(request):
  """Validate CreativeUploadRequest object.

  Args:
    request: dict CreativeUploadRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('rawFiles'):
      SanityCheck.ValidateTypes(((request[key], list),))
      for item in request[key]:
        ValidateOneLevelObject(item)
    else:
      ValidateOneLevelObject(request[key])


def ValidateCreativeUploadSession(session):
  """Validate CreativeUploadSession object.

  Args:
    session: dict CreativeUploadSession object.
  """
  SanityCheck.ValidateTypes(((session, dict),))
  for key in session:
    if session[key] is None:
      continue
    elif key in ('fileCount'):
      ValidateOneLevelObject(session[key])
    elif key in ('creativeSaveRequests', 'uploadedFiles'):
      SanityCheck.ValidateTypes(((session[key], list),))
      for item in session[key]:
        if item is None:
          continue
        SanityCheck.ValidateTypes(((item, dict),))
        for sub_key in item:
          if item[sub_key] is None:
            continue
          if sub_key in ('flashFile', 'imageFile', 'dimensions'):
            ValidateOneLevelObject(item[sub_key])
          elif sub_key in ('matchedFiles'):
            SanityCheck.ValidateTypes(((item[sub_key], list),))
            for sub_item in item[sub_key]:
              if sub_item is None:
                continue
              ValidateOneLevelObject(sub_item)
          else:
            SanityCheck.ValidateTypes(((item[sub_key], (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((session[key], (str, unicode)),))


def ValidateRichMediaAssetUploadRequest(request):
  """Validate RichMediaAssetUploadRequest object.

  Args:
    request: dict RichMediaAssetUploadRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateCreativeRenderingRequest(request):
  """Validate CreativeRenderingRequest object.

  Args:
    request: dict CreativeRenderingRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('creativeIds'):
      SanityCheck.ValidateOneLevelList(request[key])
    else:
      SanityCheck.ValidateTypes(((request[key], (str, unicode)),))


def ValidateCitySearchCriteria(criteria):
  """Validate CitySearchCriteria object.

  Args:
    criteria: dict CitySearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
      SanityCheck.ValidateOneLevelList(criteria[key])


def ValidateUserListSearchCriteria(criteria):
  """Validate UserListSearchCriteria object.

  Args:
    criteria: dict UserListSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'userListGroupIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateDomainNameSearchCriteria(criteria):
  """Validate DomainNameSearchCriteria object.

  Args:
    criteria: dict DomainNameSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateAssociationUpdateRequest(request):
  """Validate AssociationUpdateRequest object.

  Args:
    request: dict AssociationUpdateRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('adIds', 'propertiesToUpdate'):
      SanityCheck.ValidateOneLevelList(request[key])
    else:
      SanityCheck.ValidateTypes(((request[key], (str, unicode)),))


def ValidateOverridableAdProperties(request):
  """Validate OverridableAdProperties object.

  Args:
    request: dict OverridableAdProperties object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    ValidateOneLevelObject(request[key])


def ValidateAdSearchCriteria(criteria):
  """Validate AdSearchCriteria object.

  Args:
    criteria: dict AdSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids', 'sizeIds', 'typeIds'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('activeFilter'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateAdCopyRequest(request):
  """Validate AdCopyRequest object.

  Args:
    request: dict AdCopyRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateCreativeSearchCriteria(criteria):
  """Validate AdSearchCriteria object.

  Args:
    criteria: dict AdSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('ids'):
      SanityCheck.ValidateOneLevelList(criteria[key])
    elif key in ('activeFilter', 'creativeCreationDateRange'):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateUserInvitationEmailRequest(request):
  """Validate AdCopyRequest object.

  Args:
    request: dict AdCopyRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateSiteDirectorySiteImportRequest(request):
  """Validate SiteDirectorySiteImportRequest object.

  Args:
    request: dict SiteDirectorySiteImportRequest object.
  """
  ValidateOneLevelObject(request)


def ValidateDateTime(date_time):
  """Validate DateTime object.

  Args:
    date_time: dict DateTime object.
  """
  SanityCheck.ValidateTypes(((date_time, (str, unicode, tuple)),))
  if isinstance(date_time, (str, unicode)):
    return date_time
  else:
    date_time = '%04s-%02d-%02dT%02d:%02d:%02d' % (
        date_time[0], date_time[1], date_time[2], date_time[3], date_time[4],
        date_time[5])
    return date_time


def ValidateOneLevelObject(obj):
  """Validate object with one level of complexity. The DFA version allows
  NoneTypes.

  Args:
    obj: dict Object to validate.
  """
  SanityCheck.ValidateTypes(((obj, dict),))
  for key in obj:
    if obj[key] is not None:
      SanityCheck.ValidateTypes(((obj[key], (str, unicode)),))


def ValidateReportSearchCriteria(criteria):
  """Validate ReportSearchCriteria object.

  Args:
    criteria: dict ReportSearchCriteria object.
  """
  SanityCheck.ValidateTypes(((criteria, dict),))
  for key in criteria:
    if key in ('interval',):
      ValidateOneLevelObject(criteria[key])
    else:
      SanityCheck.ValidateTypes(((criteria[key], (str, unicode)),))


def ValidateReportRequest(request):
  """Validate ReportRequest object.

  Args:
    request: dict ReportRequest object.
  """
  ValidateOneLevelObject(request)
