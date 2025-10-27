# GMN Transformation Script - Python Additions for P1.3 Has Patrilineal Name
#
# INSTRUCTIONS:
# 1. Add the AAT constant (if not already present) near the top of gmn_to_cidoc_transform.py
# 2. Add the transformation function after other name property transformations (around line 106)
# 3. Add the function call in the main processing pipeline (around line 2410)
#
# Ensure proper indentation (4 spaces) matches your existing code style.

# ============================================================================
# SECTION 1: AAT CONSTANT DEFINITION
# ============================================================================
# Location: Near top of file with other AAT constants (around line 24)
# Note: Check if this constant already exists before adding

AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"

# ============================================================================
# SECTION 2: TRANSFORMATION FUNCTION
# ============================================================================
# Location: After transform_p1_2_has_name_from_source function (around line 106)
# This function transforms the P1.3 shortcut property to full CIDOC-CRM structure

def transform_p1_3_has_patrilineal_name(data):
    """Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)

# ============================================================================
# SECTION 3: INTEGRATION INTO PROCESSING PIPELINE
# ============================================================================
# Location: In the main processing function (around line 2410)
# Add this line with other name property transformations

# Transform P1.3 has patrilineal name
item = transform_p1_3_has_patrilineal_name(item)

# ============================================================================
# HELPER FUNCTION REFERENCE
# ============================================================================
# The transformation function relies on the existing transform_name_property helper
# This helper should already exist in your file (around line 48-93)
# 
# For reference, here's what the helper function does:
#
# def transform_name_property(data, property_name, aat_type_uri):
#     """
#     Generic function to transform name shortcut properties to full CIDOC-CRM structure.
#     
#     Args:
#         data: The item data dictionary
#         property_name: The shortcut property name (e.g., 'gmn:P1_3_has_patrilineal_name')
#         aat_type_uri: The AAT URI for the type of name (e.g., AAT_PATRONYMIC)
#     
#     Returns:
#         Modified data dictionary with CIDOC-CRM structure
#     
#     Transformation:
#         gmn:P1_3_has_patrilineal_name: "name"
#         →
#         cidoc:P1_is_identified_by: {
#             @id: <generated_uri>,
#             @type: "cidoc:E41_Appellation",
#             cidoc:P2_has_type: {
#                 @id: aat_type_uri,
#                 @type: "cidoc:E55_Type"
#             },
#             cidoc:P190_has_symbolic_content: "name"
#         }
#     """
#
# If this helper function does not exist, you will need to implement it.
# See the implementation guide for the complete helper function code.

# ============================================================================
# COMPLETE CONTEXT EXAMPLE
# ============================================================================
# Here's how the code should look in context:

"""
# Near top of file (around line 24)
AAT_NAME = "http://vocab.getty.edu/page/aat/300404688"
AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"
AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"  # ← ADD THIS
WIKIDATA_LOCONYM = "https://www.wikidata.org/wiki/Q17143070"

# ... other code ...

# Around line 101-108
def transform_p1_2_has_name_from_source(data):
    '''Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure.'''
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)


def transform_p1_3_has_patrilineal_name(data):  # ← ADD THIS FUNCTION
    '''Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure.'''
    return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)


def transform_p1_4_has_loconym(data):
    '''Transform gmn:P1_4_has_loconym to full CIDOC-CRM structure.'''
    # ... existing code ...

# ... much later in file (around line 2408-2412) ...

# Transform P1.1 has name
item = transform_p1_1_has_name(item)
# Transform P1.2 has name from source  
item = transform_p1_2_has_name_from_source(item)
# Transform P1.3 has patrilineal name  # ← ADD THIS LINE
item = transform_p1_3_has_patrilineal_name(item)  # ← ADD THIS LINE
# Transform P1.4 has loconym
item = transform_p1_4_has_loconym(item)
"""

# ============================================================================
# TESTING CODE
# ============================================================================
# Use this code to test the transformation function independently

def test_transform_p1_3_has_patrilineal_name():
    """Test function for P1.3 has patrilineal name transformation."""
    
    # Test case 1: Basic transformation
    test_data_1 = {
        '@id': 'https://example.org/person/test001',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_3_has_patrilineal_name': [
            {'@value': 'Giacomo Spinola q. Antonio'}
        ]
    }
    
    result_1 = transform_p1_3_has_patrilineal_name(test_data_1)
    
    print("Test 1 - Basic transformation:")
    print(f"  Input property present: {'gmn:P1_3_has_patrilineal_name' in test_data_1}")
    print(f"  Output has P1_is_identified_by: {'cidoc:P1_is_identified_by' in result_1}")
    print(f"  Number of appellations: {len(result_1.get('cidoc:P1_is_identified_by', []))}")
    
    if 'cidoc:P1_is_identified_by' in result_1:
        appellation = result_1['cidoc:P1_is_identified_by'][0]
        print(f"  Appellation type: {appellation.get('@type')}")
        print(f"  Type URI: {appellation.get('cidoc:P2_has_type', {}).get('@id')}")
        print(f"  Content: {appellation.get('cidoc:P190_has_symbolic_content')}")
    
    print()
    
    # Test case 2: Multiple patronymics
    test_data_2 = {
        '@id': 'https://example.org/person/test002',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_3_has_patrilineal_name': [
            {'@value': 'Giovanni Doria q. Luca'},
            {'@value': 'Giovanni Doria q. Luca q. Branca'}
        ]
    }
    
    result_2 = transform_p1_3_has_patrilineal_name(test_data_2)
    
    print("Test 2 - Multiple patronymics:")
    print(f"  Number of appellations: {len(result_2.get('cidoc:P1_is_identified_by', []))}")
    
    print()
    
    # Test case 3: Empty property (should not crash)
    test_data_3 = {
        '@id': 'https://example.org/person/test003',
        '@type': 'cidoc:E21_Person'
    }
    
    result_3 = transform_p1_3_has_patrilineal_name(test_data_3)
    
    print("Test 3 - No property present:")
    print(f"  Function handled gracefully: {result_3 == test_data_3}")
    
    print()
    
    # Test case 4: Empty string value
    test_data_4 = {
        '@id': 'https://example.org/person/test004',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_3_has_patrilineal_name': [
            {'@value': ''}
        ]
    }
    
    result_4 = transform_p1_3_has_patrilineal_name(test_data_4)
    
    print("Test 4 - Empty string value:")
    print(f"  Appellations created: {len(result_4.get('cidoc:P1_is_identified_by', []))}")
    print(f"  Should be 0 (empty strings should be skipped)")
    
    return True

# To run tests:
# if __name__ == "__main__":
#     test_transform_p1_3_has_patrilineal_name()

# ============================================================================
# VALIDATION CHECKLIST
# ============================================================================
# After adding the code, verify:
#
# [ ] AAT_PATRONYMIC constant is defined
# [ ] transform_p1_3_has_patrilineal_name function is implemented
# [ ] Function is called in the main processing pipeline
# [ ] transform_name_property helper function exists
# [ ] No syntax errors (run: python -m py_compile gmn_to_cidoc_transform.py)
# [ ] Test with sample data
# [ ] Verify output includes cidoc:P1_is_identified_by
# [ ] Verify appellation has correct type (AAT 300404651)
# [ ] Verify P190_has_symbolic_content contains the original string
# [ ] Original gmn:P1_3_has_patrilineal_name property is removed from output

# ============================================================================
# EXPECTED OUTPUT STRUCTURE
# ============================================================================
# After transformation, the data should look like this:
#
# INPUT:
# {
#   "@id": "person001",
#   "@type": "cidoc:E21_Person",
#   "gmn:P1_3_has_patrilineal_name": [
#     {"@value": "Giacomo Spinola q. Antonio"}
#   ]
# }
#
# OUTPUT:
# {
#   "@id": "person001",
#   "@type": "cidoc:E21_Person",
#   "cidoc:P1_is_identified_by": [
#     {
#       "@id": "<generated_uri>",
#       "@type": "cidoc:E41_Appellation",
#       "cidoc:P2_has_type": {
#         "@id": "http://vocab.getty.edu/page/aat/300404651",
#         "@type": "cidoc:E55_Type"
#       },
#       "cidoc:P190_has_symbolic_content": "Giacomo Spinola q. Antonio"
#     }
#   ]
# }

# ============================================================================
# DEPENDENCIES
# ============================================================================
# Required imports (should already be in your file):
# - from uuid import uuid4 (for URI generation)
# - json (for JSON handling)
#
# Required functions (should already exist in your file):
# - generate_appellation_uri(subject_uri, name_value, property_name)
# - transform_name_property(data, property_name, aat_type_uri)

# ============================================================================
# PERFORMANCE NOTES
# ============================================================================
# - Transformation is O(n) where n is the number of names
# - Memory overhead: One appellation object per name
# - No external API calls or network requests
# - Suitable for batch processing of large datasets

# ============================================================================
# ERROR HANDLING
# ============================================================================
# The function handles these cases gracefully:
# - Property not present in data: Returns data unchanged
# - Empty string values: Skipped (no appellation created)
# - Multiple values: Each creates a separate appellation
# - Malformed data: Attempts to extract string value safely

# ============================================================================
# COMPATIBILITY
# ============================================================================
# - Python 3.6+
# - JSON-LD 1.1
# - RDFLib 6.x (if using RDF serialization)
# - Works with both dict and JSON string inputs (after parsing)

# ============================================================================
# MAINTENANCE NOTES
# ============================================================================
# When updating this code:
# 1. Maintain backward compatibility with existing data
# 2. Update version number in comments
# 3. Add to change log
# 4. Update tests
# 5. Document any new behavior

# ============================================================================
# CHANGE LOG
# ============================================================================
# Version 1.0 - 2025-10-17
# - Initial implementation
# - Added to gmn_to_cidoc_transform.py
#
# Version 1.1 - 2025-10-26
# - Documentation additions file created
# - Test cases added
# - Validation checklist added

# ============================================================================
# SUPPORT
# ============================================================================
# For questions or issues:
# 1. Check the has-patrilineage-implementation-guide.md
# 2. Review the has-patrilineage-documentation.md
# 3. Examine the transform_name_property helper function
# 4. Contact the technical maintainer

# ============================================================================
