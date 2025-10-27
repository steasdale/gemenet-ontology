# Python Additions for gmn_to_cidoc_transform.py
# Property: P70.7 documents buyer's guarantor
# 
# This file contains the transformation function for gmn:P70_7_documents_buyers_guarantor

# ============================================================================
# SECTION 1: VERIFY AAT CONSTANT EXISTS (should be near top of file, ~line 30)
# ============================================================================

# Verify this constant is defined. If not, add it:
AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"


# ============================================================================
# SECTION 2: VERIFY HELPER FUNCTION EXISTS (should be around line 564-629)
# ============================================================================

# If the generic guarantor transformation helper does NOT exist, add this function:
# (If P70.6 seller's guarantor is already implemented, this should exist)

def transform_guarantor_property(data, property_name, motivated_by_property):
    """
    Generic function to transform guarantor properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    
    Args:
        data: Item data dictionary
        property_name: The guarantor property to transform
        motivated_by_property: Property linking to the party being guaranteed
                              (P22_transferred_title_to for buyer, 
                               P23_transferred_title_from for seller)
    
    Returns:
        Transformed data dictionary
    """
    if property_name not in data:
        return data
    
    guarantors = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition node exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure P9_consists_of exists
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Find the party being guaranteed (buyer or seller)
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    # Create E7_Activity for each guarantor
    for guarantor_obj in guarantors:
        # Handle both dict and string representations
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI using hash
        activity_hash = str(hash(guarantor_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
        
        # Create the guaranteeing activity node
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add motivation link to the party being guaranteed (if present)
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the shortcut property
    del data[property_name]
    return data


# ============================================================================
# SECTION 3: MAIN TRANSFORMATION FUNCTION (insert after P70.6, before P70.8)
# ============================================================================

# Find this function in the file (should be around line 632-635):
# def transform_p70_6_documents_sellers_guarantor(data):
#     """Transform gmn:P70_6_documents_sellers_guarantor to full CIDOC-CRM structure."""
#     return transform_guarantor_property(data, 'gmn:P70_6_documents_sellers_guarantor', 
#                                        'cidoc:P23_transferred_title_from')

# IMMEDIATELY AFTER the P70.6 function, add this P70.7 function:

def transform_p70_7_documents_buyers_guarantor(data):
    """Transform gmn:P70_7_documents_buyers_guarantor to full CIDOC-CRM structure."""
    return transform_guarantor_property(data, 'gmn:P70_7_documents_buyers_guarantor', 
                                       'cidoc:P22_transferred_title_to')


# ============================================================================
# SECTION 4: ADD FUNCTION CALL IN transform_item() (around line 2200-2300)
# ============================================================================

# In the transform_item() function, find the P70 properties section.
# It should look like this:
#
#     # Sales contract properties (P70.1-P70.17)
#     item = transform_p70_1_documents_seller(item)
#     item = transform_p70_2_documents_buyer(item)
#     item = transform_p70_3_documents_transfer_of(item)
#     item = transform_p70_4_documents_sellers_procurator(item)
#     item = transform_p70_5_documents_buyers_procurator(item)
#     item = transform_p70_6_documents_sellers_guarantor(item)
#     item = transform_p70_8_documents_broker(item)
#     ...
#
# INSERT this line AFTER P70.6 and BEFORE P70.8:

    item = transform_p70_7_documents_buyers_guarantor(item)

# The result should look like:
#
#     item = transform_p70_6_documents_sellers_guarantor(item)
#     item = transform_p70_7_documents_buyers_guarantor(item)  # <-- NEW LINE
#     item = transform_p70_8_documents_broker(item)


# ============================================================================
# INSTALLATION INSTRUCTIONS
# ============================================================================

# STEP 1: Verify AAT Constant
# -----------------------------------------------------------------------------
# Check if AAT_GUARANTOR is defined near the top of the file (~line 30)
# If not present, add:
#     AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"

# STEP 2: Verify Helper Function  
# -----------------------------------------------------------------------------
# Check if transform_guarantor_property() exists (should be around line 564-629)
# This should already exist if P70.6 (seller's guarantor) is implemented
# If not present, copy the entire helper function from SECTION 2 above

# STEP 3: Add Main Transformation Function
# -----------------------------------------------------------------------------
# 1. Find: def transform_p70_6_documents_sellers_guarantor(data):
# 2. After that function ends, add the P70.7 function from SECTION 3

# STEP 4: Add Function Call
# -----------------------------------------------------------------------------
# 1. Find the transform_item() function
# 2. Locate the P70 properties transformation section
# 3. Find the line: item = transform_p70_6_documents_sellers_guarantor(item)
# 4. After that line, add: item = transform_p70_7_documents_buyers_guarantor(item)

# STEP 5: Verify Installation
# -----------------------------------------------------------------------------
# Run these checks:

# Check function exists:
# $ grep -n "def transform_p70_7_documents_buyers_guarantor" gmn_to_cidoc_transform.py

# Check function is called:
# $ grep -n "transform_p70_7_documents_buyers_guarantor(item)" gmn_to_cidoc_transform.py

# Check correct sequence:
# $ grep -A 1 "transform_p70_6_documents_sellers_guarantor(item)" gmn_to_cidoc_transform.py
# Should show P70.7 on the next line

# STEP 6: Test Installation
# -----------------------------------------------------------------------------
# Create test file test_p70_7.json:

TEST_INPUT = '''
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/ontology#"
  },
  "@graph": [{
    "@id": "http://example.org/contract/test001",
    "@type": "gmn:E31_2_Sales_Contract",
    "gmn:P70_2_documents_buyer": [{
      "@id": "http://example.org/person/buyer001"
    }],
    "gmn:P70_7_documents_buyers_guarantor": [{
      "@id": "http://example.org/person/guarantor001"
    }]
  }]
}
'''

# Run transformation:
# $ python gmn_to_cidoc_transform.py test_p70_7.json > output.json

# Verify output has:
# - cidoc:P70_documents with E8_Acquisition
# - cidoc:P9_consists_of with E7_Activity  
# - cidoc:P14_carried_out_by linking to guarantor
# - cidoc:P14.1_in_the_role_of linking to AAT_GUARANTOR
# - cidoc:P17_was_motivated_by linking to buyer
# - NO gmn:P70_7_documents_buyers_guarantor (should be removed)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

# Example 1: Single guarantor transformation
# INPUT:
example_1_input = {
    "@id": "ex:Contract_001",
    "gmn:P70_7_documents_buyers_guarantor": [
        {"@id": "ex:Guarantor_Marco"}
    ],
    "cidoc:P70_documents": [{
        "@id": "ex:Contract_001/acquisition",
        "@type": "cidoc:E8_Acquisition",
        "cidoc:P22_transferred_title_to": [
            {"@id": "ex:Buyer_Giovanni"}
        ]
    }]
}

# OUTPUT (after transformation):
example_1_output = {
    "@id": "ex:Contract_001",
    "cidoc:P70_documents": [{
        "@id": "ex:Contract_001/acquisition",
        "@type": "cidoc:E8_Acquisition",
        "cidoc:P22_transferred_title_to": [
            {"@id": "ex:Buyer_Giovanni"}
        ],
        "cidoc:P9_consists_of": [{
            "@id": "ex:Contract_001/activity/guarantor_XXXXXXXX",
            "@type": "cidoc:E7_Activity",
            "cidoc:P14_carried_out_by": [
                {"@id": "ex:Guarantor_Marco", "@type": "cidoc:E21_Person"}
            ],
            "cidoc:P14.1_in_the_role_of": {
                "@id": "http://vocab.getty.edu/page/aat/300025614",
                "@type": "cidoc:E55_Type"
            },
            "cidoc:P17_was_motivated_by": {
                "@id": "ex:Buyer_Giovanni",
                "@type": "cidoc:E21_Person"
            }
        }]
    }]
    # Note: gmn:P70_7_documents_buyers_guarantor is removed
}

# Example 2: Multiple guarantors
example_2_input = {
    "@id": "ex:Contract_002",
    "gmn:P70_7_documents_buyers_guarantor": [
        {"@id": "ex:Guarantor_1"},
        {"@id": "ex:Guarantor_2"},
        {"@id": "ex:Guarantor_3"}
    ]
}

# OUTPUT: Creates three separate E7_Activity nodes, one for each guarantor


# ============================================================================
# TESTING CODE
# ============================================================================

# Automated test function:

def test_p70_7_transformation():
    """Test P70.7 buyer's guarantor transformation."""
    from gmn_to_cidoc_transform import transform_p70_7_documents_buyers_guarantor
    
    # Test case 1: Basic transformation
    input_data = {
        "@id": "http://example.org/contract/test001",
        "gmn:P70_7_documents_buyers_guarantor": [
            {"@id": "http://example.org/person/guarantor001"}
        ],
        "cidoc:P70_documents": [{
            "@id": "http://example.org/contract/test001/acquisition",
            "@type": "cidoc:E8_Acquisition",
            "cidoc:P22_transferred_title_to": [
                {"@id": "http://example.org/person/buyer001"}
            ]
        }]
    }
    
    result = transform_p70_7_documents_buyers_guarantor(input_data)
    
    # Assertions
    assert "gmn:P70_7_documents_buyers_guarantor" not in result, \
        "Shortcut property should be removed"
    
    acquisition = result["cidoc:P70_documents"][0]
    assert "cidoc:P9_consists_of" in acquisition, \
        "Should create P9_consists_of"
    
    activity = acquisition["cidoc:P9_consists_of"][0]
    assert activity["@type"] == "cidoc:E7_Activity", \
        "Should create E7_Activity"
    assert "cidoc:P14_carried_out_by" in activity, \
        "Should have P14_carried_out_by"
    assert "cidoc:P17_was_motivated_by" in activity, \
        "Should have P17_was_motivated_by"
    
    print("✓ All tests passed!")

# Run test:
# if __name__ == "__main__":
#     test_p70_7_transformation()


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Problem: Shortcut property not removed
# Solution: Verify 'del data[property_name]' is at end of transform function

# Problem: No E7_Activity created  
# Solution: Check that helper function exists and is called correctly

# Problem: P17_was_motivated_by missing
# Solution: Ensure buyer (P70.2) transforms before guarantor (P70.7)

# Problem: Wrong AAT URI
# Solution: Verify AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"

# Problem: Duplicate activities
# Solution: Check function only called once in transform_item()


# ============================================================================
# NOTES
# ============================================================================

# - This function reuses the generic transform_guarantor_property helper
# - The only difference from P70.6 is the motivated_by_property parameter:
#   * P70.6 (seller's guarantor): uses 'cidoc:P23_transferred_title_from'
#   * P70.7 (buyer's guarantor): uses 'cidoc:P22_transferred_title_to'
# - Activity URI generated using hash for uniqueness
# - Role specification uses Getty AAT concept for guarantor (300025614)
# - Handles both dict and string representations of guarantors
# - Gracefully handles missing buyer (creates activity without P17)
# - Supports multiple guarantors (each gets own E7_Activity)


# ============================================================================
# VERSION INFORMATION
# ============================================================================

# Function: transform_p70_7_documents_buyers_guarantor
# Property: gmn:P70_7_documents_buyers_guarantor
# Version: 1.0
# Created: 2025-10-17
# Dependencies: transform_guarantor_property, AAT_GUARANTOR constant
# Part of: P70 Sales Contract Properties (P70.1 - P70.17)
