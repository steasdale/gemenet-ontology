#!/usr/bin/env python3
"""
P70.3 Indicates Transferred Object - Transformation Code

This module provides transformation functions for converting the GMN shortcut property
gmn:P70_3_indicates_transferred_object to full CIDOC-CRM compliant structure using
the E13 Attribute Assignment pattern.

To integrate into gmn_to_cidoc_transform.py:
1. Copy all functions from this file
2. Add to AAT_CONSTANTS section
3. Add transform calls to transform_item() function
4. Test with sample data

Version: 1.0
Created: 2025-10-28
Author: Genoese Merchant Networks Project
"""

import json
from uuid import uuid4

##################################
# AAT CONSTANTS (add to main script)
##################################

# Add these to the existing AAT constants section in gmn_to_cidoc_transform.py
AAT_WEIGHT = "http://vocab.getty.edu/page/aat/300056240"
AAT_VOLUME = "http://vocab.getty.edu/page/aat/300055624"
AAT_LENGTH = "http://vocab.getty.edu/page/aat/300055645"
AAT_MONETARY_VALUE = "http://vocab.getty.edu/page/aat/300055997"
AAT_COLOR = "http://vocab.getty.edu/page/aat/300056130"
AAT_NAME = "http://vocab.getty.edu/page/aat/300404650"

# Object type examples (extend as needed)
AAT_SALT = "http://vocab.getty.edu/page/aat/300010967"
AAT_WOOL = "http://vocab.getty.edu/page/aat/300243430"
AAT_CLOTH = "http://vocab.getty.edu/page/aat/300014063"
AAT_WINE = "http://vocab.getty.edu/page/aat/300379690"


##################################
# HELPER FUNCTIONS
##################################

def get_or_create_activity(data, activity_type=None):
    """
    Get existing activity from P67_refers_to or create a new one.
    
    Args:
        data: The contract data dictionary
        activity_type: Type of activity ('E8_Acquisition' or 'E10_Transfer_of_Custody')
                      If None, determined from contract type
    
    Returns:
        tuple: (activity_uri, activity_dict)
    """
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Determine activity type if not specified
    if activity_type is None:
        contract_type = data.get('@type', '')
        if isinstance(contract_type, list):
            contract_type = contract_type[0] if contract_type else ''
        
        # Lease contracts use E10_Transfer_of_Custody, others use E8_Acquisition
        if 'E31_6_Lease_Contract' in str(contract_type):
            activity_type = 'cidoc:E10_Transfer_of_Custody'
            activity_uri = f"{subject_uri}/custody_transfer"
        else:
            activity_type = 'cidoc:E8_Acquisition'
            activity_uri = f"{subject_uri}/acquisition"
    else:
        # Use provided activity type
        if 'E10' in activity_type:
            activity_uri = f"{subject_uri}/custody_transfer"
        else:
            activity_uri = f"{subject_uri}/acquisition"
    
    # Check if activity already exists
    if 'cidoc:P67_refers_to' in data:
        refers_to = data['cidoc:P67_refers_to']
        if isinstance(refers_to, list) and len(refers_to) > 0:
            activity = refers_to[0]
            return activity['@id'], activity
        elif isinstance(refers_to, dict):
            return refers_to['@id'], refers_to
    
    # Create new activity
    activity = {
        '@id': activity_uri,
        '@type': activity_type
    }
    
    # Initialize P67_refers_to
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    data['cidoc:P67_refers_to'].append(activity)
    
    return activity_uri, activity


def generate_attribution_uri(activity_uri, object_uri, index=1):
    """Generate a unique URI for an E13 Attribute Assignment."""
    object_hash = str(hash(object_uri))[-6:]
    return f"{activity_uri}/attribution_{index:03d}_{object_hash}"


def get_property_type_for_activity(activity_type):
    """
    Determine whether to use P24 (title) or P30 (custody) based on activity type.
    
    Args:
        activity_type: The CIDOC-CRM activity type
    
    Returns:
        str: Property type URI (P24 or P30)
    """
    if 'E10_Transfer_of_Custody' in str(activity_type):
        return 'cidoc:P30_transferred_custody_of'
    else:
        return 'cidoc:P24_transferred_title_of'


##################################
# CORE TRANSFORMATION FUNCTION
##################################

def transform_p70_3_indicates_transferred_object(data):
    """
    Transform gmn:P70_3_indicates_transferred_object to full CIDOC-CRM structure
    using E13 Attribute Assignment pattern.
    
    Pattern:
    E31_Document > P67_refers_to > E7/E8/E10_Activity 
                                   > P140i_was_assigned_by > E13_Attribute_Assignment
                                                            > P177 (P24 or P30)
                                                            > P141 (object)
                                                            > P2 (type)
    
    Args:
        data: The contract item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_3_indicates_transferred_object' not in data:
        return data
    
    objects = data['gmn:P70_3_indicates_transferred_object']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Get or create the activity (E8 or E10)
    activity_uri, activity = get_or_create_activity(data)
    activity_type = activity.get('@type', 'cidoc:E8_Acquisition')
    
    # Determine property type (P24 for ownership, P30 for custody)
    property_type = get_property_type_for_activity(activity_type)
    
    # Initialize P140i_was_assigned_by if not exists
    if 'cidoc:P140i_was_assigned_by' not in activity:
        activity['cidoc:P140i_was_assigned_by'] = []
    
    # Process each object
    attribution_index = len(activity['cidoc:P140i_was_assigned_by']) + 1
    
    for obj_ref in objects:
        # Extract object URI and type
        if isinstance(obj_ref, dict):
            object_uri = obj_ref.get('@id', '')
            object_type = obj_ref.get('gmn:P2_1_has_type', obj_ref.get('cidoc:P2_has_type', None))
        else:
            object_uri = str(obj_ref)
            object_type = None
        
        if not object_uri:
            continue
        
        # Generate E13 Attribute Assignment URI
        attribution_uri = generate_attribution_uri(activity_uri, object_uri, attribution_index)
        
        # Create E13 Attribute Assignment
        attribution = {
            '@id': attribution_uri,
            '@type': 'cidoc:E13_Attribute_Assignment',
            'cidoc:P177_assigned_property_of_type': {
                '@id': property_type
            },
            'cidoc:P141_assigned': {
                '@id': object_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        }
        
        # Add object type to E13 if available
        if object_type:
            if isinstance(object_type, dict):
                attribution['cidoc:P2_has_type'] = object_type
            elif isinstance(object_type, str):
                attribution['cidoc:P2_has_type'] = {
                    '@id': object_type,
                    '@type': 'cidoc:E55_Type'
                }
        
        # Add E13 to activity
        activity['cidoc:P140i_was_assigned_by'].append(attribution)
        attribution_index += 1
    
    # Remove shortcut property
    del data['gmn:P70_3_indicates_transferred_object']
    
    return data


##################################
# OBJECT PROPERTY TRANSFORMATIONS
##################################

def transform_object_properties(object_data):
    """
    Transform all object-specific shortcut properties to CIDOC-CRM.
    Call this on object resources after they've been loaded.
    
    Args:
        object_data: The object item data dictionary
    
    Returns:
        Modified object data dictionary
    """
    # Transform each property type
    object_data = transform_p2_1_has_type(object_data)
    object_data = transform_p54_1_has_count(object_data)
    object_data = transform_p43_1_has_dimension(object_data)
    object_data = transform_p56_1_has_color(object_data)
    object_data = transform_p27_1_has_origin(object_data)
    object_data = transform_monetary_value_properties(object_data)
    
    return object_data


def transform_p2_1_has_type(data):
    """
    Transform gmn:P2_1_has_type to cidoc:P2_has_type.
    
    Args:
        data: The object data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P2_1_has_type' not in data:
        return data
    
    types = data['gmn:P2_1_has_type']
    
    if 'cidoc:P2_has_type' not in data:
        data['cidoc:P2_has_type'] = []
    
    for type_obj in types if isinstance(types, list) else [types]:
        if isinstance(type_obj, dict):
            data['cidoc:P2_has_type'].append(type_obj)
        else:
            data['cidoc:P2_has_type'].append({
                '@id': str(type_obj),
                '@type': 'cidoc:E55_Type'
            })
    
    del data['gmn:P2_1_has_type']
    return data


def transform_p54_1_has_count(data):
    """
    Transform gmn:P54_1_has_count to cidoc:P57_has_number_of_parts.
    
    Args:
        data: The object data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P54_1_has_count' not in data:
        return data
    
    count = data['gmn:P54_1_has_count']
    
    if isinstance(count, dict):
        count_value = count.get('@value', count)
    else:
        count_value = count
    
    data['cidoc:P57_has_number_of_parts'] = count_value
    
    del data['gmn:P54_1_has_count']
    return data


def transform_p43_1_has_dimension(data):
    """
    Transform gmn:P43_1_has_dimension to cidoc:P43_has_dimension.
    
    Args:
        data: The object data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P43_1_has_dimension' not in data:
        return data
    
    dimensions = data['gmn:P43_1_has_dimension']
    
    if 'cidoc:P43_has_dimension' not in data:
        data['cidoc:P43_has_dimension'] = []
    
    for dim_obj in dimensions if isinstance(dimensions, list) else [dimensions]:
        if isinstance(dim_obj, dict):
            # Dimension is embedded or referenced
            data['cidoc:P43_has_dimension'].append(dim_obj)
        else:
            # Dimension is a URI reference
            data['cidoc:P43_has_dimension'].append({
                '@id': str(dim_obj),
                '@type': 'cidoc:E54_Dimension'
            })
    
    del data['gmn:P43_1_has_dimension']
    return data


def transform_p56_1_has_color(data):
    """
    Transform gmn:P56_1_has_color to cidoc:P56_bears_feature (color).
    
    Pattern:
    E18 > P56_bears_feature > E26_Physical_Feature > P2 (color) + P3 (value)
    
    Args:
        data: The object data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P56_1_has_color' not in data:
        return data
    
    colors = data['gmn:P56_1_has_color']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P56_bears_feature' not in data:
        data['cidoc:P56_bears_feature'] = []
    
    color_index = 1
    for color_obj in colors if isinstance(colors, list) else [colors]:
        if isinstance(color_obj, dict):
            color_value = color_obj.get('@value', str(color_obj))
        else:
            color_value = str(color_obj)
        
        feature_uri = f"{subject_uri}/feature/color_{color_index}"
        
        feature = {
            '@id': feature_uri,
            '@type': 'cidoc:E26_Physical_Feature',
            'cidoc:P2_has_type': {
                '@id': AAT_COLOR,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P3_has_note': color_value
        }
        
        data['cidoc:P56_bears_feature'].append(feature)
        color_index += 1
    
    del data['gmn:P56_1_has_color']
    return data


def transform_p27_1_has_origin(data):
    """
    Transform gmn:P27_1_has_origin to cidoc:P27_moved_from.
    
    Args:
        data: The object data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P27_1_has_origin' not in data:
        return data
    
    origins = data['gmn:P27_1_has_origin']
    
    if 'cidoc:P27_moved_from' not in data:
        data['cidoc:P27_moved_from'] = []
    
    for origin_obj in origins if isinstance(origins, list) else [origins]:
        if isinstance(origin_obj, dict):
            data['cidoc:P27_moved_from'].append(origin_obj)
        else:
            data['cidoc:P27_moved_from'].append({
                '@id': str(origin_obj),
                '@type': 'cidoc:E53_Place'
            })
    
    del data['gmn:P27_1_has_origin']
    return data


def transform_monetary_value_properties(data):
    """
    Transform monetary value properties (L.S.D format) to CIDOC-CRM E54_Dimension.
    
    Pattern:
    E18 > P43_has_dimension > E54_Dimension > P2 (monetary value) + P90 (value) + P91 (currency)
    
    Args:
        data: The object data dictionary
    
    Returns:
        Modified data dictionary
    """
    # Check if any monetary value properties exist
    has_lire = 'gmn:has_monetary_value_lire' in data
    has_soldi = 'gmn:has_monetary_value_soldi' in data
    has_denari = 'gmn:has_monetary_value_denari' in data
    has_currency = 'gmn:has_monetary_value_currency' in data
    
    if not (has_lire or has_soldi or has_denari):
        return data
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Get values
    lire = data.get('gmn:has_monetary_value_lire', 0)
    soldi = data.get('gmn:has_monetary_value_soldi', 0)
    denari = data.get('gmn:has_monetary_value_denari', 0)
    currency = data.get('gmn:has_monetary_value_currency', None)
    provenance = data.get('gmn:has_monetary_value_provenance', None)
    
    # Convert to decimal if needed
    if isinstance(lire, dict):
        lire = float(lire.get('@value', 0))
    else:
        lire = float(lire)
    
    # Create E54_Dimension for monetary value
    dimension_uri = f"{subject_uri}/dimension/monetary_value"
    
    dimension = {
        '@id': dimension_uri,
        '@type': 'cidoc:E54_Dimension',
        'cidoc:P2_has_type': {
            '@id': AAT_MONETARY_VALUE,
            '@type': 'cidoc:E55_Type'
        },
        'cidoc:P90_has_value': lire
    }
    
    # Add currency if specified
    if currency:
        if isinstance(currency, dict):
            dimension['cidoc:P91_has_unit'] = currency
        else:
            dimension['cidoc:P91_has_unit'] = {
                '@id': str(currency),
                '@type': 'cidoc:E98_Currency'
            }
    
    # Add provenance as note if specified
    if provenance:
        if isinstance(provenance, dict):
            provenance = provenance.get('@value', '')
        dimension['cidoc:P3_has_note'] = str(provenance)
    
    # Initialize P43_has_dimension if not exists
    if 'cidoc:P43_has_dimension' not in data:
        data['cidoc:P43_has_dimension'] = []
    
    data['cidoc:P43_has_dimension'].append(dimension)
    
    # Remove shortcut properties
    if has_lire:
        del data['gmn:has_monetary_value_lire']
    if has_soldi:
        del data['gmn:has_monetary_value_soldi']
    if has_denari:
        del data['gmn:has_monetary_value_denari']
    if has_currency:
        del data['gmn:has_monetary_value_currency']
    if 'gmn:has_monetary_value_provenance' in data:
        del data['gmn:has_monetary_value_provenance']
    
    return data


##################################
# INTEGRATION WITH MAIN SCRIPT
##################################

def integrate_with_transform_item(item, include_internal=False):
    """
    Example of how to integrate these transformations into the main transform_item() function.
    
    Add this call to transform_item() in gmn_to_cidoc_transform.py:
    
    ```python
    def transform_item(item, include_internal=False):
        # ... existing transformations ...
        
        # P70.3 Transferred Object (E13 pattern)
        item = transform_p70_3_indicates_transferred_object(item)
        
        # If this item is an object (not a contract), transform its properties
        if is_object_resource(item):
            item = transform_object_properties(item)
        
        # ... rest of transformations ...
        return item
    ```
    
    Args:
        item: The item data dictionary
        include_internal: Whether to include internal-only properties
    
    Returns:
        Transformed item
    """
    # Transform P70.3 property on contracts
    item = transform_p70_3_indicates_transferred_object(item)
    
    # If this is an object resource, transform its properties
    item_types = item.get('@type', [])
    if not isinstance(item_types, list):
        item_types = [item_types]
    
    is_object = any(
        'E18_Physical_Thing' in str(t) or
        'E24_Physical_Human-Made_Thing' in str(t) or
        'E22_' in str(t) or
        'Physical' in str(t)
        for t in item_types
    )
    
    if is_object:
        item = transform_object_properties(item)
    
    return item


##################################
# UTILITY FUNCTIONS FOR TESTING
##################################

def test_transformation():
    """
    Test the transformation with sample data.
    """
    # Sample contract with object
    contract = {
        '@id': 'http://example.org/contract001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_1_indicates_seller': {'@id': 'http://example.org/seller001'},
        'gmn:P70_2_indicates_buyer': {'@id': 'http://example.org/buyer001'},
        'gmn:P70_3_indicates_transferred_object': [
            {
                '@id': 'http://example.org/object_salt_001',
                'gmn:P2_1_has_type': 'http://vocab.getty.edu/page/aat/300010967'
            }
        ]
    }
    
    # Sample object
    object_resource = {
        '@id': 'http://example.org/object_salt_001',
        '@type': 'cidoc:E24_Physical_Human-Made_Thing',
        'gmn:P1_1_has_name': 'White salt from Ibiza',
        'gmn:P2_1_has_type': 'http://vocab.getty.edu/page/aat/300010967',
        'gmn:P54_1_has_count': 100,
        'gmn:P56_1_has_color': 'white',
        'gmn:P27_1_has_origin': {'@id': 'http://example.org/place_ibiza'},
        'gmn:has_monetary_value_lire': 450.00,
        'gmn:has_monetary_value_currency': {'@id': 'http://example.org/lira_genovese'}
    }
    
    # Transform
    transformed_contract = transform_p70_3_indicates_transferred_object(contract)
    transformed_object = transform_object_properties(object_resource)
    
    # Print results
    print("Transformed Contract:")
    print(json.dumps(transformed_contract, indent=2))
    print("\nTransformed Object:")
    print(json.dumps(transformed_object, indent=2))


##################################
# DOCUMENTATION
##################################

"""
INTEGRATION CHECKLIST:

1. Add AAT constants to main script
2. Copy all transformation functions to main script
3. Add function calls to transform_item():
   - transform_p70_3_indicates_transferred_object(item)
   - transform_object_properties(item) for objects
4. Test with sample data
5. Validate output against CIDOC-CRM

TRANSFORMATION ORDER:
1. Contract properties (P70.1, P70.2, etc.)
2. P70.3 (creates E13 pattern)
3. Object properties (P2.1, P54.1, etc.)
4. Related entities (dimensions, places, etc.)

DEPENDENCIES:
- Requires existing transformation functions for:
  - P1_1_has_name (for object names)
  - P94i properties (for dates)
  - Other contract properties

TESTING:
- Run test_transformation() to verify basic functionality
- Test with real Omeka-S JSON-LD exports
- Validate output RDF with CIDOC-CRM validator
- Check that E13 nodes are created correctly

VERSION: 1.0
DATE: 2025-10-28
"""


if __name__ == '__main__':
    # Run test if script is executed directly
    print("Testing P70.3 transformation...")
    test_transformation()
