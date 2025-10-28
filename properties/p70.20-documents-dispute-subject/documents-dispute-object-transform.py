# GMN Transformation Script Additions
# Property: P70.20 Documents Dispute Subject
# 
# INSTRUCTIONS:
# 1. Copy the transformation function below
# 2. Paste it into your gmn_to_cidoc_transform.py file
# 3. Add after the transform_p70_19_documents_arbitrator function
# 4. Add function call to your transformation pipeline
# 
# VERSION: 1.0
# LAST UPDATED: 2025-10-28
# ============================================================================

from uuid import uuid4

# AAT Vocabulary URI (add to constants section if not already present)
AAT_ARBITRATION = 'http://vocab.getty.edu/page/aat/300417271'


def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure.
    
    This function transforms the simplified property for associating an 
    arbitration agreement with the subject matter of the dispute being arbitrated.
    
    CIDOC-CRM Path:
        E31_Document 
          → P70_documents 
            → E7_Activity 
              → P16_used_specific_object 
                → E1_CRM_Entity
    
    The transformation:
    1. Locates or creates a shared E7_Activity node (arbitration activity)
    2. Adds the dispute subject(s) to the activity's P16_used_specific_object property
    3. Ensures the activity is typed as arbitration (AAT 300417271)
    4. Removes the shortcut property from the document
    
    The E7_Activity is shared with P70.18 (disputing parties) and P70.19 
    (arbitrators), representing one unified arbitration process where:
    - P14_carried_out_by contains both disputing parties and arbitrators
    - P16_used_specific_object contains the dispute subject(s)
    
    Args:
        data (dict): The arbitration agreement document in JSON-LD format.
                    Expected to have '@type' of 'gmn:E31_3_Arbitration_Agreement'
                    and 'gmn:P70_20_documents_dispute_subject' property.
    
    Returns:
        dict: The transformed document with CIDOC-CRM compliant structure.
              The shortcut property is removed and replaced with the full
              P70_documents → E7_Activity → P16_used_specific_object path.
    
    Example Input:
        {
            "@type": "gmn:E31_3_Arbitration_Agreement",
            "@id": "http://example.org/arb/001",
            "gmn:P70_20_documents_dispute_subject": [
                {"@id": "http://example.org/property/house1"},
                {"@id": "http://example.org/debts/debt123"}
            ]
        }
    
    Example Output:
        {
            "@type": "gmn:E31_3_Arbitration_Agreement",
            "@id": "http://example.org/arb/001",
            "cidoc:P70_documents": [{
                "@id": "http://example.org/arb/001/arbitration",
                "@type": "cidoc:E7_Activity",
                "cidoc:P2_has_type": {
                    "@id": "http://vocab.getty.edu/page/aat/300417271",
                    "@type": "cidoc:E55_Type"
                },
                "cidoc:P16_used_specific_object": [
                    {"@id": "http://example.org/property/house1", "@type": "cidoc:E1_CRM_Entity"},
                    {"@id": "http://example.org/debts/debt123", "@type": "cidoc:E1_CRM_Entity"}
                ]
            }]
        }
    
    Notes:
        - The function handles both single subjects and arrays of subjects
        - If a subject already has an @type, it is preserved
        - If a subject lacks an @type, it receives cidoc:E1_CRM_Entity
        - The function safely handles subjects as either dicts or URIs
        - Activity creation is shared with P70.18 and P70.19 transformations
        - The function is idempotent - running it multiple times produces same result
    
    Version: 1.0
    Last Updated: 2025-10-28
    """
    # Check if the shortcut property exists
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    # Extract the dispute subjects and ensure it's a list
    subjects = data['gmn:P70_20_documents_dispute_subject']
    if not isinstance(subjects, list):
        subjects = [subjects]
    
    # Get or generate document URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Find existing E7_Activity or create new one
    # The activity may already exist if P70.18 or P70.19 was processed first
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new E7_Activity for arbitration
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Get reference to the activity (shared with P70.18 and P70.19)
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P16_used_specific_object if not present
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    # Add each dispute subject to the activity
    for subject_obj in subjects:
        if isinstance(subject_obj, dict):
            # Subject is already a dictionary (may have @id and @type)
            subject_data = subject_obj.copy()
            # Add default type if not present
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            # Subject is a URI string - create dict with default type
            subject_uri_str = str(subject_obj)
            subject_data = {
                '@id': subject_uri_str,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add to activity's used objects
        activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Remove the shortcut property
    del data['gmn:P70_20_documents_dispute_subject']
    
    return data


# ============================================================================
# PIPELINE INTEGRATION
# ============================================================================
#
# Add this function call to your transformation pipeline.
# Typical placement in transform_document() or similar main function:
#
# def transform_document(data):
#     """Main transformation pipeline"""
#     
#     # ... existing transformations ...
#     
#     # Arbitration Agreement transformations
#     if data.get('@type') == 'gmn:E31_3_Arbitration_Agreement':
#         data = transform_p70_18_documents_disputing_party(data)
#         data = transform_p70_19_documents_arbitrator(data)
#         data = transform_p70_20_documents_dispute_subject(data)  # ADD THIS LINE
#     
#     # ... remaining transformations ...
#     
#     return data
#
# ============================================================================


# ============================================================================
# TESTING CODE
# ============================================================================
#
# Use this code to test the transformation function:
#

def test_transform_p70_20():
    """Test cases for P70.20 transformation"""
    
    print("="*70)
    print("Testing P70.20 Documents Dispute Subject Transformation")
    print("="*70)
    
    # Test 1: Single subject
    print("\n[Test 1] Single dispute subject")
    test_data_1 = {
        '@type': 'gmn:E31_3_Arbitration_Agreement',
        '@id': 'http://example.org/arb/test001',
        'gmn:P70_20_documents_dispute_subject': [
            {'@id': 'http://example.org/property/building123'}
        ]
    }
    result_1 = transform_p70_20_documents_dispute_subject(test_data_1.copy())
    
    assert 'cidoc:P70_documents' in result_1, "P70_documents not created"
    assert 'gmn:P70_20_documents_dispute_subject' not in result_1, "Shortcut not removed"
    activity_1 = result_1['cidoc:P70_documents'][0]
    assert 'cidoc:P16_used_specific_object' in activity_1, "P16 not created"
    assert len(activity_1['cidoc:P16_used_specific_object']) == 1, "Wrong subject count"
    print("✅ Test 1 passed")
    
    # Test 2: Multiple subjects
    print("\n[Test 2] Multiple dispute subjects")
    test_data_2 = {
        '@type': 'gmn:E31_3_Arbitration_Agreement',
        '@id': 'http://example.org/arb/test002',
        'gmn:P70_20_documents_dispute_subject': [
            {'@id': 'http://example.org/debts/debt_xyz', '@type': 'cidoc:E72_Legal_Object'},
            {'@id': 'http://example.org/ships/ship_maria'},
            {'@id': 'http://example.org/contracts/partnership_001', '@type': 'gmn:E31_1_Contract'}
        ]
    }
    result_2 = transform_p70_20_documents_dispute_subject(test_data_2.copy())
    
    activity_2 = result_2['cidoc:P70_documents'][0]
    assert len(activity_2['cidoc:P16_used_specific_object']) == 3, "Wrong subject count"
    
    # Check type preservation and addition
    subjects_2 = activity_2['cidoc:P16_used_specific_object']
    assert subjects_2[0]['@type'] == 'cidoc:E72_Legal_Object', "Type not preserved"
    assert subjects_2[1]['@type'] == 'cidoc:E1_CRM_Entity', "Default type not added"
    assert subjects_2[2]['@type'] == 'gmn:E31_1_Contract', "Type not preserved"
    print("✅ Test 2 passed")
    
    # Test 3: Integration with P70.18 and P70.19 (shared activity)
    print("\n[Test 3] Shared activity with P70.18 and P70.19")
    test_data_3 = {
        '@type': 'gmn:E31_3_Arbitration_Agreement',
        '@id': 'http://example.org/arb/test003',
        'gmn:P70_18_documents_disputing_party': [
            {'@id': 'http://example.org/persons/party1'}
        ],
        'gmn:P70_19_documents_arbitrator': [
            {'@id': 'http://example.org/persons/arbitrator1'}
        ],
        'gmn:P70_20_documents_dispute_subject': [
            {'@id': 'http://example.org/property/land'}
        ]
    }
    
    # Simulate processing all three properties
    # (In practice, use your actual transformation functions)
    result_3 = test_data_3.copy()
    # Note: You would call transform_p70_18 and transform_p70_19 first
    result_3 = transform_p70_20_documents_dispute_subject(result_3)
    
    activity_3 = result_3['cidoc:P70_documents'][0]
    assert 'cidoc:P16_used_specific_object' in activity_3, "P16 not in shared activity"
    print("✅ Test 3 passed")
    
    # Test 4: Subject as URI string (not dict)
    print("\n[Test 4] Subject as URI string")
    test_data_4 = {
        '@type': 'gmn:E31_3_Arbitration_Agreement',
        '@id': 'http://example.org/arb/test004',
        'gmn:P70_20_documents_dispute_subject': [
            'http://example.org/property/warehouse'  # URI string, not dict
        ]
    }
    result_4 = transform_p70_20_documents_dispute_subject(test_data_4.copy())
    
    activity_4 = result_4['cidoc:P70_documents'][0]
    subject_4 = activity_4['cidoc:P16_used_specific_object'][0]
    assert '@id' in subject_4, "ID not created from URI string"
    assert subject_4['@type'] == 'cidoc:E1_CRM_Entity', "Type not added"
    print("✅ Test 4 passed")
    
    # Test 5: No property present
    print("\n[Test 5] No property present (no-op)")
    test_data_5 = {
        '@type': 'gmn:E31_3_Arbitration_Agreement',
        '@id': 'http://example.org/arb/test005'
    }
    result_5 = transform_p70_20_documents_dispute_subject(test_data_5.copy())
    assert result_5 == test_data_5, "Data modified when property absent"
    print("✅ Test 5 passed")
    
    print("\n" + "="*70)
    print("All tests passed! ✅")
    print("="*70)


# Uncomment to run tests:
# if __name__ == '__main__':
#     test_transform_p70_20()


# ============================================================================
# VALIDATION HELPER
# ============================================================================

def validate_p70_20_transformation(data):
    """
    Validate that P70.20 transformation was successful.
    
    Args:
        data (dict): Transformed document
        
    Returns:
        list: List of validation errors (empty if valid)
    """
    errors = []
    
    # Check shortcut property removed
    if 'gmn:P70_20_documents_dispute_subject' in data:
        errors.append("Shortcut property 'gmn:P70_20_documents_dispute_subject' not removed")
    
    # Check P70_documents exists
    if 'cidoc:P70_documents' not in data:
        errors.append("'cidoc:P70_documents' not created")
        return errors  # Can't continue validation
    
    if not isinstance(data['cidoc:P70_documents'], list) or len(data['cidoc:P70_documents']) == 0:
        errors.append("'cidoc:P70_documents' is not a non-empty list")
        return errors
    
    activity = data['cidoc:P70_documents'][0]
    
    # Check activity type
    if '@type' not in activity:
        errors.append("Activity missing '@type'")
    elif activity['@type'] != 'cidoc:E7_Activity':
        errors.append(f"Activity type is '{activity['@type']}', expected 'cidoc:E7_Activity'")
    
    # Check arbitration typing
    if 'cidoc:P2_has_type' not in activity:
        errors.append("Activity not typed as arbitration (missing P2_has_type)")
    else:
        type_obj = activity['cidoc:P2_has_type']
        if isinstance(type_obj, dict) and type_obj.get('@id') != AAT_ARBITRATION:
            errors.append(f"Activity type is {type_obj.get('@id')}, expected AAT 300417271")
    
    # Check P16_used_specific_object exists
    if 'cidoc:P16_used_specific_object' not in activity:
        errors.append("'cidoc:P16_used_specific_object' not created in activity")
        return errors
    
    # Check subjects structure
    subjects = activity['cidoc:P16_used_specific_object']
    if not isinstance(subjects, list):
        errors.append("'P16_used_specific_object' is not a list")
        return errors
    
    if len(subjects) == 0:
        errors.append("'P16_used_specific_object' is empty")
    
    # Check each subject
    for i, subject in enumerate(subjects):
        if not isinstance(subject, dict):
            errors.append(f"Subject {i} is not a dictionary")
            continue
        
        if '@id' not in subject:
            errors.append(f"Subject {i} missing '@id'")
        
        if '@type' not in subject:
            errors.append(f"Subject {i} missing '@type'")
    
    return errors


# Usage example:
# errors = validate_p70_20_transformation(transformed_data)
# if errors:
#     print("Validation failed:")
#     for error in errors:
#         print(f"  - {error}")
# else:
#     print("Validation passed!")


# ============================================================================
# END OF ADDITIONS
# ============================================================================
