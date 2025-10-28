# Python Transformation Code for P70.14 Documents Referenced Object
# Add this function to gmn_to_cidoc_transform.py after transform_p70_13_documents_referenced_place()

def transform_p70_14_documents_referenced_object(data):
    """
    Transform gmn:P70_14_documents_referenced_object to full CIDOC-CRM structure:
    P67_refers_to > E1_CRM_Entity
    
    This property handles objects (legal or physical) referenced in sales contracts,
    including rights, obligations, debts, claims, privileges, and physical items.
    
    Args:
        data (dict): Document data dictionary containing GMN properties
    
    Returns:
        dict: Transformed data dictionary with CIDOC-CRM compliant structure
    
    Transformation:
        INPUT:  gmn:P70_14_documents_referenced_object
        OUTPUT: cidoc:P67_refers_to with E1_CRM_Entity type
    
    Examples:
        Simple URI reference:
        Input:
            {
                "@id": "contract:123",
                "gmn:P70_14_documents_referenced_object": ["object:water_right_1"]
            }
        Output:
            {
                "@id": "contract:123",
                "cidoc:P67_refers_to": [
                    {
                        "@id": "object:water_right_1",
                        "@type": "cidoc:E1_CRM_Entity"
                    }
                ]
            }
        
        Complex object with properties:
        Input:
            {
                "@id": "contract:456",
                "gmn:P70_14_documents_referenced_object": [
                    {
                        "@id": "object:debt_1",
                        "@type": "cidoc:E72_Legal_Object",
                        "rdfs:label": "Outstanding debt"
                    }
                ]
            }
        Output:
            {
                "@id": "contract:456",
                "cidoc:P67_refers_to": [
                    {
                        "@id": "object:debt_1",
                        "@type": "cidoc:E72_Legal_Object",
                        "rdfs:label": "Outstanding debt"
                    }
                ]
            }
    
    Notes:
        - Preserves specific entity types when present (E72_Legal_Object, E18_Physical_Thing, etc.)
        - Adds default E1_CRM_Entity type when no type specified
        - Appends to existing P67_refers_to array if present
        - Handles both simple URI strings and complex object dictionaries
        - Multiple objects are supported in a single transformation
    """
    # Check if the property exists in the data
    if 'gmn:P70_14_documents_referenced_object' not in data:
        return data
    
    # Get the list of referenced objects from the GMN property
    objects = data['gmn:P70_14_documents_referenced_object']
    
    # Initialize P67_refers_to array if it doesn't exist
    # This preserves any existing P67_refers_to data from other properties
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Process each referenced object
    for obj_obj in objects:
        if isinstance(obj_obj, dict):
            # Object is already a dictionary with properties
            # Copy it to avoid modifying the original
            obj_data = obj_obj.copy()
            
            # Add default type if not already specified
            # This preserves more specific types like E72_Legal_Object
            if '@type' not in obj_data:
                obj_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            # Object is a simple URI string
            # Create a minimal dictionary with ID and default type
            obj_uri = str(obj_obj)
            obj_data = {
                '@id': obj_uri,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add the processed object to the P67_refers_to array
        data['cidoc:P67_refers_to'].append(obj_data)
    
    # Remove the simplified GMN property after transformation
    del data['gmn:P70_14_documents_referenced_object']
    
    return data


# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================
#
# 1. Add the function above to gmn_to_cidoc_transform.py
#    - Place it after transform_p70_13_documents_referenced_place()
#    - Place it before transform_p70_15_documents_witness()
#
# 2. Add function call to main transformation pipeline
#    Find the section that calls P70 transformation functions and add:
#
#    item = transform_p70_13_documents_referenced_place(item)
#    item = transform_p70_14_documents_referenced_object(item)    # <-- ADD THIS LINE
#    item = transform_p70_15_documents_witness(item)
#
# 3. No additional imports are required for this function
#
# ============================================================================


# ============================================================================
# TEST CASES
# ============================================================================
#
# Use these test cases to verify the transformation works correctly:

def test_transform_p70_14():
    """Test suite for P70.14 transformation"""
    
    # Test Case 1: Simple URI reference
    test_1_input = {
        "@id": "contract:test_001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_14_documents_referenced_object": [
            "object:water_right_1"
        ]
    }
    test_1_expected = {
        "@id": "contract:test_001",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": [
            {
                "@id": "object:water_right_1",
                "@type": "cidoc:E1_CRM_Entity"
            }
        ]
    }
    
    # Test Case 2: Complex object with type
    test_2_input = {
        "@id": "contract:test_002",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_14_documents_referenced_object": [
            {
                "@id": "object:debt_1",
                "@type": "cidoc:E72_Legal_Object",
                "rdfs:label": "Outstanding debt"
            }
        ]
    }
    test_2_expected = {
        "@id": "contract:test_002",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": [
            {
                "@id": "object:debt_1",
                "@type": "cidoc:E72_Legal_Object",
                "rdfs:label": "Outstanding debt"
            }
        ]
    }
    
    # Test Case 3: Multiple objects
    test_3_input = {
        "@id": "contract:test_003",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_14_documents_referenced_object": [
            "object:water_right_1",
            {
                "@id": "object:easement_1",
                "@type": "cidoc:E72_Legal_Object"
            },
            "object:well_1"
        ]
    }
    test_3_expected = {
        "@id": "contract:test_003",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": [
            {
                "@id": "object:water_right_1",
                "@type": "cidoc:E1_CRM_Entity"
            },
            {
                "@id": "object:easement_1",
                "@type": "cidoc:E72_Legal_Object"
            },
            {
                "@id": "object:well_1",
                "@type": "cidoc:E1_CRM_Entity"
            }
        ]
    }
    
    # Test Case 4: Existing P67_refers_to (from other properties)
    test_4_input = {
        "@id": "contract:test_004",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": [
            {
                "@id": "place:venice",
                "@type": "cidoc:E53_Place"
            }
        ],
        "gmn:P70_14_documents_referenced_object": [
            "object:privilege_1"
        ]
    }
    test_4_expected = {
        "@id": "contract:test_004",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": [
            {
                "@id": "place:venice",
                "@type": "cidoc:E53_Place"
            },
            {
                "@id": "object:privilege_1",
                "@type": "cidoc:E1_CRM_Entity"
            }
        ]
    }
    
    # Test Case 5: Empty array (edge case)
    test_5_input = {
        "@id": "contract:test_005",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_14_documents_referenced_object": []
    }
    test_5_expected = {
        "@id": "contract:test_005",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P67_refers_to": []
    }
    
    # Test Case 6: Property not present (edge case)
    test_6_input = {
        "@id": "contract:test_006",
        "@type": "gmn:E31_2_Sales_Contract"
    }
    test_6_expected = {
        "@id": "contract:test_006",
        "@type": "gmn:E31_2_Sales_Contract"
    }
    
    # Run tests
    print("Running P70.14 transformation tests...\n")
    
    test_cases = [
        ("Simple URI", test_1_input, test_1_expected),
        ("Complex object with type", test_2_input, test_2_expected),
        ("Multiple objects", test_3_input, test_3_expected),
        ("Existing P67_refers_to", test_4_input, test_4_expected),
        ("Empty array", test_5_input, test_5_expected),
        ("Property not present", test_6_input, test_6_expected)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, input_data, expected_output in test_cases:
        result = transform_p70_14_documents_referenced_object(input_data.copy())
        
        if result == expected_output:
            print(f"✓ PASSED: {test_name}")
            passed += 1
        else:
            print(f"✗ FAILED: {test_name}")
            print(f"  Expected: {expected_output}")
            print(f"  Got: {result}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed out of {len(test_cases)} total")
    return failed == 0


# Uncomment to run tests:
# if __name__ == "__main__":
#     test_transform_p70_14()
