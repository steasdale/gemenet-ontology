# has_name_from_source Property - Python Transformation Code
# Ready-to-copy code for gmn_to_cidoc_transform.py
#
# INSTRUCTIONS:
# 1. Open gmn_to_cidoc_transform.py in a text editor
# 2. Verify AAT_NAME_FROM_SOURCE constant is defined (around line 23)
# 3. Add transformation function in name properties section (around line 101)
# 4. Add function call to main transformation pipeline (around line 2409)
# 5. Test with sample data before deploying
#
# Version: 1.0
# Date: 2025-10-26

# ==============================================================================
# STEP 1: Verify or Add AAT Constant (near top of file, around line 23)
# ==============================================================================
# 
# Check if this constant exists. If not, add it with other AAT constants:

AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"

# Context: Should be added near other AAT constants like:
# AAT_NAME = "http://vocab.getty.edu/page/aat/300404650"
# AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"  # <-- Add this
# AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"


# ==============================================================================
# STEP 2: Add Transformation Function (around line 101)
# ==============================================================================
#
# Insert this function between transform_p1_1_has_name and transform_p1_3_has_patrilineal_name

def transform_p1_2_has_name_from_source(data):
    """Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure.
    
    This function converts the simplified name-from-source property into the
    full CIDOC-CRM compliant structure with E41_Appellation, automatically
    applying the AAT type 300456607 (names found in historical sources).
    
    Args:
        data (dict): The item data dictionary containing person information
        
    Returns:
        dict: Modified data dictionary with CIDOC-CRM structure
        
    Example:
        Input:
            {
                '@id': 'person/123',
                '@type': 'cidoc:E21_Person',
                'gmn:P1_2_has_name_from_source': [
                    {'@value': 'Antonius Spinula'}
                ]
            }
            
        Output:
            {
                '@id': 'person/123',
                '@type': 'cidoc:E21_Person',
                'cidoc:P1_is_identified_by': [
                    {
                        '@id': 'appellation/xyz',
                        '@type': 'cidoc:E41_Appellation',
                        'cidoc:P2_has_type': {
                            '@id': 'http://vocab.getty.edu/page/aat/300456607',
                            '@type': 'cidoc:E55_Type'
                        },
                        'cidoc:P190_has_symbolic_content': 'Antonius Spinula'
                    }
                ]
            }
    """
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)


# Context: The function should be placed like this:
#
# def transform_p1_1_has_name(data):
#     """Transform gmn:P1_1_has_name to full CIDOC-CRM structure."""
#     return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)
#
#
# def transform_p1_2_has_name_from_source(data):  # <-- ADD THIS FUNCTION
#     """Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure."""
#     return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)
#
#
# def transform_p1_3_has_patrilineal_name(data):
#     """Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure."""
#     return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)


# ==============================================================================
# STEP 3: Add Function Call to Transformation Pipeline (around line 2409)
# ==============================================================================
#
# In the main transformation function (typically transform_item or similar),
# add the function call with other name property transformations:

# Find this section in your transformation pipeline:
#
# def transform_item(item):
#     """Transform a single item from Omeka-S format to CIDOC-CRM."""
#     # ... other transformations ...
#     
#     item = transform_p1_1_has_name(item)
#     item = transform_p1_2_has_name_from_source(item)  # <-- ADD THIS LINE
#     item = transform_p1_3_has_patrilineal_name(item)
#     
#     # ... more transformations ...
#     return item


# ==============================================================================
# TESTING CODE
# ==============================================================================
#
# Use this code to test the transformation function:

def test_transform_p1_2_has_name_from_source():
    """Test function for P1_2 transformation."""
    
    # Test 1: Single name
    test_data_1 = {
        '@id': 'http://example.org/person/test_001',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_2_has_name_from_source': [
            {'@value': 'Iohannes Spinula'}
        ]
    }
    
    result_1 = transform_p1_2_has_name_from_source(test_data_1.copy())
    assert 'cidoc:P1_is_identified_by' in result_1, "P1_is_identified_by not created"
    assert 'gmn:P1_2_has_name_from_source' not in result_1, "Original property not removed"
    print("✓ Test 1 passed: Single name transformation")
    
    # Test 2: Multiple names
    test_data_2 = {
        '@id': 'http://example.org/person/test_002',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_2_has_name_from_source': [
            {'@value': 'Antonius de Auria'},
            {'@value': 'Antonio Doria'}
        ]
    }
    
    result_2 = transform_p1_2_has_name_from_source(test_data_2.copy())
    assert len(result_2['cidoc:P1_is_identified_by']) == 2, "Should have 2 appellations"
    print("✓ Test 2 passed: Multiple names transformation")
    
    # Test 3: Verify AAT type
    for app in result_2['cidoc:P1_is_identified_by']:
        assert app['@type'] == 'cidoc:E41_Appellation', "Wrong appellation type"
        assert 'cidoc:P2_has_type' in app, "Missing type link"
        assert app['cidoc:P2_has_type']['@id'] == AAT_NAME_FROM_SOURCE, "Wrong AAT type"
        assert 'cidoc:P190_has_symbolic_content' in app, "Missing symbolic content"
    print("✓ Test 3 passed: AAT type verification")
    
    # Test 4: Special characters
    test_data_3 = {
        '@id': 'http://example.org/person/test_003',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_2_has_name_from_source': [
            {'@value': 'Iohannes q. Petri de Nigro'}
        ]
    }
    
    result_3 = transform_p1_2_has_name_from_source(test_data_3.copy())
    content = result_3['cidoc:P1_is_identified_by'][0]['cidoc:P190_has_symbolic_content']
    assert 'q.' in content, "Special characters not preserved"
    print("✓ Test 4 passed: Special character handling")
    
    # Test 5: Empty name handling
    test_data_4 = {
        '@id': 'http://example.org/person/test_004',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_2_has_name_from_source': [
            {'@value': ''}
        ]
    }
    
    result_4 = transform_p1_2_has_name_from_source(test_data_4.copy())
    # Empty names should be skipped by transform_name_property
    if 'cidoc:P1_is_identified_by' in result_4:
        assert len(result_4['cidoc:P1_is_identified_by']) == 0, "Empty name should be skipped"
    print("✓ Test 5 passed: Empty name handling")
    
    # Test 6: Integration with existing appellations
    test_data_5 = {
        '@id': 'http://example.org/person/test_005',
        '@type': 'cidoc:E21_Person',
        'cidoc:P1_is_identified_by': [
            {
                '@id': 'http://example.org/appellation/existing',
                '@type': 'cidoc:E41_Appellation',
                'cidoc:P190_has_symbolic_content': 'Existing Name'
            }
        ],
        'gmn:P1_2_has_name_from_source': [
            {'@value': 'New Source Name'}
        ]
    }
    
    result_5 = transform_p1_2_has_name_from_source(test_data_5.copy())
    assert len(result_5['cidoc:P1_is_identified_by']) == 2, "Should preserve existing appellations"
    print("✓ Test 6 passed: Integration with existing appellations")
    
    print("\n✓ All tests passed!")
    return True


# Run tests if this file is executed directly
if __name__ == '__main__':
    print("Testing transform_p1_2_has_name_from_source...")
    test_transform_p1_2_has_name_from_source()


# ==============================================================================
# INTEGRATION NOTES
# ==============================================================================
#
# Dependencies:
# - transform_name_property() function must exist (it should already be in the script)
# - generate_appellation_uri() function must exist
# - AAT_NAME_FROM_SOURCE constant must be defined
# - uuid module must be imported
#
# The transform_name_property function (should already exist around line 48) handles:
# - Extracting name values from the property
# - Generating unique URIs for appellations
# - Creating E41_Appellation structures
# - Applying the correct AAT type
# - Adding appellations to P1_is_identified_by
# - Removing the original shortcut property
#
# Example of the helper function being used:
# def transform_name_property(data, property_name, aat_type_uri):
#     """Generic function to transform name shortcut properties."""
#     if property_name not in data:
#         return data
#     
#     names = data[property_name]
#     subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
#     
#     if 'cidoc:P1_is_identified_by' not in data:
#         data['cidoc:P1_is_identified_by'] = []
#     
#     for name_obj in names:
#         if isinstance(name_obj, dict):
#             name_value = name_obj.get('@value', '')
#         else:
#             name_value = str(name_obj)
#         
#         if not name_value:
#             continue
#         
#         appellation_uri = generate_appellation_uri(subject_uri, name_value, property_name)
#         
#         appellation = {
#             '@id': appellation_uri,
#             '@type': 'cidoc:E41_Appellation',
#             'cidoc:P2_has_type': {
#                 '@id': aat_type_uri,
#                 '@type': 'cidoc:E55_Type'
#             },
#             'cidoc:P190_has_symbolic_content': name_value
#         }
#         
#         data['cidoc:P1_is_identified_by'].append(appellation)
#     
#     del data[property_name]
#     return data


# ==============================================================================
# VALIDATION CHECKLIST
# ==============================================================================
#
# Before deploying, verify:
# ✓ AAT_NAME_FROM_SOURCE constant is defined with correct URI
# ✓ transform_p1_2_has_name_from_source function is added
# ✓ Function is called in main transformation pipeline
# ✓ Function is called in correct order (after P1_1, before P1_3)
# ✓ All tests pass successfully
# ✓ Python syntax validates without errors
# ✓ Integration test with full pipeline succeeds
#
# Syntax validation:
#   python -m py_compile gmn_to_cidoc_transform.py
#
# Run unit tests:
#   python gmn_to_cidoc_transform.py  # If __main__ block includes tests
#
# Or create and run a separate test file:
#   python test_has_name_from_source.py


# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================
#
# Issue: NameError: name 'AAT_NAME_FROM_SOURCE' is not defined
# Solution: Add the constant at the top of the file with other AAT constants
#
# Issue: Function not being called
# Solution: Verify function is added to transformation pipeline
#
# Issue: AttributeError: 'NoneType' object has no attribute 'copy'
# Solution: Check that transform_name_property function exists and is working
#
# Issue: Original property not removed
# Solution: Verify transform_name_property deletes the source property
#
# Issue: Wrong AAT type in output
# Solution: Check AAT_NAME_FROM_SOURCE constant value is correct


# ==============================================================================
# END OF PYTHON ADDITIONS FILE
# ==============================================================================
