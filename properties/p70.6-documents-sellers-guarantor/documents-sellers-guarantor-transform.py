# Python Additions for P70.6 Documents Seller's Guarantor
# Ready-to-copy code for gmn_to_cidoc_transform.py

# =============================================================================
# SECTION 1: IMPORTS (Add if not already present)
# =============================================================================
# Add these imports at the top of the file if not already present:

from uuid import uuid4
import json

# =============================================================================
# SECTION 2: AAT CONSTANTS (Add if not already present)
# =============================================================================
# Add this constant near the top of the file with other AAT constants:

AAT_GUARANTOR = 'http://vocab.getty.edu/aat/300379835'

# Complete set of AAT constants for context:
# AAT_NOTARY = 'http://vocab.getty.edu/aat/300025631'
# AAT_PROCURATOR = 'http://vocab.getty.edu/aat/300266886'
# AAT_GUARANTOR = 'http://vocab.getty.edu/aat/300379835'
# AAT_BROKER = 'http://vocab.getty.edu/aat/300025234'

# =============================================================================
# SECTION 3: HELPER FUNCTION (Add if not already present)
# =============================================================================
# This helper function is shared between P70.6 (seller's guarantor) 
# and P70.7 (buyer's guarantor). Add once and use for both properties.

def transform_guarantor_property(data, property_name, motivated_by_property):
    """
    Generic function to transform guarantor properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    
    This function handles both seller's guarantors (P70.6) and buyer's 
    guarantors (P70.7) by accepting different motivated_by properties.
    
    Args:
        data (dict): The item data dictionary to transform
        property_name (str): The GMN property to transform
                           (e.g., 'gmn:P70_6_documents_sellers_guarantor')
        motivated_by_property (str): The CIDOC property linking to the principal
                                    ('cidoc:P23_transferred_title_from' for seller,
                                     'cidoc:P22_transferred_title_to' for buyer)
    
    Returns:
        dict: Transformed data dictionary with guarantor activities in CIDOC-CRM format
    
    Example:
        >>> data = {
        ...     '@id': 'http://example.org/contract/001',
        ...     'gmn:P70_6_documents_sellers_guarantor': [
        ...         {'@id': 'http://example.org/person/guarantor001'}
        ...     ]
        ... }
        >>> result = transform_guarantor_property(
        ...     data, 
        ...     'gmn:P70_6_documents_sellers_guarantor',
        ...     'cidoc:P23_transferred_title_from'
        ... )
    """
    # Check if the property exists in the data
    if property_name not in data:
        return data
    
    guarantors = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure the acquisition node exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure P9_consists_of array exists
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Extract the motivated-by URI (seller or buyer) if available
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    # Process each guarantor
    for guarantor_obj in guarantors:
        # Extract guarantor URI and data
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate a unique but deterministic activity URI
        activity_hash = str(hash(guarantor_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
        
        # Build the E7_Activity node
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if the principal (seller/buyer) is known
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add the activity to the acquisition's P9_consists_of
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the original GMN property
    del data[property_name]
    return data

# =============================================================================
# SECTION 4: SPECIFIC TRANSFORMATION FUNCTION FOR P70.6
# =============================================================================
# Add this function with other P70.x transformation functions:

def transform_p70_6_documents_sellers_guarantor(data):
    """
    Transform gmn:P70_6_documents_sellers_guarantor to full CIDOC-CRM structure.
    
    Converts the simplified GMN property into a complete CIDOC-CRM representation:
    - Creates an E7_Activity for the guarantor's participation
    - Links the guarantor via P14_carried_out_by
    - Qualifies the role via P14.1_in_the_role_of (AAT: guarantor)
    - Links to the seller via P17_was_motivated_by
    
    The transformation pattern:
        E31_Document > P70_documents > E8_Acquisition > P9_consists_of > 
        E7_Activity > P14_carried_out_by > E21_Person (guarantor)
        E7_Activity > P17_was_motivated_by > E21_Person (seller)
    
    Args:
        data (dict): Item data dictionary containing gmn:P70_6_documents_sellers_guarantor
    
    Returns:
        dict: Transformed item dictionary with CIDOC-CRM structure
    
    Example:
        >>> contract = {
        ...     '@id': 'http://example.org/contract/1455_03_15',
        ...     '@type': 'gmn:E31_2_Sales_Contract',
        ...     'gmn:P70_1_documents_seller': {
        ...         '@id': 'http://example.org/person/giovanni',
        ...         '@type': 'cidoc:E21_Person'
        ...     },
        ...     'gmn:P70_6_documents_sellers_guarantor': [{
        ...         '@id': 'http://example.org/person/marco',
        ...         '@type': 'cidoc:E21_Person'
        ...     }]
        ... }
        >>> result = transform_p70_6_documents_sellers_guarantor(contract)
        >>> 'gmn:P70_6_documents_sellers_guarantor' in result
        False
        >>> 'cidoc:P70_documents' in result
        True
    """
    return transform_guarantor_property(
        data, 
        'gmn:P70_6_documents_sellers_guarantor', 
        'cidoc:P23_transferred_title_from'
    )

# =============================================================================
# SECTION 5: UPDATE THE MAIN TRANSFORM_ITEM FUNCTION
# =============================================================================
# Find the transform_item() function and add the function call in the 
# appropriate sequence. It should go after P70.5 and before P70.7:

def transform_item(item, include_internal=False):
    """
    Transform a single item from GMN format to CIDOC-CRM format.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # Name and title properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p102_1_has_title(item)
    
    # Creation properties (notary, date, place)
    item = transform_p94i_1_was_created_by(item)
    item = transform_p94i_2_has_enactment_date(item)
    item = transform_p94i_3_has_place_of_enactment(item)
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)  # ← ADD THIS LINE
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    # ... continue with remaining transformations
    
    return item

# =============================================================================
# SECTION 6: UNIT TESTS (OPTIONAL BUT RECOMMENDED)
# =============================================================================
# Add these unit tests to your test suite:

def test_transform_p70_6_single_guarantor():
    """Test transformation of a single seller's guarantor."""
    data = {
        '@id': 'http://example.org/contract/001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'cidoc:P70_documents': [{
            '@id': 'http://example.org/contract/001/acquisition',
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P23_transferred_title_from': [{
                '@id': 'http://example.org/person/seller',
                '@type': 'cidoc:E21_Person'
            }]
        }],
        'gmn:P70_6_documents_sellers_guarantor': [{
            '@id': 'http://example.org/person/guarantor',
            '@type': 'cidoc:E21_Person'
        }]
    }
    
    result = transform_p70_6_documents_sellers_guarantor(data)
    
    # Verify GMN property is removed
    assert 'gmn:P70_6_documents_sellers_guarantor' not in result
    
    # Verify acquisition structure
    assert 'cidoc:P70_documents' in result
    acquisition = result['cidoc:P70_documents'][0]
    
    # Verify P9_consists_of exists
    assert 'cidoc:P9_consists_of' in acquisition
    activities = acquisition['cidoc:P9_consists_of']
    
    # Find the guarantor activity
    guarantor_activity = None
    for activity in activities:
        if 'guarantor' in activity.get('@id', ''):
            guarantor_activity = activity
            break
    
    assert guarantor_activity is not None
    assert guarantor_activity['@type'] == 'cidoc:E7_Activity'
    
    # Verify P14_carried_out_by
    assert 'cidoc:P14_carried_out_by' in guarantor_activity
    assert guarantor_activity['cidoc:P14_carried_out_by'][0]['@id'] == 'http://example.org/person/guarantor'
    
    # Verify role
    assert 'cidoc:P14.1_in_the_role_of' in guarantor_activity
    assert guarantor_activity['cidoc:P14.1_in_the_role_of']['@id'] == AAT_GUARANTOR
    
    # Verify motivation
    assert 'cidoc:P17_was_motivated_by' in guarantor_activity
    assert guarantor_activity['cidoc:P17_was_motivated_by']['@id'] == 'http://example.org/person/seller'


def test_transform_p70_6_multiple_guarantors():
    """Test transformation of multiple seller's guarantors."""
    data = {
        '@id': 'http://example.org/contract/002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'cidoc:P70_documents': [{
            '@id': 'http://example.org/contract/002/acquisition',
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P23_transferred_title_from': [{
                '@id': 'http://example.org/person/seller',
                '@type': 'cidoc:E21_Person'
            }]
        }],
        'gmn:P70_6_documents_sellers_guarantor': [
            {'@id': 'http://example.org/person/guarantor1'},
            {'@id': 'http://example.org/person/guarantor2'}
        ]
    }
    
    result = transform_p70_6_documents_sellers_guarantor(data)
    
    # Verify GMN property is removed
    assert 'gmn:P70_6_documents_sellers_guarantor' not in result
    
    # Verify two activities were created
    acquisition = result['cidoc:P70_documents'][0]
    activities = acquisition['cidoc:P9_consists_of']
    guarantor_activities = [a for a in activities if 'guarantor' in a.get('@id', '')]
    
    assert len(guarantor_activities) == 2
    
    # Verify both guarantors are represented
    guarantor_uris = set()
    for activity in guarantor_activities:
        guarantor_uri = activity['cidoc:P14_carried_out_by'][0]['@id']
        guarantor_uris.add(guarantor_uri)
    
    assert 'http://example.org/person/guarantor1' in guarantor_uris
    assert 'http://example.org/person/guarantor2' in guarantor_uris


def test_transform_p70_6_no_seller():
    """Test transformation when seller is not defined."""
    data = {
        '@id': 'http://example.org/contract/003',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_6_documents_sellers_guarantor': [{
            '@id': 'http://example.org/person/guarantor',
            '@type': 'cidoc:E21_Person'
        }]
    }
    
    result = transform_p70_6_documents_sellers_guarantor(data)
    
    # Should still create activity but without P17
    acquisition = result['cidoc:P70_documents'][0]
    activities = acquisition['cidoc:P9_consists_of']
    guarantor_activity = activities[0]
    
    assert 'cidoc:P14_carried_out_by' in guarantor_activity
    assert 'cidoc:P14.1_in_the_role_of' in guarantor_activity
    # P17 should be absent
    assert 'cidoc:P17_was_motivated_by' not in guarantor_activity


def test_transform_p70_6_no_guarantors():
    """Test transformation when property doesn't exist."""
    data = {
        '@id': 'http://example.org/contract/004',
        '@type': 'gmn:E31_2_Sales_Contract'
    }
    
    result = transform_p70_6_documents_sellers_guarantor(data)
    
    # Should return data unchanged
    assert result == data

# =============================================================================
# SECTION 7: VALIDATION FUNCTION (OPTIONAL)
# =============================================================================
# Helper function to validate transformation output:

def validate_guarantor_transformation(data, property_name='gmn:P70_6_documents_sellers_guarantor'):
    """
    Validate that a guarantor property was correctly transformed.
    
    Args:
        data (dict): Transformed data to validate
        property_name (str): Original GMN property name
    
    Returns:
        tuple: (is_valid, error_messages)
    
    Example:
        >>> result = transform_p70_6_documents_sellers_guarantor(data)
        >>> is_valid, errors = validate_guarantor_transformation(result)
        >>> assert is_valid, f"Validation failed: {errors}"
    """
    errors = []
    
    # Check that GMN property was removed
    if property_name in data:
        errors.append(f"Original property {property_name} still present in output")
    
    # Check for acquisition node
    if 'cidoc:P70_documents' not in data:
        errors.append("Missing cidoc:P70_documents (acquisition node)")
        return False, errors
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Check for P9_consists_of
    if 'cidoc:P9_consists_of' not in acquisition:
        errors.append("Missing cidoc:P9_consists_of in acquisition")
        return False, errors
    
    activities = acquisition['cidoc:P9_consists_of']
    
    # Find guarantor activities
    guarantor_activities = [
        a for a in activities 
        if a.get('cidoc:P14.1_in_the_role_of', {}).get('@id') == AAT_GUARANTOR
    ]
    
    if not guarantor_activities:
        errors.append("No guarantor activities found in P9_consists_of")
        return False, errors
    
    # Validate each guarantor activity
    for i, activity in enumerate(guarantor_activities):
        if '@type' not in activity or activity['@type'] != 'cidoc:E7_Activity':
            errors.append(f"Guarantor activity {i} has wrong or missing @type")
        
        if 'cidoc:P14_carried_out_by' not in activity:
            errors.append(f"Guarantor activity {i} missing P14_carried_out_by")
        
        if 'cidoc:P14.1_in_the_role_of' not in activity:
            errors.append(f"Guarantor activity {i} missing P14.1_in_the_role_of")
    
    is_valid = len(errors) == 0
    return is_valid, errors

# =============================================================================
# SECTION 8: INTEGRATION NOTES
# =============================================================================
"""
Integration checklist:

1. Add AAT_GUARANTOR constant at module level
2. Add transform_guarantor_property() helper function (if not present)
3. Add transform_p70_6_documents_sellers_guarantor() function
4. Update transform_item() to call the new function
5. Add unit tests to your test suite
6. Run tests to verify: pytest test_gmn_transform.py::test_transform_p70_6
7. Test with sample data
8. Validate output structure
9. Check performance with large datasets
10. Update documentation

Dependencies:
- Requires uuid module for UUID generation
- Requires AAT_GUARANTOR constant
- Works with existing acquisition structure
- Compatible with other P70.x transformations

Performance notes:
- O(n) where n is number of guarantors
- Creates one E7_Activity per guarantor
- Deterministic URI generation (hash-based)
- No database queries needed
"""

# =============================================================================
# END OF PYTHON ADDITIONS
# =============================================================================
