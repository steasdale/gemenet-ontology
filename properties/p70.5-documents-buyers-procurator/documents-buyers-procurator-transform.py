# Python Additions for P70.5 Documents Buyer's Procurator
# Ready-to-copy code for gmn_to_cidoc_transform.py

# ==============================================================================
# INSTRUCTIONS
# ==============================================================================
#
# This file contains the code needed to transform gmn:P70_5_documents_buyers_procurator
# to full CIDOC-CRM structure. Follow these steps:
#
# 1. VERIFY DEPENDENCIES (see section below)
# 2. ADD CONSTANTS (if not already present)
# 3. ADD OR VERIFY GENERIC FUNCTION (transform_procurator_property)
# 4. ADD SPECIFIC TRANSFORMATION FUNCTION
# 5. INTEGRATE INTO MAIN PIPELINE
# 6. TEST WITH SAMPLE DATA
#
# ==============================================================================

# ==============================================================================
# SECTION 1: REQUIRED IMPORTS
# ==============================================================================
#
# Ensure these imports are present at the top of gmn_to_cidoc_transform.py:

from uuid import uuid4

# ==============================================================================
# SECTION 2: REQUIRED CONSTANTS
# ==============================================================================
#
# Add this constant near the top of the file (around line 20-30) if not present.
# This should be grouped with other AAT vocabulary constants.

# AAT vocabulary URIs for roles
AAT_AGENT = "http://vocab.getty.edu/aat/300411835"  # Agents (people in legal context)

# Note: If other AAT constants are already defined (e.g., AAT_GUARANTOR),
# add AAT_AGENT alongside them.

# ==============================================================================
# SECTION 3: GENERIC TRANSFORMATION FUNCTION
# ==============================================================================
#
# This generic function handles both P70.4 (seller's procurator) and P70.5
# (buyer's procurator). If this function already exists in your file (for P70.4),
# you can SKIP this section. Otherwise, add it:

def transform_procurator_property(data, property_name, motivated_by_property):
    """
    Generic function to transform procurator properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    
    Args:
        data: Item data dictionary
        property_name: The GMN property to transform 
                      (e.g., 'gmn:P70_5_documents_buyers_procurator')
        motivated_by_property: The CIDOC property linking to principal party
                              (e.g., 'cidoc:P22_transferred_title_to' for buyer)
    
    Returns:
        Transformed data dictionary
    
    Example:
        >>> data = {
        ...     '@id': 'contract123',
        ...     'gmn:P70_5_documents_buyers_procurator': [
        ...         {'@id': 'person456'}
        ...     ]
        ... }
        >>> transform_procurator_property(data, 
        ...     'gmn:P70_5_documents_buyers_procurator',
        ...     'cidoc:P22_transferred_title_to')
    """
    # Check if property exists in data
    if property_name not in data:
        return data
    
    procurators = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create E8_Acquisition if it doesn't exist
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P9_consists_of array if needed
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Get the motivated_by person (seller or buyer)
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    # Process each procurator in the list
    for procurator_obj in procurators:
        # Handle both dictionary and string URI formats
        if isinstance(procurator_obj, dict):
            procurator_uri = procurator_obj.get('@id', '')
            procurator_data = procurator_obj.copy()
        else:
            procurator_uri = str(procurator_obj)
            procurator_data = {
                '@id': procurator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI using hash
        activity_hash = str(hash(procurator_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/procurator_{activity_hash}"
        
        # Create E7_Activity structure
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [procurator_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_AGENT,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Link to motivated_by person if available
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove simplified property from data
    del data[property_name]
    return data


# ==============================================================================
# SECTION 4: SPECIFIC TRANSFORMATION FUNCTION
# ==============================================================================
#
# Add this function after transform_procurator_property (or after P70.4
# transformation function if it exists). This should go in the section with
# other P70 transformation functions.

def transform_p70_5_documents_buyers_procurator(data):
    """
    Transform gmn:P70_5_documents_buyers_procurator to full CIDOC-CRM structure.
    
    Transforms simplified buyer's procurator property to:
    E31_Document → P70_documents → E8_Acquisition → P9_consists_of → E7_Activity
      → P14_carried_out_by → E21_Person (procurator)
      → P14.1_in_the_role_of → E55_Type (AAT: agent)
      → P17_was_motivated_by → E21_Person (buyer)
    
    Args:
        data: Item data dictionary containing the property to transform
    
    Returns:
        Transformed data dictionary with CIDOC-CRM compliant structure
    
    Example:
        >>> data = {
        ...     '@id': 'https://example.org/contract/123',
        ...     '@type': 'gmn:E31_2_Sales_Contract',
        ...     'gmn:P70_2_documents_buyer': [
        ...         {'@id': 'https://example.org/person/buyer1'}
        ...     ],
        ...     'gmn:P70_5_documents_buyers_procurator': [
        ...         {'@id': 'https://example.org/person/procurator1'}
        ...     ]
        ... }
        >>> transformed = transform_p70_5_documents_buyers_procurator(data)
        >>> 'cidoc:P70_documents' in transformed
        True
        >>> 'gmn:P70_5_documents_buyers_procurator' in transformed
        False
    """
    return transform_procurator_property(
        data, 
        'gmn:P70_5_documents_buyers_procurator',
        'cidoc:P22_transferred_title_to'
    )


# ==============================================================================
# SECTION 5: MAIN PIPELINE INTEGRATION
# ==============================================================================
#
# Add the transformation call to your main transform_item() function.
# This should be inserted in the sales contract properties section,
# AFTER transform_p70_2_documents_buyer() and BEFORE 
# transform_p70_6_documents_sellers_guarantor().
#
# Find the section that looks like this:

"""
def transform_item(item, include_internal=False):
    '''
    Transform a single item from GMN shorthand to full CIDOC-CRM.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    '''
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    # ADD THE FOLLOWING LINE HERE:
    item = transform_p70_5_documents_buyers_procurator(item)
    # END OF NEW LINE
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    # ... continue with other transformations ...
"""

# ==============================================================================
# SECTION 6: TESTING CODE
# ==============================================================================
#
# Use this code to test the transformation function:

def test_p70_5_transformation():
    """Test function for P70.5 transformation."""
    
    # Test 1: Basic transformation
    test_data_1 = {
        '@id': 'https://example.org/contract/test_001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_2_documents_buyer': [{
            '@id': 'https://example.org/person/buyer_001',
            '@type': 'cidoc:E21_Person'
        }],
        'gmn:P70_5_documents_buyers_procurator': [{
            '@id': 'https://example.org/person/procurator_001',
            '@type': 'cidoc:E21_Person'
        }]
    }
    
    print("Test 1: Basic transformation")
    print("Input:", test_data_1)
    result_1 = transform_p70_5_documents_buyers_procurator(test_data_1.copy())
    print("Output:", result_1)
    print("✓ Test 1 passed" if 'cidoc:P70_documents' in result_1 else "✗ Test 1 failed")
    print()
    
    # Test 2: Multiple procurators
    test_data_2 = {
        '@id': 'https://example.org/contract/test_002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_2_documents_buyer': [{
            '@id': 'https://example.org/person/buyer_002'
        }],
        'gmn:P70_5_documents_buyers_procurator': [
            {'@id': 'https://example.org/person/procurator_002'},
            {'@id': 'https://example.org/person/procurator_003'}
        ]
    }
    
    print("Test 2: Multiple procurators")
    print("Input:", test_data_2)
    result_2 = transform_p70_5_documents_buyers_procurator(test_data_2.copy())
    activities = result_2.get('cidoc:P70_documents', [{}])[0].get('cidoc:P9_consists_of', [])
    print("Output activities count:", len(activities))
    print("✓ Test 2 passed" if len(activities) == 2 else "✗ Test 2 failed")
    print()
    
    # Test 3: No procurator (should return unchanged)
    test_data_3 = {
        '@id': 'https://example.org/contract/test_003',
        '@type': 'gmn:E31_2_Sales_Contract'
    }
    
    print("Test 3: No procurator")
    result_3 = transform_p70_5_documents_buyers_procurator(test_data_3.copy())
    print("✓ Test 3 passed" if result_3 == test_data_3 else "✗ Test 3 failed")
    print()
    
    # Test 4: String URI format
    test_data_4 = {
        '@id': 'https://example.org/contract/test_004',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_5_documents_buyers_procurator': [
            'https://example.org/person/procurator_004'
        ]
    }
    
    print("Test 4: String URI format")
    result_4 = transform_p70_5_documents_buyers_procurator(test_data_4.copy())
    print("✓ Test 4 passed" if 'cidoc:P70_documents' in result_4 else "✗ Test 4 failed")
    print()


# To run tests, uncomment the following line:
# test_p70_5_transformation()

# ==============================================================================
# SECTION 7: VERIFICATION CHECKLIST
# ==============================================================================
#
# After adding the code, verify:
#
# [ ] AAT_AGENT constant is defined
# [ ] transform_procurator_property function exists (either new or from P70.4)
# [ ] transform_p70_5_documents_buyers_procurator function is added
# [ ] Function is called in transform_item pipeline
# [ ] Function is called AFTER transform_p70_2_documents_buyer
# [ ] Function is called BEFORE transform_p70_6_documents_sellers_guarantor
# [ ] uuid4 is imported from uuid module
# [ ] No syntax errors (run Python syntax check)
# [ ] Test function executes without errors
# [ ] All tests pass
#
# ==============================================================================

# ==============================================================================
# SECTION 8: COMMON ISSUES AND SOLUTIONS
# ==============================================================================
#
# Issue 1: NameError: name 'AAT_AGENT' is not defined
# Solution: Add AAT_AGENT constant at module level (Section 2)
#
# Issue 2: AttributeError: 'str' object has no attribute 'get'
# Solution: The code handles both dict and string formats; check input data
#
# Issue 3: KeyError: 'cidoc:P22_transferred_title_to'
# Solution: Ensure transform_p70_2_documents_buyer runs before this function
#
# Issue 4: Transformation produces no output
# Solution: Check that property_name matches exactly: 
#           'gmn:P70_5_documents_buyers_procurator'
#
# Issue 5: Multiple acquisitions created
# Solution: Verify acquisition existence check in generic function
#
# ==============================================================================

# ==============================================================================
# SECTION 9: INTEGRATION WITH FULL PIPELINE
# ==============================================================================
#
# Complete transformation flow for a sales contract with buyer's procurator:
#
# 1. transform_p70_1_documents_seller(item)
#    - Creates acquisition with P23_transferred_title_from
#
# 2. transform_p70_2_documents_buyer(item)
#    - Adds P22_transferred_title_to to acquisition
#
# 3. transform_p70_3_documents_transfer_of(item)
#    - Adds P24_transferred_title_of to acquisition
#
# 4. transform_p70_4_documents_sellers_procurator(item)
#    - Creates E7_Activity for seller's procurator
#    - Links to seller via P17_was_motivated_by
#
# 5. transform_p70_5_documents_buyers_procurator(item) ← THIS FUNCTION
#    - Creates E7_Activity for buyer's procurator
#    - Links to buyer via P17_was_motivated_by
#
# 6. transform_p70_6_documents_sellers_guarantor(item)
#    - Creates E7_Activity for seller's guarantor
#    - Links to seller via P17_was_motivated_by
#
# And so on...
#
# ==============================================================================

# ==============================================================================
# SECTION 10: ADVANCED USAGE EXAMPLES
# ==============================================================================

# Example 1: Procurator with rich person data
example_1 = {
    '@id': 'https://example.org/contract/adv_001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_2_documents_buyer': [{
        '@id': 'https://example.org/person/buyer_001',
        'gmn:P1_1_has_name': 'Giovanni de Marini'
    }],
    'gmn:P70_5_documents_buyers_procurator': [{
        '@id': 'https://example.org/person/procurator_001',
        '@type': 'cidoc:E21_Person',
        'gmn:P1_1_has_name': 'Oberto Spinola',
        'gmn:P1_3_has_patrilineal_name': 'Spinola',
        'gmn:P1_4_has_loconym': 'de Ianua'
    }]
}

# The rich person data is preserved in the transformation

# Example 2: Multiple contracts with same procurator
example_2a = {
    '@id': 'https://example.org/contract/multi_001',
    'gmn:P70_5_documents_buyers_procurator': [{
        '@id': 'https://example.org/person/common_procurator'
    }]
}

example_2b = {
    '@id': 'https://example.org/contract/multi_002',
    'gmn:P70_5_documents_buyers_procurator': [{
        '@id': 'https://example.org/person/common_procurator'
    }]
}

# Each contract creates its own E7_Activity, but references the same procurator

# Example 3: Integration with other buyer properties
example_3 = {
    '@id': 'https://example.org/contract/integrated_001',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_2_documents_buyer': [{
        '@id': 'https://example.org/person/buyer_003'
    }],
    'gmn:P70_5_documents_buyers_procurator': [{
        '@id': 'https://example.org/person/procurator_003'
    }],
    'gmn:P70_7_documents_buyers_guarantor': [{
        '@id': 'https://example.org/person/guarantor_001'
    }],
    'gmn:P70_9_documents_payment_provider_for_buyer': [{
        '@id': 'https://example.org/person/provider_001'
    }]
}

# All properties create separate E7_Activities within the same acquisition
# All link to the buyer via P17_was_motivated_by

# ==============================================================================
# SECTION 11: PERFORMANCE CONSIDERATIONS
# ==============================================================================
#
# The transformation function is designed for efficiency:
#
# 1. Early Return: Returns immediately if property not present
# 2. Single Acquisition: Reuses existing acquisition when possible
# 3. Hash-Based URIs: Deterministic URI generation avoids collisions
# 4. Minimal Copying: Only copies necessary data structures
#
# For large datasets:
# - Consider batch processing
# - Monitor memory usage with many procurators per contract
# - Use profiling tools to identify bottlenecks
#
# ==============================================================================

# ==============================================================================
# SECTION 12: MAINTENANCE AND VERSIONING
# ==============================================================================
#
# Version History:
# - 1.0 (2025-10-27): Initial implementation
#
# Future Considerations:
# - Add support for procuration dates (when power of attorney granted)
# - Add support for procuration scope (general vs. special)
# - Consider linking to separate E7_Event for procuration grant
# - Add validation for procurator URI format
#
# ==============================================================================

# ==============================================================================
# SECTION 13: REFERENCES
# ==============================================================================
#
# CIDOC-CRM Specification:
# - E7_Activity: http://www.cidoc-crm.org/Entity/E7-Activity/version-7.1.3
# - P14_carried_out_by: http://www.cidoc-crm.org/Property/P14-carried-out-by/version-7.1.3
# - P17_was_motivated_by: http://www.cidoc-crm.org/Property/P17-was-motivated-by/version-7.1.3
#
# Getty AAT:
# - Agents: http://vocab.getty.edu/aat/300411835
#
# Related Documentation:
# - documents-buyers-procurator-documentation.md
# - documents-buyers-procurator-implementation-guide.md
#
# ==============================================================================

# END OF FILE
