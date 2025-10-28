# ============================================================================
# GMN to CIDOC-CRM Transformation - P70.15 Documents Witness
# Python Additions for gmn_to_cidoc_transform.py
# ============================================================================
#
# INSTRUCTIONS:
# 1. Locate the transformation functions section in gmn_to_cidoc_transform.py
# 2. Find the position between transform_p70_14_documents_referenced_object 
#    and transform_p70_16_documents_sale_price_amount functions
# 3. Copy the function below and paste it in that location
# 4. Ensure the AAT_WITNESS constant is defined at the top of the file
# 5. Add the function call to the main transformation pipeline
#
# ============================================================================

# ----------------------------------------------------------------------------
# STEP 1: Add AAT Constant (if not already present)
# ----------------------------------------------------------------------------
# Add this to the constants section at the top of gmn_to_cidoc_transform.py:

AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"


# ----------------------------------------------------------------------------
# STEP 2: Add Transformation Function
# ----------------------------------------------------------------------------
# Add this function with other P70.x transformation functions:

def transform_p70_15_documents_witness(data):
    """
    Transform gmn:P70_15_documents_witness to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    
    This transformation creates E7_Activity nodes for each witness, representing their
    participation in the acquisition event. Each activity is typed with the AAT concept
    for "witness" (300028910) via P14.1_in_the_role_of.
    
    Args:
        data: Dictionary containing the contract data
        
    Returns:
        Dictionary with transformed structure
        
    Example:
        Input:
            {
                "@id": "contract001",
                "gmn:P70_15_documents_witness": ["witness_antonio", "witness_paolo"]
            }
        
        Output:
            {
                "@id": "contract001",
                "cidoc:P70_documents": [{
                    "@id": "contract001/acquisition",
                    "@type": "cidoc:E8_Acquisition",
                    "cidoc:P9_consists_of": [
                        {
                            "@id": "contract001/activity/witness_<hash1>",
                            "@type": "cidoc:E7_Activity",
                            "cidoc:P14_carried_out_by": [{
                                "@id": "witness_antonio",
                                "@type": "cidoc:E21_Person"
                            }],
                            "cidoc:P14.1_in_the_role_of": {
                                "@id": "http://vocab.getty.edu/page/aat/300028910",
                                "@type": "cidoc:E55_Type"
                            }
                        },
                        {
                            "@id": "contract001/activity/witness_<hash2>",
                            "@type": "cidoc:E7_Activity",
                            "cidoc:P14_carried_out_by": [{
                                "@id": "witness_paolo",
                                "@type": "cidoc:E21_Person"
                            }],
                            "cidoc:P14.1_in_the_role_of": {
                                "@id": "http://vocab.getty.edu/page/aat/300028910",
                                "@type": "cidoc:E55_Type"
                            }
                        }
                    ]
                }]
            }
    """
    if 'gmn:P70_15_documents_witness' not in data:
        return data
    
    witnesses = data['gmn:P70_15_documents_witness']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create E8_Acquisition if it doesn't exist
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P9_consists_of array if it doesn't exist
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Process each witness
    for witness_obj in witnesses:
        # Handle both URI strings and full object descriptions
        if isinstance(witness_obj, dict):
            witness_uri = witness_obj.get('@id', '')
            witness_data = witness_obj.copy()
        else:
            witness_uri = str(witness_obj)
            witness_data = {
                '@id': witness_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI using hash
        activity_hash = str(hash(witness_uri + 'witness'))[-8:]
        activity_uri = f"{subject_uri}/activity/witness_{activity_hash}"
        
        # Create E7_Activity for witnessing
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [witness_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_WITNESS,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the shortcut property
    del data['gmn:P70_15_documents_witness']
    return data


# ----------------------------------------------------------------------------
# STEP 3: Add to Main Pipeline
# ----------------------------------------------------------------------------
# In the transform_gmn_to_cidoc() or main transformation function,
# add this line with other P70.x transformations:

def transform_gmn_to_cidoc(item, include_internal=False):
    """
    Main transformation function.
    """
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    item = transform_p70_9_documents_payment_provider_for_buyer(item)
    item = transform_p70_10_documents_payment_recipient_for_seller(item)
    item = transform_p70_11_documents_referenced_person(item)
    item = transform_p70_12_documents_payment_through_organization(item)
    item = transform_p70_13_documents_referenced_place(item)
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)  # <-- ADD THIS LINE
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # ... remaining transformations ...
    
    return item


# ============================================================================
# VERIFICATION CHECKLIST:
# ============================================================================
#
# After adding the code, verify:
#
# [ ] AAT_WITNESS constant is defined with correct URI
# [ ] Function name is transform_p70_15_documents_witness
# [ ] Function is placed between P70.14 and P70.16 functions
# [ ] Function is called in the main transformation pipeline
# [ ] Function signature matches: def transform_p70_15_documents_witness(data):
# [ ] Docstring is present and describes the transformation
# [ ] Code handles both URI strings and dictionary objects
# [ ] Hash function generates unique activity URIs
# [ ] E8_Acquisition is created if it doesn't exist
# [ ] Each witness creates a separate E7_Activity
# [ ] Role is assigned via P14.1_in_the_role_of
# [ ] Original property is deleted after transformation
# [ ] No syntax errors (validate with Python linter)
#
# ============================================================================
# TESTING CODE:
# ============================================================================
#
# Use this code to test the transformation:

if __name__ == "__main__":
    # Test case 1: Simple witness
    test_data_1 = {
        "@id": "contract001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_15_documents_witness": ["witness_antonio"]
    }
    
    result_1 = transform_p70_15_documents_witness(test_data_1.copy())
    print("Test 1 - Simple witness:")
    print(json.dumps(result_1, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test case 2: Multiple witnesses
    test_data_2 = {
        "@id": "contract002",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_15_documents_witness": [
            "witness_antonio",
            "witness_paolo",
            "witness_giovanni"
        ]
    }
    
    result_2 = transform_p70_15_documents_witness(test_data_2.copy())
    print("Test 2 - Multiple witnesses:")
    print(json.dumps(result_2, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test case 3: Witness with full data
    test_data_3 = {
        "@id": "contract003",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_15_documents_witness": [
            {
                "@id": "witness_antonio_spinola",
                "@type": "cidoc:E21_Person",
                "cidoc:P1_is_identified_by": {
                    "@type": "cidoc:E41_Appellation",
                    "cidoc:P190_has_symbolic_content": "Antonio Spinola"
                }
            }
        ]
    }
    
    result_3 = transform_p70_15_documents_witness(test_data_3.copy())
    print("Test 3 - Witness with full data:")
    print(json.dumps(result_3, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test case 4: No witnesses (should return unchanged)
    test_data_4 = {
        "@id": "contract004",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_1_documents_seller": "seller_giovanni"
    }
    
    result_4 = transform_p70_15_documents_witness(test_data_4.copy())
    print("Test 4 - No witnesses:")
    print(json.dumps(result_4, indent=2))
    assert result_4 == test_data_4, "Data should be unchanged when no witnesses present"
    print("✓ Data unchanged as expected\n")


# ============================================================================
# INTEGRATION NOTES:
# ============================================================================
#
# 1. DEPENDENCIES:
#    - Requires uuid module for UUID generation
#    - Uses Python's built-in hash() function
#    - Compatible with Python 3.7+
#
# 2. PERFORMANCE:
#    - O(n) complexity where n is number of witnesses
#    - Hash generation is O(1)
#    - Memory efficient (processes witnesses iteratively)
#
# 3. ERROR HANDLING:
#    - Returns data unchanged if property not present
#    - Handles both string URIs and object descriptions
#    - Creates acquisition node if missing
#    - Preserves all witness properties via .copy()
#
# 4. COMPATIBILITY:
#    - Works with existing P70.x transformations
#    - Reuses acquisition node if already created
#    - Appends to existing P9_consists_of array
#    - Does not interfere with other transformation functions
#
# 5. MAINTENANCE:
#    - AAT_WITNESS constant can be updated centrally
#    - Activity URI pattern can be modified if needed
#    - Hash function can be replaced for different ID generation
#    - Easy to extend for additional witness properties
#
# ============================================================================
# COMMON ISSUES AND SOLUTIONS:
# ============================================================================
#
# Issue: NameError for AAT_WITNESS
# Solution: Ensure constant is defined at top of file
#
# Issue: Duplicate activities for same witness
# Solution: Hash function should prevent this; check witness URI consistency
#
# Issue: Missing E8_Acquisition
# Solution: Function creates it automatically if not present
#
# Issue: Witness data not preserved
# Solution: Using .copy() preserves all properties; verify this is working
#
# Issue: Wrong role assignment
# Solution: Check AAT_WITNESS constant value is correct
#
# ============================================================================
# END OF PYTHON ADDITIONS
# ============================================================================
