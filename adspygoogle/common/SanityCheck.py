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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import ETREE
from adspygoogle.common import PYXML
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.Errors import ValidationError


# The BASE_TYPE_KEY and _SOAP_TYPE_KEY represent two keys that are required for
# all dictionary definitions of WSDL types. These dictionaries are referenced in
# the functions in this module.
BASE_TYPE_KEY = 'base_type'
_SOAP_TYPE_KEY = 'soap_type'
# The _SOAP_TYPE_VALIDATION_FUNCTIONS dictionary maps SOAP types from WSDL type
# definition dictionaries to the correct validation function. It is initialized
# later, after the functions have all been declared. Once a value has been set
# for it, it is treated as a constant.
_SOAP_TYPE_VALIDATION_FUNCTIONS = {}

def ValidateRequiredHeaders(headers, required_headers):
  """Sanity check for required authentication elements.

  The required headers may contain several possible header combinations, only
  one of which must be satisfied to make successful API request. In order for
  any single combination to be satisfied, all of the headers it specifies must
  exist as keys within the headers dict and each entry must contain data.

  Args:
    headers: A dict containing authentication headers.
    required_headers: A tuple containing valid combinations of headers. Each
                      combination of headers is represented as a tuple of
                      strings. e.g. (('Name', 'Password'), ('Name', 'Token'))

  Raises:
    ValidationError: The given authentication headers are not sufficient to make
                     requests against this API.
  """
  is_valid = False
  for headers_set in required_headers:
    is_valid_set = True
    for key in headers_set:
      if key not in headers or not headers[key]: is_valid_set = False
    if is_valid_set:
      is_valid = True
      break

  if not is_valid:
    msg = ('Required authentication header is missing. Valid options for '
           'headers are %s.' % str(required_headers))
    raise ValidationError(msg)


def IsConfigUserInputValid(user_input, valid_el):
  """Determines if user input within configuration scripts is valid.

  Each time a choice is presented to the user, a set of allowed values specific
  to that interaction is passed into this function.

  Args:
    user_input: The string of user input.
    valid_el: A list of valid elements for the current interaction.

  Returns:
    bool True if user input is valid, False otherwise.
  """
  if not user_input: return False

  try:
    valid_el.index(str(user_input))
  except ValueError:
    return False
  return True


def ValidateConfigSoapLib(soap_lib):
  """Checks that the SOAP library set in the configuration is a valid choice.

  Args:
    soap_lib: A string specifying which SOAP library to use.

  Raises:
    ValidationError: The given SOAP toolkit is not supported by this library.
  """
  if (not isinstance(soap_lib, str) or
      not IsConfigUserInputValid(soap_lib, [SOAPPY, ZSI])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(soap_lib), soap_lib, SOAPPY, ZSI))
    raise ValidationError(msg)


def ValidateConfigXmlParser(xml_parser):
  """Checks that the XML parser set in the configuration is a valid choice.

  Args:
    xml_parser: A string specifying which XML parser to use.

  Raises:
    ValidationError: The given XML parser is not supported by this library.
  """
  if (not isinstance(xml_parser, str) or
      not IsConfigUserInputValid(xml_parser, [PYXML, ETREE])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(xml_parser), xml_parser, PYXML, ETREE))
    raise ValidationError(msg)


def ValidateTypes(vars_tpl):
  """Checks that each variable in a set of variables is the correct type.

  Args:
    vars_tpl: A tuple containing a set of variables to check.

  Raises:
    ValidationError: The given object was not one of the given accepted types.
  """
  for var, var_types in vars_tpl:
    if not isinstance(var_types, tuple):
      var_types = (var_types,)
    for var_type in var_types:
      if isinstance(var, var_type):
        return
    msg = ('The \'%s\' is of type %s, expecting one of %s.'
           % (var, type(var), var_types))
    raise ValidationError(msg)


def ValidateOneLevelObject(obj):
  """Validates that a dict representing an object contains only string entries.

  Args:
    obj: A dictionary to validate.
  """
  ValidateTypes(((obj, dict),))
  for key in obj:
    if obj[key] != 'None': ValidateTypes(((obj[key], (str, unicode)),))


def ValidateOneLevelList(lst):
  """Validates that a list contains only string entries.

  Args:
    lst: A list to validate.
  """
  ValidateTypes(((lst, list),))
  for item in lst:
    if item != 'None': ValidateTypes(((item, (str, unicode)),))


def IsSuperType(wsdl_types, sub_type, super_type):
  """Determines if one type is a supertype of another type.

  Any case where the sub_type cannot be traced through to super_type is
  considered to be an invalid supertype. For example, if the WSDL definitions
  dictionary is empty or if one type's entry in the definitions does not include
  the required field (BASE_TYPE_KEY), these are not valid supertypes.

  Args:
    wsdl_types: A dict of WSDL-defined types in a single web service.
    sub_type: A string representing a type that may be extending super_type.
    super_type: A string representing a type that may be extended by sub_type.

  Returns:
    bool Whether super_type is really a supertype of sub_type.
  """
  if not wsdl_types or sub_type not in wsdl_types:
    return False
  while (sub_type != super_type and BASE_TYPE_KEY in wsdl_types[sub_type] and
         wsdl_types[sub_type][BASE_TYPE_KEY]):
    sub_type = wsdl_types[sub_type][BASE_TYPE_KEY]
  return sub_type == super_type


def _SanityCheckComplexType(wsdl_types, obj, xsi_type):
  """Validates a dict representing a complex type against its WSDL definition.

  Args:
    wsdl_types: A dict of WSDL-defined types in a single web service.
    obj: A dict that should represent an instance of the given type.
    xsi_type: A string specifying the name of a complex type defined in the
              WSDL.

  Raises:
    ValidationError: The given object is not an acceptable representation of the
                     given WSDL-defined complex type.
  """
  ValidateTypes(((obj, dict),))
  obj_contained_type, contained_type_key = Utils.GetExplicitType(wsdl_types,
                                                                 obj, xsi_type)

  if obj_contained_type and not obj_contained_type == xsi_type:
    if not IsSuperType(wsdl_types, obj_contained_type, xsi_type):
      raise ValidationError('Expecting type of \'%s\' but given type of class '
                            '\'%s\'.' % (xsi_type, obj_contained_type))
    xsi_type = obj_contained_type

  parameters = Utils.GenParamOrder(wsdl_types, xsi_type)
  for key in obj:
    if obj[key] is None or (obj_contained_type and key == contained_type_key):
      continue
    found = False
    for parameter, param_type in parameters:
      if parameter == key:
        found = True
        if Utils.IsXsdOrSoapenc(param_type):
          try:
            ValidateTypes(((obj[key], (str, unicode)),))
          except ValidationError:
            raise ValidationError('Field \'%s\' should be a string but value '
                                  '\'%s\' is a \'%s\' instead.' %
                                  (key, obj[key], type(obj[key])))
        else:
          NewSanityCheck(wsdl_types, obj[key], param_type)
        break
    if not found:
      raise ValidationError('Field \'%s\' is not in type \'%s\'.'
                            % (key, xsi_type))


def _SanityCheckSimpleType(wsdl_types, obj, xsi_type):
  """Validates a string representing a simple type against its WSDL definition.

  Args:
    wsdl_types: A dict of WSDL-defined types in a single web service.
    obj: String representing the given simple type.
    xsi_type: A string specifying the simple type name defined in the WSDL.

  Raises:
    ValidationError: The given object is not an acceptable representation of the
                     given WSDL-defined simple type.
  """
  try:
    ValidateTypes(((obj, (str, unicode)),))
  except ValidationError:
    raise ValidationError('Simple type \'%s\' should be a string but value '
                          '\'%s\' is a \'%s\' instead.' %
                          (xsi_type, obj, type(obj)))
  if obj not in wsdl_types[xsi_type]['allowed_values']:
    raise ValidationError('Value \'%s\' is not listed as an acceptable value '
                          'for type \'%s\'. Allowed values are: %s.' %
                          (obj, xsi_type,
                           wsdl_types[xsi_type]['allowed_values']))


def _SanityCheckArray(wsdl_types, obj, xsi_type):
  """Validates a list representing an array type against its WSDL definition.

  Args:
    wsdl_types: A dict of WSDL-defined types in a single web service.
    obj: List representing the given array type.
    xsi_type: A string specifying the array type name defined in the WSDL.
  """
  try:
    ValidateTypes(((obj, list),))
  except ValidationError:
    raise ValidationError('Type \'%s\' should be a list but value '
                          '\'%s\' is a \'%s\' instead.' %
                          (xsi_type, obj, type(obj)))
  if Utils.IsXsdOrSoapenc(wsdl_types[xsi_type][BASE_TYPE_KEY]):
    for item in obj:
      if item is None: continue
      try:
        ValidateTypes(((item, (str, unicode)),))
      except ValidationError:
        raise ValidationError('The items in array \'%s\' must all be strings. '
                              'Value \'%s\' is of type \'%s\'.'
                              % (xsi_type, item, type(item)))
  else:
    for item in obj:
      if item is None: continue
      NewSanityCheck(wsdl_types, item, wsdl_types[xsi_type][BASE_TYPE_KEY])


def NewSanityCheck(wsdl_types, obj, xsi_type):
  """Validates any given object against its WSDL definition.

  This method considers None and the empty string to be a valid representation
  of any type.

  Args:
    wsdl_types: A dict of WSDL-defined types in a single web service.
    obj: Object to be validated. Depending on the WSDL-defined type this object
         represents, the data type will vary. It should always be either a
         dictionary, list, or string no matter what WSDL-defined type it is.
    xsi_type: A string specifying the type name defined in the WSDL.

  Raises:
    ValidationError: The given WSDL-defined type has no definition in the WSDL
                     types map.
  """
  if obj in (None, ''):
    return
  if not xsi_type in wsdl_types or _SOAP_TYPE_KEY not in wsdl_types[xsi_type]:
    raise ValidationError('This type is not properly defined in the WSDL: %s.'
                          % xsi_type)

  if not _SOAP_TYPE_VALIDATION_FUNCTIONS:
    _SOAP_TYPE_VALIDATION_FUNCTIONS['simple'] = _SanityCheckSimpleType
    _SOAP_TYPE_VALIDATION_FUNCTIONS['complex'] = _SanityCheckComplexType
    _SOAP_TYPE_VALIDATION_FUNCTIONS['array'] = _SanityCheckArray

  soap_type = wsdl_types[xsi_type][_SOAP_TYPE_KEY]
  if soap_type in _SOAP_TYPE_VALIDATION_FUNCTIONS:
    _SOAP_TYPE_VALIDATION_FUNCTIONS[soap_type](wsdl_types, obj, xsi_type)
  else:
    raise ValidationError('Error in autogenerated WSDL definitions - Unknown '
                          'parameter type: %s' % soap_type)
