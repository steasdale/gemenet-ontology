# Python Transformation Code for gmn:P70_4_documents_sellers_procurator
# Ready to copy into gmn_to_cidoc_transform.py
#
# INSTRUCTIONS:
# 1. Open gmn_to_cidoc_transform.py
# 2. Verify the helper function transform_procurator_property() exists (lines ~483-549)
# 3. Locate transform_p70_3_documents_transfer_of() function (around line 450)
# 4. Insert the content below AFTER transform_p70_3_documents_transfer_of()
# 5. Update the transform_item() function to call this transformation
# 6. Ensure AAT_AGENT constant exists at top of file (line 29)

# ===========================================================================
# STEP 1: VERIFY HELPER FUNCTION EXISTS
# ===========================================================================
# The following function should already exist in your transformation script.
# If it doesn't exist, you need to add it first (see NOTE below).

"""
def transform_procurator_property(data, property_name, motivated_by_property):
    '''
    Generic function to transform procurator properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    '''
    if property_name not in data:
        return data
    
    procurators = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
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
    
    for procurator_obj in procurators:
        if isinstance(procurator_obj, dict):
            procurator_uri = procurator_obj.get('@id', '')
            procurator_data = procurator_obj.copy()
        else:
            procurator_uri = str(procurator_obj)
            procurator_data = {
                '@id': procurator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(procurator_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/procurator_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [procurator_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_AGENT,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data[property_name]
    return data
"""

# NOTE: If the helper function doesn't exist, add it before the specific
# transformation function. It's used by both P70.4 and P70.5.

# ===========================================================================
# STEP 2: ADD SPECIFIC TRANSFORMATION FUNCTION
# ===========================================================================
# COPY FROM HERE (insert after transform_p70_3_documents_transfer_of)
# ===========================================================================


def transform_p70_4_documents_sellers_procurator(data):
    """Transform gmn:P70_4_documents_sellers_procurator to full CIDOC-CRM structure."""
    return transform_procurator_property(data, 'gmn:P70_4_documents_sellers_procurator', 
                                        'cidoc:P23_transferred_title_from')


# ===========================================================================
# COPY TO HERE
# ===========================================================================

# ===========================================================================
# STEP 3: UPDATE transform_item() FUNCTION
# ===========================================================================
# In the transform_item() function, add the following line in the
# "Sales contract properties (P70.1-P70.17)" section, after P70.3:

"""
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)  # <-- ADD THIS LINE
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    # ... rest of transformations
"""

# CRITICAL: The order matters! P70.4 must come after P70.1 (seller) to
# ensure the seller URI is available for the P17_was_motivated_by linkage.

# ===========================================================================
# STEP 4: VERIFY CONSTANTS
# ===========================================================================
# Ensure the following constant exists at the top of the file (around line 29):

"""
AAT_AGENT = "http://vocab.getty.edu/page/aat/300025972"
"""

# ===========================================================================
# FUNCTION DOCUMENTATION
# ===========================================================================

"""
Function: transform_p70_4_documents_sellers_procurator(data)

Purpose:
    Transforms the GMN shortcut property P70_4_documents_sellers_procurator
    into full CIDOC-CRM compliant structure by delegating to the generic
    transform_procurator_property() helper function.

Parameters:
    data (dict): JSON-LD data dictionary containing the contract information
                 Must include '@id' and may include the P70.4 property

Returns:
    dict: Transformed data with P70.4 expanded to CIDOC-CRM structure
          and original shortcut property removed

Transformation Path:
    gmn:P70_4_documents_sellers_procurator
        ↓
    cidoc:P70_documents → E8_Acquisition
        └─ cidoc:P9_consists_of → E7_Activity
            ├─ cidoc:P14_carried_out_by → E21_Person (procurator)
            ├─ cidoc:P14.1_in_the_role_of → E55_Type (AAT:agent)
            └─ cidoc:P17_was_motivated_by → E21_Person (seller)

Dependencies:
    - transform_procurator_property(): Generic helper function
    - AAT_AGENT: Constant for Getty AAT agent term
    - transform_p70_1_documents_seller(): Must be called first for P17 linkage

Usage Example:
    Input:
    {
        "@id": "contract/001",
        "gmn:P70_1_documents_seller": [{"@id": "person/seller"}],
        "gmn:P70_4_documents_sellers_procurator": [{"@id": "person/procurator"}]
    }

    Output:
    {
        "@id": "contract/001",
        "cidoc:P70_documents": [{
            "@id": "contract/001/acquisition",
            "@type": "cidoc:E8_Acquisition",
            "cidoc:P23_transferred_title_from": [{"@id": "person/seller", ...}],
            "cidoc:P9_consists_of": [{
                "@id": "contract/001/activity/procurator_abc12345",
                "@type": "cidoc:E7_Activity",
                "cidoc:P14_carried_out_by": [{"@id": "person/procurator", ...}],
                "cidoc:P14.1_in_the_role_of": {"@id": "http://vocab.getty.edu/...", ...},
                "cidoc:P17_was_motivated_by": {"@id": "person/seller", ...}
            }]
        }]
    }

Notes:
    - Handles multiple procurators by creating separate E7_Activity nodes
    - Generates unique URIs using hash of procurator URI + property name
    - Gracefully handles missing seller (no P17 link in that case)
    - Automatically removes original gmn:P70_4 property after transformation
    - Uses AAT "agent" concept to explicitly qualify the procurator role

Related Functions:
    - transform_p70_5_documents_buyers_procurator(): Parallel for buyer's procurator
    - transform_p70_6_documents_sellers_guarantor(): Similar but different role
    - transform_procurator_property(): Generic helper for both procurator types

Error Handling:
    - Returns data unchanged if P70.4 property not present
    - Creates acquisition structure if not already present
    - Handles both dict and string formats for procurator objects
    - Ensures P9_consists_of array exists before appending

Testing:
    Run unit test with:
        python3 -m pytest test_transform_p70_4.py

    Or manual test:
        python3 gmn_to_cidoc_transform.py test_input.json test_output.json

    Verify output contains:
        - E7_Activity with correct structure
        - P14_carried_out_by linking to procurator
        - P14.1_in_the_role_of with AAT:agent
        - P17_was_motivated_by linking to seller (if seller defined)
        - Original gmn:P70_4 property removed
"""

# ===========================================================================
# TESTING CODE (Optional - for development/debugging)
# ===========================================================================

# Uncomment and run this section to test the transformation independently:

"""
if __name__ == "__main__":
    # Test data
    test_data = {
        "@id": "contract/test_001",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_1_documents_seller": [{
            "@id": "person/seller_001",
            "@type": "cidoc:E21_Person"
        }],
        "gmn:P70_4_documents_sellers_procurator": [{
            "@id": "person/procurator_001",
            "@type": "cidoc:E21_Person"
        }]
    }
    
    # Transform seller first (dependency)
    test_data = transform_p70_1_documents_seller(test_data)
    
    # Transform procurator
    result = transform_p70_4_documents_sellers_procurator(test_data)
    
    # Print result
    import json
    print(json.dumps(result, indent=2))
    
    # Validate structure
    assert 'cidoc:P70_documents' in result
    assert 'cidoc:P9_consists_of' in result['cidoc:P70_documents'][0]
    assert 'gmn:P70_4_documents_sellers_procurator' not in result
    print("✓ All assertions passed")
"""

# ===========================================================================
# INTEGRATION CHECKLIST
# ===========================================================================
"""
After adding this code:

[ ] Verify helper function transform_procurator_property() exists
[ ] Verify AAT_AGENT constant exists at top of file
[ ] Add transform_p70_4_documents_sellers_procurator() function
[ ] Update transform_item() to call the new function
[ ] Ensure call happens after transform_p70_1_documents_seller()
[ ] Test with sample data
[ ] Verify output structure matches CIDOC-CRM spec
[ ] Check that original property is removed
[ ] Validate P17_was_motivated_by links to seller
[ ] Test edge case: procurator without seller
[ ] Test edge case: multiple procurators
[ ] Run full test suite
[ ] Update documentation
"""

# ===========================================================================
# VERSION INFORMATION
# ===========================================================================
# Function created: 2025-10-17
# File version: 1.0
# Last updated: October 2025
# Compatible with: gmn_to_cidoc_transform.py v2.0+
# Python version: 3.8+
# Dependencies: uuid.uuid4, json (standard library)
