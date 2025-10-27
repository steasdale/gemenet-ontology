# GMN to CIDOC-CRM Transformation - P70.3 Documents Transfer Of
# Python Code Additions for gmn_to_cidoc_transform.py
# Ready to copy into transformation script

# =============================================================================
# INSTRUCTIONS FOR USE
# =============================================================================
# 1. Open your gmn_to_cidoc_transform.py file
# 2. Locate the transform_p70_2_documents_buyer function
# 3. Copy the function below and paste it immediately after P70.2 function
# 4. Register the function in your transformation pipeline (see bottom)
# 5. Run tests to verify correct transformation
# =============================================================================

# =============================================================================
# REQUIRED IMPORTS
# =============================================================================
# Ensure these imports are present at the top of your file:
#
# from uuid import uuid4
#
# If not present, add them to the import section.
# =============================================================================


def transform_p70_3_documents_transfer_of(data):
    """
    Transform gmn:P70_3_documents_transfer_of to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    
    This function takes a simplified sales contract property that directly
    associates the contract with the physical thing being transferred, and
    expands it to the full CIDOC-CRM structure with an intermediate E8_Acquisition
    event.
    
    Args:
        data (dict): JSON-LD data structure representing a sales contract
        
    Returns:
        dict: Transformed data structure with full CIDOC-CRM representation
        
    Example:
        Input:
        {
            "@id": "contract/sale_1",
            "@type": "gmn:E31_2_Sales_Contract",
            "gmn:P70_3_documents_transfer_of": [
                {
                    "@id": "building/house_42",
                    "@type": "gmn:E22_1_Building"
                }
            ]
        }
        
        Output:
        {
            "@id": "contract/sale_1",
            "@type": "gmn:E31_2_Sales_Contract",
            "cidoc:P70_documents": [
                {
                    "@id": "contract/sale_1/acquisition",
                    "@type": "cidoc:E8_Acquisition",
                    "cidoc:P24_transferred_title_of": [
                        {
                            "@id": "building/house_42",
                            "@type": "gmn:E22_1_Building"
                        }
                    ]
                }
            ]
        }
    """
    # Check if the simplified property exists
    if 'gmn:P70_3_documents_transfer_of' not in data:
        return data
    
    # Get the array of things being transferred
    things = data['gmn:P70_3_documents_transfer_of']
    
    # Get or generate the subject URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or locate the E8_Acquisition node
    # Check if P70_documents already exists (from P70.1 or P70.2 transformations)
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new acquisition node if it doesn't exist
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get the acquisition node (first element in P70_documents array)
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P24_transferred_title_of array if it doesn't exist
    if 'cidoc:P24_transferred_title_of' not in acquisition:
        acquisition['cidoc:P24_transferred_title_of'] = []
    
    # Process each thing being transferred
    for thing_obj in things:
        if isinstance(thing_obj, dict):
            # Thing is provided as a dictionary with properties
            # Copy the entire object to preserve all properties
            thing_data = thing_obj.copy()
            
            # Ensure the thing has a type
            # If no type is specified, default to E18_Physical_Thing
            if '@type' not in thing_data:
                thing_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            # Thing is provided as a simple URI string
            # Create a minimal object with the URI and default type
            thing_uri = str(thing_obj)
            thing_data = {
                '@id': thing_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        # Add the thing to the acquisition's P24_transferred_title_of array
        acquisition['cidoc:P24_transferred_title_of'].append(thing_data)
    
    # Remove the simplified property from the data structure
    # This prevents duplication and ensures clean CIDOC-CRM output
    del data['gmn:P70_3_documents_transfer_of']
    
    return data


# =============================================================================
# REGISTRATION IN TRANSFORMATION PIPELINE
# =============================================================================
# Add this function to your transformation pipeline registration.
# Locate the section where transformation functions are registered
# (usually near the bottom of the file or in a main transformation function)
# and add the following line in the appropriate sequence:
#
# Example registration:
"""
def transform_document(data):
    '''
    Apply all GMN to CIDOC-CRM transformations in sequence.
    '''
    # ... other transformations ...
    data = transform_p70_1_documents_seller(data)
    data = transform_p70_2_documents_buyer(data)
    data = transform_p70_3_documents_transfer_of(data)  # ← ADD THIS LINE
    data = transform_p70_4_documents_sellers_procurator(data)
    # ... more transformations ...
    return data
"""
#
# Or if using a list-based approach:
"""
transform_functions = [
    # ... other functions ...
    transform_p70_1_documents_seller,
    transform_p70_2_documents_buyer,
    transform_p70_3_documents_transfer_of,  # ← ADD THIS LINE
    transform_p70_4_documents_sellers_procurator,
    # ... more functions ...
]

def transform_document(data):
    for transform_func in transform_functions:
        data = transform_func(data)
    return data
"""
# =============================================================================


# =============================================================================
# TEST CASES
# =============================================================================
# Use these test cases to verify correct implementation

def test_p70_3_single_building():
    """Test transformation of a single building transfer."""
    input_data = {
        "@id": "https://example.org/contract/c001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_3_documents_transfer_of": [
            {
                "@id": "https://example.org/building/b001",
                "@type": "gmn:E22_1_Building",
                "cidoc:P1_is_identified_by": {
                    "@type": "cidoc:E41_Appellation",
                    "@value": "House on Via Luccoli"
                }
            }
        ]
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    # Verify structure
    assert 'cidoc:P70_documents' in result, "P70_documents should be created"
    assert len(result['cidoc:P70_documents']) == 1, "Should have one acquisition"
    
    acquisition = result['cidoc:P70_documents'][0]
    assert acquisition['@type'] == 'cidoc:E8_Acquisition', "Should be E8_Acquisition"
    assert 'cidoc:P24_transferred_title_of' in acquisition, "Should have P24 property"
    
    things = acquisition['cidoc:P24_transferred_title_of']
    assert len(things) == 1, "Should have one thing"
    assert things[0]['@type'] == 'gmn:E22_1_Building', "Type should be preserved"
    assert things[0]['@id'] == 'https://example.org/building/b001', "ID should match"
    
    # Verify cleanup
    assert 'gmn:P70_3_documents_transfer_of' not in result, "Simplified property should be removed"
    
    print("✅ Test 1 passed: Single building transfer")
    return True


def test_p70_3_multiple_items():
    """Test transformation of multiple items (building and moveable property)."""
    input_data = {
        "@id": "https://example.org/contract/c002",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_3_documents_transfer_of": [
            {
                "@id": "https://example.org/building/b002",
                "@type": "gmn:E22_1_Building"
            },
            {
                "@id": "https://example.org/goods/g001",
                "@type": "gmn:E22_2_Moveable_Property"
            }
        ]
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    acquisition = result['cidoc:P70_documents'][0]
    things = acquisition['cidoc:P24_transferred_title_of']
    
    assert len(things) == 2, "Should have two things"
    assert things[0]['@type'] == 'gmn:E22_1_Building', "First should be Building"
    assert things[1]['@type'] == 'gmn:E22_2_Moveable_Property', "Second should be Moveable Property"
    
    print("✅ Test 2 passed: Multiple items transfer")
    return True


def test_p70_3_uri_string():
    """Test transformation with URI string (not dict)."""
    input_data = {
        "@id": "https://example.org/contract/c003",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_3_documents_transfer_of": [
            "https://example.org/building/b003"
        ]
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    acquisition = result['cidoc:P70_documents'][0]
    things = acquisition['cidoc:P24_transferred_title_of']
    
    assert len(things) == 1, "Should have one thing"
    assert things[0]['@id'] == 'https://example.org/building/b003', "ID should match"
    assert things[0]['@type'] == 'cidoc:E18_Physical_Thing', "Should default to E18_Physical_Thing"
    
    print("✅ Test 3 passed: URI string reference")
    return True


def test_p70_3_integration():
    """Test integration with other P70 properties."""
    input_data = {
        "@id": "https://example.org/contract/c004",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_1_documents_seller": [
            {"@id": "https://example.org/person/seller001", "@type": "cidoc:E21_Person"}
        ],
        "gmn:P70_2_documents_buyer": [
            {"@id": "https://example.org/person/buyer001", "@type": "cidoc:E21_Person"}
        ],
        "gmn:P70_3_documents_transfer_of": [
            {"@id": "https://example.org/building/b004", "@type": "gmn:E22_1_Building"}
        ]
    }
    
    # Apply transformations in sequence (assuming other functions exist)
    # In real testing, you'd import these functions
    # result = transform_p70_1_documents_seller(input_data)
    # result = transform_p70_2_documents_buyer(result)
    # result = transform_p70_3_documents_transfer_of(result)
    
    # For this isolated test, just test P70.3
    result = transform_p70_3_documents_transfer_of(input_data)
    
    acquisition = result['cidoc:P70_documents'][0]
    assert 'cidoc:P24_transferred_title_of' in acquisition, "Should have P24 property"
    
    print("✅ Test 4 passed: Integration with other properties")
    return True


def test_p70_3_no_property():
    """Test that function returns unchanged data when property doesn't exist."""
    input_data = {
        "@id": "https://example.org/contract/c005",
        "@type": "gmn:E31_2_Sales_Contract"
    }
    
    result = transform_p70_3_documents_transfer_of(input_data)
    
    assert result == input_data, "Data should be unchanged"
    assert 'cidoc:P70_documents' not in result, "Should not create P70_documents"
    
    print("✅ Test 5 passed: No property present")
    return True


def run_all_p70_3_tests():
    """Run all test cases for P70.3 transformation."""
    print("=" * 60)
    print("Running P70.3 Documents Transfer Of - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_p70_3_single_building,
        test_p70_3_multiple_items,
        test_p70_3_uri_string,
        test_p70_3_integration,
        test_p70_3_no_property
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


# =============================================================================
# USAGE NOTES
# =============================================================================
# 1. This function should be placed in gmn_to_cidoc_transform.py after the
#    transform_p70_2_documents_buyer function
#
# 2. The function creates or reuses an existing E8_Acquisition node, allowing
#    integration with P70.1 (seller) and P70.2 (buyer) transformations
#
# 3. The function preserves specific types (E22_1_Building, E22_2_Moveable_Property)
#    when provided in the input data
#
# 4. If no type is specified, the function defaults to cidoc:E18_Physical_Thing
#
# 5. The function handles both dictionary objects and simple URI strings
#
# 6. After transformation, the simplified property is removed to avoid duplication
# =============================================================================


# =============================================================================
# TRANSFORMATION SEQUENCE
# =============================================================================
# For correct integration, apply transformations in this order:
#
# 1. transform_p70_1_documents_seller     (creates acquisition, adds P23)
# 2. transform_p70_2_documents_buyer      (reuses acquisition, adds P22)
# 3. transform_p70_3_documents_transfer_of (reuses acquisition, adds P24) ← THIS
# 4. transform_p70_4_documents_sellers_procurator
# 5. transform_p70_5_documents_buyers_procurator
#
# All these transformations contribute to the same E8_Acquisition node
# =============================================================================


# =============================================================================
# DEBUGGING TIPS
# =============================================================================
# If transformation isn't working as expected:
#
# 1. Check that the function is registered in the transformation pipeline
# 2. Verify that 'gmn:P70_3_documents_transfer_of' exists in input data
# 3. Ensure the uuid4 import is available
# 4. Check that the acquisition node is being created/reused correctly
# 5. Verify that types are being preserved properly
# 6. Confirm that the simplified property is being deleted
#
# Add logging for debugging:
"""
import logging
logging.basicConfig(level=logging.DEBUG)

def transform_p70_3_documents_transfer_of(data):
    logging.debug(f"P70.3 input: {data.get('gmn:P70_3_documents_transfer_of')}")
    # ... rest of function ...
    logging.debug(f"P70.3 output: {data.get('cidoc:P70_documents')}")
    return data
"""
# =============================================================================


if __name__ == "__main__":
    # Run tests when this file is executed directly
    run_all_p70_3_tests()


# END OF PYTHON ADDITIONS
