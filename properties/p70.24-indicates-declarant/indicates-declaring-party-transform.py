# GMN P70.24 Indicates Declaring Party - Python Transformation Code

"""
This file contains ready-to-copy Python code for transforming the
gmn:P70_24_indicates_declarant property in the GMN to CIDOC-CRM transformation script.
"""

# ============================================================================
# PART 1: AAT CONSTANT DEFINITION
# ============================================================================
# Add this near the top of gmn_to_cidoc_transform.py with other AAT constants
# (around line 20-50)

AAT_DECLARATION = 'http://vocab.getty.edu/page/aat/300027623'


# ============================================================================
# PART 2: MAIN TRANSFORMATION FUNCTION
# ============================================================================
# Add this function to gmn_to_cidoc_transform.py in the declaration properties
# section (around line 800-900)

def transform_p70_24_indicates_declarant(data):
    """
    Transform gmn:P70_24_indicates_declarant to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function converts the simplified declarant property into the full
    CIDOC-CRM compliant structure. It creates an E7_Activity node typed as
    a declaration (AAT 300027623) and links the declarant(s) via P14_carried_out_by.
    
    Args:
        data (dict): The document data dictionary containing the shortcut property
        
    Returns:
        dict: The transformed data with CIDOC-CRM compliant structure
        
    Examples:
        >>> data = {
        ...     '@id': 'http://example.org/declaration001',
        ...     '@type': 'gmn:E31_5_Declaration',
        ...     'gmn:P70_24_indicates_declarant': ['http://example.org/person_marco']
        ... }
        >>> result = transform_p70_24_indicates_declarant(data)
        >>> 'cidoc:P70_documents' in result
        True
        >>> result['cidoc:P70_documents'][0]['cidoc:P14_carried_out_by']
        [{'@id': 'http://example.org/person_marco', '@type': 'cidoc:E39_Actor'}]
    """
    # Check if the property exists in the data
    if 'gmn:P70_24_indicates_declarant' not in data:
        return data
    
    # Extract declarants (always a list)
    declarants = data['gmn:P70_24_indicates_declarant']
    
    # Get the document URI for generating the activity URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or reuse the activity node
    # This checks if P70_documents already exists (e.g., from P70.25)
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create a new activity with proper typing
        activity_uri = f"{subject_uri}/declaration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Get reference to the activity (either newly created or existing)
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P14_carried_out_by list if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Process each declarant
    for declarant_obj in declarants:
        # Handle both URI strings and full object dictionaries
        if isinstance(declarant_obj, dict):
            # Copy the full object data
            declarant_data = declarant_obj.copy()
            # Ensure it has a type
            if '@type' not in declarant_data:
                declarant_data['@type'] = 'cidoc:E39_Actor'
        else:
            # Simple URI string - create minimal object
            declarant_uri = str(declarant_obj)
            declarant_data = {
                '@id': declarant_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add the declarant to the activity
        activity['cidoc:P14_carried_out_by'].append(declarant_data)
    
    # Remove the shortcut property (no longer needed)
    del data['gmn:P70_24_indicates_declarant']
    
    return data


# ============================================================================
# PART 3: INTEGRATION INTO TRANSFORM PIPELINE
# ============================================================================
# Add this function call to the transform_item() function
# in the declaration properties section (around line 1300)
# Place it AFTER cession properties and BEFORE correspondence properties

def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    
    # ... [other transformations above] ...
    
    # Cession properties (P70.21-P70.23)
    item = transform_p70_21_indicates_conceding_party(item)
    item = transform_p70_22_indicates_receiving_party(item)
    item = transform_p70_23_indicates_object_of_cession(item)
    
    # Declaration properties (P70.24-P70.25)
    item = transform_p70_24_indicates_declarant(item)  # <-- ADD THIS LINE
    item = transform_p70_25_indicates_declaration_subject(item)
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    # ... [rest of transformations below] ...


# ============================================================================
# PART 4: UNIT TEST FUNCTIONS
# ============================================================================
# Optional: Add these test functions to verify the transformation works correctly

def test_p70_24_single_declarant():
    """Test transformation with a single declarant."""
    data = {
        '@id': 'http://example.org/declaration001',
        '@type': 'gmn:E31_5_Declaration',
        'gmn:P70_24_indicates_declarant': ['http://example.org/person_marco']
    }
    
    result = transform_p70_24_indicates_declarant(data)
    
    # Verify structure
    assert 'cidoc:P70_documents' in result
    assert len(result['cidoc:P70_documents']) == 1
    
    activity = result['cidoc:P70_documents'][0]
    assert activity['@type'] == 'cidoc:E7_Activity'
    assert activity['cidoc:P2_has_type']['@id'] == AAT_DECLARATION
    assert len(activity['cidoc:P14_carried_out_by']) == 1
    assert activity['cidoc:P14_carried_out_by'][0]['@id'] == 'http://example.org/person_marco'
    
    # Verify shortcut removed
    assert 'gmn:P70_24_indicates_declarant' not in result
    
    print("✓ Single declarant test passed")


def test_p70_24_multiple_declarants():
    """Test transformation with multiple declarants (joint declaration)."""
    data = {
        '@id': 'http://example.org/declaration002',
        '@type': 'gmn:E31_5_Declaration',
        'gmn:P70_24_indicates_declarant': [
            'http://example.org/brother_antonio',
            'http://example.org/brother_giovanni',
            'http://example.org/brother_francesco'
        ]
    }
    
    result = transform_p70_24_indicates_declarant(data)
    
    # Verify structure
    activity = result['cidoc:P70_documents'][0]
    assert len(activity['cidoc:P14_carried_out_by']) == 3
    
    # Verify all declarants present
    declarant_uris = [d['@id'] for d in activity['cidoc:P14_carried_out_by']]
    assert 'http://example.org/brother_antonio' in declarant_uris
    assert 'http://example.org/brother_giovanni' in declarant_uris
    assert 'http://example.org/brother_francesco' in declarant_uris
    
    print("✓ Multiple declarants test passed")


def test_p70_24_with_detailed_declarant():
    """Test transformation with declarant object containing additional data."""
    data = {
        '@id': 'http://example.org/declaration003',
        '@type': 'gmn:E31_5_Declaration',
        'gmn:P70_24_indicates_declarant': [
            {
                '@id': 'http://example.org/person_lucia',
                '@type': 'cidoc:E21_Person',
                'rdfs:label': 'Lucia the merchant'
            }
        ]
    }
    
    result = transform_p70_24_indicates_declarant(data)
    
    # Verify declarant data preserved
    activity = result['cidoc:P70_documents'][0]
    declarant = activity['cidoc:P14_carried_out_by'][0]
    assert declarant['@id'] == 'http://example.org/person_lucia'
    assert declarant['@type'] == 'cidoc:E21_Person'
    assert declarant['rdfs:label'] == 'Lucia the merchant'
    
    print("✓ Detailed declarant test passed")


def test_p70_24_no_declarant():
    """Test that function handles missing property gracefully."""
    data = {
        '@id': 'http://example.org/declaration004',
        '@type': 'gmn:E31_5_Declaration'
    }
    
    result = transform_p70_24_indicates_declarant(data)
    
    # Data should be unchanged
    assert result == data
    assert 'cidoc:P70_documents' not in result
    
    print("✓ No declarant test passed")


def test_p70_24_activity_reuse():
    """Test that existing activity is reused (integration with P70.25)."""
    data = {
        '@id': 'http://example.org/declaration005',
        '@type': 'gmn:E31_5_Declaration',
        'cidoc:P70_documents': [{
            '@id': 'http://example.org/declaration005/declaration',
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P16_used_specific_object': ['http://example.org/subject']
        }],
        'gmn:P70_24_indicates_declarant': ['http://example.org/person_marco']
    }
    
    result = transform_p70_24_indicates_declarant(data)
    
    # Should still have only one activity
    assert len(result['cidoc:P70_documents']) == 1
    
    # Activity should have both P16 (from before) and P14 (newly added)
    activity = result['cidoc:P70_documents'][0]
    assert 'cidoc:P16_used_specific_object' in activity
    assert 'cidoc:P14_carried_out_by' in activity
    
    print("✓ Activity reuse test passed")


def run_all_p70_24_tests():
    """Run all unit tests for P70.24 transformation."""
    print("\nRunning P70.24 transformation tests...")
    print("=" * 60)
    
    test_p70_24_single_declarant()
    test_p70_24_multiple_declarants()
    test_p70_24_with_detailed_declarant()
    test_p70_24_no_declarant()
    test_p70_24_activity_reuse()
    
    print("=" * 60)
    print("All tests passed! ✓\n")


# ============================================================================
# PART 5: EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    """
    Example usage and testing of the transformation function.
    Run this file directly to see examples of the transformation in action.
    """
    
    import json
    from uuid import uuid4
    
    print("\n" + "="*60)
    print("GMN P70.24 Transformation Examples")
    print("="*60 + "\n")
    
    # Example 1: Simple declaration
    print("Example 1: Simple Debt Declaration")
    print("-" * 60)
    
    example1_input = {
        '@id': 'http://example.org/debt_declaration_01',
        '@type': 'gmn:E31_5_Declaration',
        'gmn:P1_1_has_name': "Marco's debt acknowledgment",
        'gmn:P70_24_indicates_declarant': ['http://example.org/merchant_marco'],
        'gmn:P70_25_indicates_declaration_subject': ['http://example.org/debt_500_lire']
    }
    
    print("Input:")
    print(json.dumps(example1_input, indent=2))
    
    example1_output = transform_p70_24_indicates_declarant(example1_input.copy())
    
    print("\nOutput:")
    print(json.dumps(example1_output, indent=2))
    print()
    
    # Example 2: Joint declaration
    print("\nExample 2: Joint Property Declaration")
    print("-" * 60)
    
    example2_input = {
        '@id': 'http://example.org/joint_declaration_02',
        '@type': 'gmn:E31_5_Declaration',
        'gmn:P1_1_has_name': "Joint vineyard ownership declaration",
        'gmn:P70_24_indicates_declarant': [
            'http://example.org/brother_antonio',
            'http://example.org/brother_giovanni'
        ]
    }
    
    print("Input:")
    print(json.dumps(example2_input, indent=2))
    
    example2_output = transform_p70_24_indicates_declarant(example2_input.copy())
    
    print("\nOutput:")
    print(json.dumps(example2_output, indent=2))
    print()
    
    # Example 3: Rich declarant data
    print("\nExample 3: Declaration with Detailed Declarant")
    print("-" * 60)
    
    example3_input = {
        '@id': 'http://example.org/declaration_03',
        '@type': 'gmn:E31_5_Declaration',
        'gmn:P70_24_indicates_declarant': [
            {
                '@id': 'http://example.org/person_lucia',
                '@type': 'cidoc:E21_Person',
                'gmn:P1_1_has_name': 'Lucia Cattaneo',
                'gmn:P1_3_has_patrilineal_name': 'Cattaneo'
            }
        ]
    }
    
    print("Input:")
    print(json.dumps(example3_input, indent=2))
    
    example3_output = transform_p70_24_indicates_declarant(example3_input.copy())
    
    print("\nOutput:")
    print(json.dumps(example3_output, indent=2))
    print()
    
    # Run unit tests
    run_all_p70_24_tests()


# ============================================================================
# PART 6: HELPER FUNCTIONS (Optional)
# ============================================================================

def validate_p70_24_output(data):
    """
    Validate that the transformation output is correct.
    
    Args:
        data (dict): The transformed data to validate
        
    Returns:
        tuple: (bool, list) - (is_valid, list_of_errors)
    """
    errors = []
    
    # Check that shortcut property is removed
    if 'gmn:P70_24_indicates_declarant' in data:
        errors.append("Shortcut property not removed")
    
    # Check that activity exists
    if 'cidoc:P70_documents' not in data:
        errors.append("No cidoc:P70_documents found")
        return (False, errors)
    
    if len(data['cidoc:P70_documents']) == 0:
        errors.append("Empty cidoc:P70_documents list")
        return (False, errors)
    
    activity = data['cidoc:P70_documents'][0]
    
    # Check activity type
    if '@type' not in activity or activity['@type'] != 'cidoc:E7_Activity':
        errors.append("Activity not typed as E7_Activity")
    
    # Check activity has proper typing
    if 'cidoc:P2_has_type' not in activity:
        errors.append("Activity not typed with P2_has_type")
    elif activity['cidoc:P2_has_type']['@id'] != AAT_DECLARATION:
        errors.append(f"Activity type is not AAT 300027623 (declaration)")
    
    # Check declarants exist
    if 'cidoc:P14_carried_out_by' not in activity:
        errors.append("No P14_carried_out_by found in activity")
    elif len(activity['cidoc:P14_carried_out_by']) == 0:
        errors.append("P14_carried_out_by list is empty")
    else:
        # Check each declarant
        for i, declarant in enumerate(activity['cidoc:P14_carried_out_by']):
            if '@id' not in declarant:
                errors.append(f"Declarant {i} missing @id")
            if '@type' not in declarant:
                errors.append(f"Declarant {i} missing @type")
            elif 'E39_Actor' not in declarant['@type']:
                errors.append(f"Declarant {i} not typed as E39_Actor")
    
    return (len(errors) == 0, errors)


def get_declarants_from_transformed_data(data):
    """
    Extract declarant URIs from transformed data.
    
    Args:
        data (dict): The transformed data
        
    Returns:
        list: List of declarant URIs, or empty list if none found
    """
    if 'cidoc:P70_documents' not in data:
        return []
    
    if len(data['cidoc:P70_documents']) == 0:
        return []
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P14_carried_out_by' not in activity:
        return []
    
    return [d['@id'] for d in activity['cidoc:P14_carried_out_by'] if '@id' in d]


# ============================================================================
# NOTES FOR IMPLEMENTATION
# ============================================================================

"""
IMPLEMENTATION CHECKLIST:

1. Add AAT_DECLARATION constant (Part 1)
2. Add transform_p70_24_indicates_declarant function (Part 2)
3. Add function call to transform_item pipeline (Part 3)
4. Run unit tests to verify (Part 4)
5. Test with real data
6. Validate output with SPARQL queries

IMPORTANT NOTES:

- This function should be called BEFORE transform_p70_25_indicates_declaration_subject
  so that if both properties exist, they share the same activity node.

- The function checks for existing activities to enable reuse. This is critical
  for properties that share the same activity.

- All declarants are explicitly typed as E39_Actor if no type is provided.

- The activity URI follows the pattern: {document_uri}/declaration

- The function handles both URI strings and full object dictionaries as declarants.

- Edge cases (empty lists, missing properties) are handled gracefully.

TROUBLESHOOTING:

- If multiple activities are created: Check that activity reuse logic is working
- If shortcut not removed: Verify the del statement is not commented out
- If wrong activity type: Check AAT_DECLARATION constant value
- If declarants not linked: Verify P14_carried_out_by initialization

For more details, see the implementation guide included in the deliverables package.
"""
