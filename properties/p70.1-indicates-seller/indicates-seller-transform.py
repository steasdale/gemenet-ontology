# Python Additions for gmn:P70_1_indicates_seller
# Ready-to-copy code for gmn_to_cidoc_transform.py

# ==============================================================================
# REQUIRED CONSTANTS
# ==============================================================================
# Add these AAT constants at the top of gmn_to_cidoc_transform.py if not present

# AAT Terms for sale transactions
AAT_SALE_EVENT = 'http://vocab.getty.edu/aat/300054751'  # sale (event)
AAT_SELLER_ROLE = 'http://vocab.getty.edu/aat/300410369'  # sellers (people)
CIDOC_P14 = 'http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by'


# ==============================================================================
# TRANSFORMATION FUNCTION
# ==============================================================================
# Location: Add to sales contract transformation functions section
# Suggested placement: Around line 360-400, with other P70 transform functions

def transform_p70_1_indicates_seller(data):
    """
    Transform gmn:P70_1_indicates_seller to full CIDOC-CRM structure using E13 Attribute Assignment:
    
    E70_Document 
      > P70_documents 
      > E7_Activity (type: sale)
        > P140i_was_attributed_by 
        > E13_Attribute_Assignment
          > P141_assigned > E21_Person (seller)
          > P177_assigned_property_of_type > E55_Type ("P14 carried out by")
          > P14.1_in_the_role_of > E55_Type ("seller")
    
    This transformation uses the E13_Attribute_Assignment pattern to formally assign
    the "carried out by" attribute to the sale event, specifying the seller's role.
    
    The E13 pattern provides:
    - Explicit role specification via P14.1_in_the_role_of
    - Property type documentation via P177_assigned_property_of_type
    - Support for multiple sellers with clear role attribution
    - Provenance capabilities for the attribution itself
    
    Args:
        data (dict): The item data dictionary containing the document and 
                     optional gmn:P70_1_indicates_seller property.
    
    Returns:
        dict: Transformed item with full CIDOC-CRM E13 pattern structure.
    
    Example Input:
        {
            "@id": "contract_001",
            "@type": "cidoc:E70_Document",
            "cidoc:P2_has_type": {
                "@type": "cidoc:E55_Type",
                "rdfs:label": "sales contract"
            },
            "gmn:P70_1_indicates_seller": [
                {
                    "@id": "person_001",
                    "@type": "cidoc:E21_Person"
                }
            ]
        }
    
    Example Output:
        {
            "@id": "contract_001",
            "@type": "cidoc:E70_Document",
            "cidoc:P2_has_type": {
                "@type": "cidoc:E55_Type",
                "rdfs:label": "sales contract"
            },
            "cidoc:P70_documents": [
                {
                    "@id": "contract_001/sale",
                    "@type": "cidoc:E7_Activity",
                    "cidoc:P2_has_type": {
                        "@id": "http://vocab.getty.edu/aat/300054751",
                        "@type": "cidoc:E55_Type",
                        "rdfs:label": "sale"
                    },
                    "cidoc:P140i_was_attributed_by": [
                        {
                            "@id": "contract_001/attribution/seller_abc12345",
                            "@type": "cidoc:E13_Attribute_Assignment",
                            "cidoc:P141_assigned": {
                                "@id": "person_001",
                                "@type": "cidoc:E21_Person"
                            },
                            "cidoc:P177_assigned_property_of_type": {
                                "@id": "http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by",
                                "@type": "cidoc:E55_Type",
                                "rdfs:label": "P14 carried out by"
                            },
                            "cidoc:P14.1_in_the_role_of": {
                                "@id": "http://vocab.getty.edu/aat/300410369",
                                "@type": "cidoc:E55_Type",
                                "rdfs:label": "seller"
                            }
                        }
                    ]
                }
            ]
        }
    """
    # Check if the property exists in the data
    if 'gmn:P70_1_indicates_seller' not in data:
        return data
    
    # Get the list of sellers from the property
    sellers = data['gmn:P70_1_indicates_seller']
    
    # Get or generate the subject URI (document URI)
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create E7_Activity (sale) if it doesn't exist
    # Check if cidoc:P70_documents exists and has content
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        sale_uri = f"{subject_uri}/sale"
        data['cidoc:P70_documents'] = [{
            '@id': sale_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_SALE_EVENT,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'sale'
            }
        }]
    
    # Get reference to the sale event
    sale_event = data['cidoc:P70_documents'][0]
    
    # Initialize P140i_was_attributed_by if not present
    if 'cidoc:P140i_was_attributed_by' not in sale_event:
        sale_event['cidoc:P140i_was_attributed_by'] = []
    
    # Create E13_Attribute_Assignment for each seller
    for seller_obj in sellers:
        # Handle seller data (dict or string format)
        if isinstance(seller_obj, dict):
            seller_data = seller_obj.copy()
            seller_uri = seller_data.get('@id', f"urn:uuid:{uuid4()}")
            # Ensure @type is present
            if '@type' not in seller_data:
                seller_data['@type'] = 'cidoc:E21_Person'
        else:
            # String format (just URI)
            seller_uri = str(seller_obj)
            seller_data = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique attribution URI using hash
        attribution_hash = str(hash(seller_uri + 'seller'))[-8:]
        attribution_uri = f"{subject_uri}/attribution/seller_{attribution_hash}"
        
        # Create E13_Attribute_Assignment
        # This formally assigns the seller to the sale event via P14 carried out by
        attribution = {
            '@id': attribution_uri,
            '@type': 'cidoc:E13_Attribute_Assignment',
            # P141: Assigns the person as the value
            'cidoc:P141_assigned': seller_data,
            # P177: Specifies the property type being assigned (P14 carried out by)
            'cidoc:P177_assigned_property_of_type': {
                '@id': CIDOC_P14,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'P14 carried out by'
            },
            # P14.1: Specifies the role (seller)
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_SELLER_ROLE,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'seller'
            }
        }
        
        # Add the E13 attribution to the sale event
        sale_event['cidoc:P140i_was_attributed_by'].append(attribution)
    
    # Remove the simplified property after transformation
    del data['gmn:P70_1_indicates_seller']
    
    return data


# ==============================================================================
# FUNCTION INTEGRATION
# ==============================================================================
# Add this function call to the transform_item() function
# Location: Around line 1600-1700 in the sales contract properties section

# In transform_item() function, add:
#
# def transform_item(item, include_internal=False):
#     """Transform a single item, applying all transformation rules."""
#     
#     # ... other transformations ...
#     
#     # Sales contract properties (P70.1-P70.17)
#     item = transform_p70_1_indicates_seller(item)      # ADD THIS LINE
#     item = transform_p70_2_indicates_buyer(item)
#     item = transform_p70_3_indicates_transfer_of(item)
#     # ... rest of P70 functions ...

# ==============================================================================
# DEPENDENCIES
# ==============================================================================

# Required imports (should be at top of file):
# from uuid import uuid4

# Required constants (should be defined at module level):
# AAT_SALE_EVENT = 'http://vocab.getty.edu/aat/300054751'
# AAT_SELLER_ROLE = 'http://vocab.getty.edu/aat/300410369'
# CIDOC_P14 = 'http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by'

# Verify these are present in gmn_to_cidoc_transform.py


# ==============================================================================
# TESTING CODE
# ==============================================================================
# Use this code to test the transformation function

def test_transform_p70_1_indicates_seller():
    """Test cases for the transform_p70_1_indicates_seller function with E13 pattern."""
    
    # Test 1: Single seller with E13 attribution
    print("Test 1: Single seller with E13 attribution")
    test_data_1 = {
        "@id": "http://example.org/contract/sale_001",
        "@type": "cidoc:E70_Document",
        "cidoc:P2_has_type": {
            "@id": "sales_contract_type",
            "@type": "cidoc:E55_Type",
            "rdfs:label": "sales contract"
        },
        "gmn:P70_1_indicates_seller": [
            {
                "@id": "http://example.org/person/giovanni_rossi",
                "@type": "cidoc:E21_Person",
                "cidoc:P1_is_identified_by": [
                    {
                        "@type": "cidoc:E41_Appellation",
                        "cidoc:P190_has_symbolic_content": "Giovanni Rossi"
                    }
                ]
            }
        ]
    }
    result_1 = transform_p70_1_indicates_seller(test_data_1)
    
    # Validate E7 activity exists
    has_e7 = 'cidoc:P70_documents' in result_1
    # Validate E13 attribution exists
    e13_exists = False
    if has_e7:
        sale = result_1['cidoc:P70_documents'][0]
        e13_exists = 'cidoc:P140i_was_attributed_by' in sale
    # Validate E13 has all required components
    e13_complete = False
    if e13_exists:
        e13 = sale['cidoc:P140i_was_attributed_by'][0]
        e13_complete = (
            'cidoc:P141_assigned' in e13 and
            'cidoc:P177_assigned_property_of_type' in e13 and
            'cidoc:P14.1_in_the_role_of' in e13
        )
    
    print("Has E7 Activity:", "✓" if has_e7 else "✗")
    print("Has E13 Attribution:", "✓" if e13_exists else "✗")
    print("E13 Complete:", "✓" if e13_complete else "✗")
    print()
    
    # Test 2: Multiple co-sellers (multiple E13 attributions)
    print("Test 2: Multiple co-sellers")
    test_data_2 = {
        "@id": "http://example.org/contract/sale_002",
        "@type": "cidoc:E70_Document",
        "cidoc:P2_has_type": {
            "@id": "sales_contract_type",
            "@type": "cidoc:E55_Type"
        },
        "gmn:P70_1_indicates_seller": [
            {
                "@id": "http://example.org/person/marco_bianchi",
                "@type": "cidoc:E21_Person"
            },
            {
                "@id": "http://example.org/person/paolo_verdi",
                "@type": "cidoc:E21_Person"
            }
        ]
    }
    result_2 = transform_p70_1_indicates_seller(test_data_2)
    sale_2 = result_2['cidoc:P70_documents'][0]
    attributions_count = len(sale_2['cidoc:P140i_was_attributed_by'])
    print("Number of E13 attributions:", attributions_count)
    print("Expected: 2, Got:", attributions_count, "✓" if attributions_count == 2 else "✗")
    print()
    
    # Test 3: E13 structure validation
    print("Test 3: E13 structure validation")
    test_data_3 = {
        "@id": "http://example.org/contract/sale_003",
        "@type": "cidoc:E70_Document",
        "gmn:P70_1_indicates_seller": [
            {
                "@id": "http://example.org/person/antonio_ferrari",
                "@type": "cidoc:E21_Person"
            }
        ]
    }
    result_3 = transform_p70_1_indicates_seller(test_data_3)
    sale_3 = result_3['cidoc:P70_documents'][0]
    e13_3 = sale_3['cidoc:P140i_was_attributed_by'][0]
    
    # Check P141_assigned points to seller
    p141_correct = e13_3['cidoc:P141_assigned']['@id'] == "http://example.org/person/antonio_ferrari"
    # Check P177 points to P14
    p177_correct = e13_3['cidoc:P177_assigned_property_of_type']['@id'] == CIDOC_P14
    # Check P14.1 points to seller role
    p14_1_correct = e13_3['cidoc:P14.1_in_the_role_of']['@id'] == AAT_SELLER_ROLE
    
    print("P141_assigned correct:", "✓" if p141_correct else "✗")
    print("P177_assigned_property_of_type correct:", "✓" if p177_correct else "✗")
    print("P14.1_in_the_role_of correct:", "✓" if p14_1_correct else "✗")
    print()
    
    # Test 4: URI string format
    print("Test 4: URI string format")
    test_data_4 = {
        "@id": "http://example.org/contract/sale_004",
        "@type": "cidoc:E70_Document",
        "gmn:P70_1_indicates_seller": [
            "http://example.org/person/giuseppe_russo"
        ]
    }
    result_4 = transform_p70_1_indicates_seller(test_data_4)
    sale_4 = result_4['cidoc:P70_documents'][0]
    e13_4 = sale_4['cidoc:P140i_was_attributed_by'][0]
    seller_4 = e13_4['cidoc:P141_assigned']
    
    has_type = '@type' in seller_4
    correct_type = seller_4.get('@type') == 'cidoc:E21_Person'
    print("Seller has @type:", "✓" if has_type else "✗")
    print("@type is E21_Person:", "✓" if correct_type else "✗")
    print()
    
    # Test 5: Existing E7_Activity reuse
    print("Test 5: Existing E7_Activity reuse")
    test_data_5 = {
        "@id": "http://example.org/contract/sale_005",
        "@type": "cidoc:E70_Document",
        "cidoc:P70_documents": [
            {
                "@id": "http://example.org/contract/sale_005/sale",
                "@type": "cidoc:E7_Activity",
                "cidoc:P2_has_type": {
                    "@id": AAT_SALE_EVENT,
                    "@type": "cidoc:E55_Type"
                },
                "existing_property": "preserved"
            }
        ],
        "gmn:P70_1_indicates_seller": [
            {
                "@id": "http://example.org/person/seller_001",
                "@type": "cidoc:E21_Person"
            }
        ]
    }
    result_5 = transform_p70_1_indicates_seller(test_data_5)
    sale_5 = result_5['cidoc:P70_documents'][0]
    
    has_attribution = 'cidoc:P140i_was_attributed_by' in sale_5
    existing_preserved = sale_5.get('existing_property') == 'preserved'
    print("E13 attribution added:", "✓" if has_attribution else "✗")
    print("Existing properties preserved:", "✓" if existing_preserved else "✗")
    print()
    
    # Test 6: No seller property (should return unchanged)
    print("Test 6: No seller property")
    test_data_6 = {
        "@id": "http://example.org/contract/sale_006",
        "@type": "cidoc:E70_Document"
    }
    result_6 = transform_p70_1_indicates_seller(test_data_6)
    unchanged = result_6 == test_data_6
    print("Data unchanged:", "✓" if unchanged else "✗")
    print()

# Run tests (uncomment to execute):
# test_transform_p70_1_indicates_seller()


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

# Example 1: Transform a single contract with E13 pattern
"""
from gmn_to_cidoc_transform import transform_p70_1_indicates_seller

contract = {
    "@id": "contract_001",
    "@type": "cidoc:E70_Document",
    "cidoc:P2_has_type": {
        "@type": "cidoc:E55_Type",
        "rdfs:label": "sales contract"
    },
    "gmn:P70_1_indicates_seller": [
        {
            "@id": "person_001",
            "@type": "cidoc:E21_Person"
        }
    ]
}

transformed = transform_p70_1_indicates_seller(contract)

# Result will have E7 > P140i > E13 structure with:
# - E13 P141 pointing to person_001
# - E13 P177 pointing to CIDOC P14
# - E13 P14.1 pointing to AAT seller role
"""

# Example 2: Transform as part of full pipeline
"""
from gmn_to_cidoc_transform import transform_item

contract = {
    "@id": "contract_001",
    "@type": "cidoc:E70_Document",
    "cidoc:P2_has_type": {"@type": "cidoc:E55_Type", "rdfs:label": "sales contract"},
    "gmn:P70_1_indicates_seller": [{"@id": "person_001"}],
    "gmn:P70_2_indicates_buyer": [{"@id": "person_002"}]
}

# This will apply ALL transformation functions including P70.1 with E13 pattern
transformed = transform_item(contract)
"""


# ==============================================================================
# IMPLEMENTATION CHECKLIST
# ==============================================================================

# After adding this function to gmn_to_cidoc_transform.py:
# [ ] Function is placed in sales contract section (around line 360-400)
# [ ] uuid4 is imported at top of file
# [ ] AAT constants are defined (AAT_SALE_EVENT, AAT_SELLER_ROLE, CIDOC_P14)
# [ ] Function is called in transform_item()
# [ ] Function is called in correct sequence (with other P70 functions)
# [ ] Tests pass successfully
# [ ] E13 structure is complete (P141, P177, P14.1)
# [ ] Integration with other P70 properties works correctly
# [ ] No errors when processing sample data


# ==============================================================================
# PERFORMANCE NOTES
# ==============================================================================

# Expected performance characteristics:
# - Single seller: < 2ms (E13 adds slight overhead vs direct links)
# - Multiple sellers: < 10ms (linear with number of sellers)
# - Memory: O(n) where n = number of sellers
# - Safe for large-scale batch processing
#
# The E13 pattern adds minimal overhead because:
# - Hash generation is constant time
# - Dictionary operations are O(1)
# - URI construction is string concatenation


# ==============================================================================
# E13 PATTERN EXPLANATION
# ==============================================================================

# The E13_Attribute_Assignment pattern provides formal attribution:
#
# 1. WHAT IS BEING ATTRIBUTED
#    The relationship "P14 carried out by" (via P177)
#
# 2. TO WHAT ENTITY
#    The sale event (E7_Activity)
#
# 3. WITH WHAT VALUE
#    The seller person (E21_Person) (via P141)
#
# 4. IN WHAT ROLE
#    As "seller" (via P14.1)
#
# This reads as:
# "The sale event was attributed by [an assignment] which assigned 
#  [the person] as the value of [P14 carried out by] in the role of [seller]"


# ==============================================================================
# ERROR HANDLING
# ==============================================================================

# The function includes these safety features:
# 1. Early return if property not present
# 2. Handles both dict and string formats for sellers
# 3. Generates UUID if document has no @id
# 4. Creates E7_Activity if not present (with AAT type)
# 5. Reuses existing E7_Activity if present
# 6. Ensures @type is present on all sellers
# 7. Preserves all seller data and metadata
# 8. Generates unique E13 URIs via hashing
# 9. Creates complete E13 structure with all three links (P141, P177, P14.1)


# ==============================================================================
# RELATED FUNCTIONS
# ==============================================================================

# This function works in conjunction with:
# - transform_p70_2_indicates_buyer() - for buyer E13 attribution
# - transform_p70_3_indicates_transfer_of() - for object/property being sold
# - transform_p70_4_indicates_sellers_procurator() - for seller's procurator
# - transform_p70_6_indicates_sellers_guarantor() - for seller's guarantor

# All these functions operate on the same E7_Activity structure,
# so they can be used together in any combination.


# ==============================================================================
# ADVANTAGES OF E13 OVER DIRECT P14
# ==============================================================================

# Traditional approach (not used):
# E7_Activity --P14_carried_out_by--> E21_Person
#
# Problems:
# - No role specification (seller vs buyer vs other)
# - No property type documentation
# - Difficult to add attribution metadata
# - Cannot distinguish multiple participant types
#
# E13 approach (used in GMN):
# E7_Activity --P140i--> E13 --P141--> E21_Person
#                         ├─P177--> "P14"
#                         └─P14.1--> "seller"
#
# Advantages:
# - Explicit role via P14.1
# - Property type via P177
# - Extensible for metadata (time, place, agent)
# - Clear separation of different roles
# - Follows CIDOC-CRM best practices


# ==============================================================================
# DEBUGGING TIPS
# ==============================================================================

# If transformation is not working correctly:
#
# 1. Check AAT constants are defined:
#    print(AAT_SALE_EVENT, AAT_SELLER_ROLE, CIDOC_P14)
#
# 2. Verify E7 creation:
#    print('cidoc:P70_documents' in result)
#
# 3. Check E13 structure:
#    e13 = result['cidoc:P70_documents'][0]['cidoc:P140i_was_attributed_by'][0]
#    print('P141' in e13, 'P177' in e13, 'P14.1' in e13)
#
# 4. Validate seller data:
#    seller = e13['cidoc:P141_assigned']
#    print(seller.get('@id'), seller.get('@type'))
#
# 5. Check role and property types:
#    print(e13['cidoc:P177_assigned_property_of_type']['@id'])
#    print(e13['cidoc:P14.1_in_the_role_of']['@id'])


# ==============================================================================
# END OF PYTHON ADDITIONS
# ==============================================================================
