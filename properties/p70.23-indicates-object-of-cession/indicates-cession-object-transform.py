# Python Additions for P70.23 Indicates Object of Cession
# Add this to gmn_to_cidoc_transform.py after the transform_p70_22_indicates_receiving_party() function

# ============================================================================
# Transformation Function: P70.23 Indicates Object of Cession
# ============================================================================

def transform_p70_23_indicates_object_of_cession(data):
    """
    Transform gmn:P70_23_indicates_object_of_cession to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E72_Legal_Object
    
    This property associates a cession of rights contract with the legal rights,
    claims, or obligations being transferred. The transformation creates or reuses
    an E7_Activity node typed as a cession/transfer of rights (AAT 300417639).
    
    Args:
        data: Dictionary containing the entity data with JSON-LD structure
        
    Returns:
        Transformed dictionary with CIDOC-CRM compliant structure
        
    Example Input (GMN Shortcut):
        {
            '@id': 'http://example.org/cession001',
            '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
            'gmn:P70_23_indicates_object_of_cession': {
                '@id': 'http://example.org/debt_claim',
                '@type': 'cidoc:E72_Legal_Object'
            }
        }
        
    Example Output (CIDOC-CRM Compliant):
        {
            '@id': 'http://example.org/cession001',
            '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
            'cidoc:P70_documents': [{
                '@id': 'http://example.org/cession001/cession',
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': 'http://vocab.getty.edu/aat/300417639',
                    '@type': 'cidoc:E55_Type'
                },
                'cidoc:P16_used_specific_object': [{
                    '@id': 'http://example.org/debt_claim',
                    '@type': 'cidoc:E72_Legal_Object'
                }]
            }]
        }
    
    Notes:
        - The function checks if a cession activity already exists (from P70.21 or P70.22)
        - If no activity exists, it creates one with the URI pattern: {contract_uri}/cession
        - The activity is always typed as AAT 300417639 (transfer of rights)
        - Multiple legal objects can be specified (as a list)
        - The function handles both URI references and full object dictionaries
        - If the legal object doesn't have a type, E72_Legal_Object is added
    """
    # Check if the property exists in the data
    if 'gmn:P70_23_indicates_object_of_cession' not in data:
        return data
    
    # Get the legal object(s) being transferred
    rights = data['gmn:P70_23_indicates_object_of_cession']
    
    # Get the contract URI for activity URI generation
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure P70_documents exists with a cession activity
    # Check if activity already exists (from P70.21 or P70.22)
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new cession activity
        activity_uri = f"{subject_uri}/cession"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_TRANSFER_OF_RIGHTS,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Get reference to the activity (first in list)
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P16_used_specific_object if not present
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    # Normalize rights to list format for consistent processing
    if not isinstance(rights, list):
        rights = [rights]
    
    # Add each legal object to the activity
    for rights_obj in rights:
        if isinstance(rights_obj, dict):
            # Full object with properties
            rights_data = rights_obj.copy()
            # Ensure type is set
            if '@type' not in rights_data:
                rights_data['@type'] = 'cidoc:E72_Legal_Object'
        else:
            # Simple URI reference
            rights_uri = str(rights_obj)
            rights_data = {
                '@id': rights_uri,
                '@type': 'cidoc:E72_Legal_Object'
            }
        
        # Add to activity's used objects
        activity['cidoc:P16_used_specific_object'].append(rights_data)
    
    # Remove the shortcut property
    del data['gmn:P70_23_indicates_object_of_cession']
    
    return data


# ============================================================================
# Register in transform_item() function
# ============================================================================

# In the transform_item() function, add this line in the cession properties section:
# 
# # Cession properties (P70.21-P70.23)
# item = transform_p70_21_indicates_conceding_party(item)
# item = transform_p70_22_indicates_receiving_party(item)
# item = transform_p70_23_indicates_object_of_cession(item)  # <-- ADD THIS LINE


# ============================================================================
# Constant Definition (add to top of file if not already present)
# ============================================================================

# AAT_TRANSFER_OF_RIGHTS = 'http://vocab.getty.edu/aat/300417639'


# ============================================================================
# Unit Tests
# ============================================================================

def test_p70_23_basic():
    """Test basic transformation of object of cession"""
    input_data = {
        '@id': 'http://example.org/cession001',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_23_indicates_object_of_cession': {
            '@id': 'http://example.org/debt_claim',
            '@type': 'cidoc:E72_Legal_Object'
        }
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    assert 'cidoc:P70_documents' in result
    assert len(result['cidoc:P70_documents']) == 1
    
    activity = result['cidoc:P70_documents'][0]
    assert activity['@type'] == 'cidoc:E7_Activity'
    assert 'cidoc:P16_used_specific_object' in activity
    assert len(activity['cidoc:P16_used_specific_object']) == 1
    
    legal_obj = activity['cidoc:P16_used_specific_object'][0]
    assert legal_obj['@id'] == 'http://example.org/debt_claim'
    assert legal_obj['@type'] == 'cidoc:E72_Legal_Object'
    
    print("✓ Basic transformation test passed")


def test_p70_23_multiple_objects():
    """Test transformation with multiple legal objects"""
    input_data = {
        '@id': 'http://example.org/cession002',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_23_indicates_object_of_cession': [
            {'@id': 'http://example.org/debt_claim_1'},
            {'@id': 'http://example.org/usufruct_right'}
        ]
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    activity = result['cidoc:P70_documents'][0]
    assert len(activity['cidoc:P16_used_specific_object']) == 2
    
    print("✓ Multiple objects test passed")


def test_p70_23_uri_reference():
    """Test transformation with simple URI reference"""
    input_data = {
        '@id': 'http://example.org/cession003',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'gmn:P70_23_indicates_object_of_cession': 'http://example.org/inheritance_right'
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    activity = result['cidoc:P70_documents'][0]
    legal_obj = activity['cidoc:P16_used_specific_object'][0]
    assert legal_obj['@id'] == 'http://example.org/inheritance_right'
    assert legal_obj['@type'] == 'cidoc:E72_Legal_Object'
    
    print("✓ URI reference test passed")


def test_p70_23_shared_activity():
    """Test that function reuses existing activity from other properties"""
    input_data = {
        '@id': 'http://example.org/cession004',
        '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
        'cidoc:P70_documents': [{
            '@id': 'http://example.org/cession004/cession',
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [
                {'@id': 'http://example.org/giovanni'}
            ]
        }],
        'gmn:P70_23_indicates_object_of_cession': {
            '@id': 'http://example.org/debt_claim'
        }
    }
    
    result = transform_p70_23_indicates_object_of_cession(input_data)
    
    # Should still have only one activity
    assert len(result['cidoc:P70_documents']) == 1
    assert result['cidoc:P70_documents'][0]['@id'] == 'http://example.org/cession004/cession'
    
    # Activity should have both P14 (from before) and P16 (added now)
    activity = result['cidoc:P70_documents'][0]
    assert 'cidoc:P14_carried_out_by' in activity
    assert 'cidoc:P16_used_specific_object' in activity
    
    print("✓ Shared activity test passed")


if __name__ == '__main__':
    # Run tests
    test_p70_23_basic()
    test_p70_23_multiple_objects()
    test_p70_23_uri_reference()
    test_p70_23_shared_activity()
    print("\n✓ All P70.23 tests passed!")
