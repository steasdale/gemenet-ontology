# GMN P70.19 Documents Arbitrator - Python Transformation Function
# Ready-to-copy Python code for addition to gmn_to_cidoc_transform.py

# ==============================================================================
# REQUIRED IMPORTS
# ==============================================================================

# Ensure these imports exist at the top of your transformation script:
# from uuid import uuid4
# import json

# ==============================================================================
# REQUIRED CONSTANTS
# ==============================================================================

# Ensure this constant is defined (typically near the top of the file):
AAT_ARBITRATION = 'http://vocab.getty.edu/page/aat/300417271'

# ==============================================================================
# TRANSFORMATION FUNCTION
# ==============================================================================

def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function handles arbitrators appointed to resolve disputes in
    arbitration agreements. Arbitrators are modeled as active principals
    who carry out the arbitration process alongside the disputing parties.
    
    The function follows the shared activity pattern used by all arbitration
    properties (P70.18, P70.19, P70.20), ensuring they contribute to a
    single E7_Activity representing the arbitration.
    
    Transformation Process:
    1. Check if the property exists in the data
    2. Locate or create the shared E7_Activity node
    3. Add arbitrators to P14_carried_out_by array
    4. Remove the shortcut property from the document
    
    Args:
        data: Dictionary containing the document data in JSON-LD format.
              Expected to have gmn:P70_19_documents_arbitrator property.
        
    Returns:
        dict: Modified data dictionary with CIDOC-CRM compliant structure.
              The shortcut property is removed and the activity structure
              is created/enhanced.
    
    Example Input:
        {
          "@id": "http://example.org/contracts/arb001",
          "@type": "gmn:E31_3_Arbitration_Agreement",
          "gmn:P70_19_documents_arbitrator": [
            {"@id": "http://example.org/persons/arbitrator_1"}
          ]
        }
    
    Example Output:
        {
          "@id": "http://example.org/contracts/arb001",
          "@type": "gmn:E31_3_Arbitration_Agreement",
          "cidoc:P70_documents": [{
            "@id": "http://example.org/contracts/arb001/arbitration",
            "@type": "cidoc:E7_Activity",
            "cidoc:P2_has_type": {
              "@id": "http://vocab.getty.edu/page/aat/300417271",
              "@type": "cidoc:E55_Type"
            },
            "cidoc:P14_carried_out_by": [
              {
                "@id": "http://example.org/persons/arbitrator_1",
                "@type": "cidoc:E39_Actor"
              }
            ]
          }]
        }
    
    Notes:
        - Supports multiple arbitrators (arbitration panels)
        - Coordinates with P70.18 and P70.20 to share a single E7_Activity
        - Creates activity with AAT 300417271 typing if none exists
        - Handles both object and string URI formats for arbitrators
        - Safe to call even if property doesn't exist in data
    """
    # Step 1: Check if the property exists in the data
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    # Step 2: Get arbitrator value(s) and normalize to list
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    if not isinstance(arbitrators, list):
        arbitrators = [arbitrators]
    
    # Step 3: Get document URI for creating activity URI if needed
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 4: Find existing E7_Activity or create new one
    # This implements the shared activity pattern - all arbitration properties
    # contribute to the same E7_Activity instance
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # No activity exists yet, create a new one
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,  # AAT 300417271
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    # Step 5: Get reference to the activity (always use first element)
    activity = data['cidoc:P70_documents'][0]
    
    # Step 6: Ensure P14_carried_out_by array exists in the activity
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Step 7: Process each arbitrator and add to P14_carried_out_by
    for arbitrator_obj in arbitrators:
        # Handle both dictionary objects and plain URI strings
        if isinstance(arbitrator_obj, dict):
            # Already a structured object, copy it
            arbitrator_data = arbitrator_obj.copy()
            # Ensure it has a type
            if '@type' not in arbitrator_data:
                arbitrator_data['@type'] = 'cidoc:E39_Actor'
        else:
            # Plain URI string, create structure
            arbitrator_uri = str(arbitrator_obj)
            arbitrator_data = {
                '@id': arbitrator_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add arbitrator to the activity
        activity['cidoc:P14_carried_out_by'].append(arbitrator_data)
    
    # Step 8: Remove the shortcut property from the document
    # This is required for CIDOC-CRM compliance
    del data['gmn:P70_19_documents_arbitrator']
    
    # Step 9: Return modified data
    return data


# ==============================================================================
# INTEGRATION INTO TRANSFORMATION PIPELINE
# ==============================================================================

# Add this function call to the main transformation pipeline.
# Place it between P70.18 and P70.20 calls for logical grouping:

# def transform_gmn_to_cidoc(data):
#     """Main transformation pipeline"""
#     
#     # ... existing transformations ...
#     
#     # Arbitration agreement properties
#     data = transform_p70_18_documents_disputing_party(data)
#     data = transform_p70_19_documents_arbitrator(data)        # <-- ADD HERE
#     data = transform_p70_20_documents_dispute_subject(data)
#     
#     # ... more transformations ...
#     
#     return data

# ==============================================================================
# TESTING CODE
# ==============================================================================

# Use this code to test the function in isolation:

def test_transform_p70_19():
    """Test function for P70.19 transformation"""
    
    # Test Case 1: Single arbitrator
    test_data_1 = {
        "@id": "http://example.org/contracts/arb001",
        "@type": "gmn:E31_3_Arbitration_Agreement",
        "gmn:P70_19_documents_arbitrator": [
            {"@id": "http://example.org/persons/arbitrator_1"}
        ]
    }
    
    result_1 = transform_p70_19_documents_arbitrator(test_data_1)
    print("Test 1 - Single arbitrator:")
    print(json.dumps(result_1, indent=2))
    print()
    
    # Test Case 2: Multiple arbitrators (panel)
    test_data_2 = {
        "@id": "http://example.org/contracts/arb002",
        "@type": "gmn:E31_3_Arbitration_Agreement",
        "gmn:P70_19_documents_arbitrator": [
            {"@id": "http://example.org/persons/arbitrator_1"},
            {"@id": "http://example.org/persons/arbitrator_2"},
            {"@id": "http://example.org/persons/arbitrator_3"}
        ]
    }
    
    result_2 = transform_p70_19_documents_arbitrator(test_data_2)
    print("Test 2 - Multiple arbitrators:")
    print(json.dumps(result_2, indent=2))
    print()
    
    # Test Case 3: Activity pre-exists from P70.18
    test_data_3 = {
        "@id": "http://example.org/contracts/arb003",
        "@type": "gmn:E31_3_Arbitration_Agreement",
        "cidoc:P70_documents": [{
            "@id": "http://example.org/contracts/arb003/arbitration",
            "@type": "cidoc:E7_Activity",
            "cidoc:P14_carried_out_by": [
                {"@id": "http://example.org/persons/party_1", "@type": "cidoc:E39_Actor"},
                {"@id": "http://example.org/persons/party_2", "@type": "cidoc:E39_Actor"}
            ]
        }],
        "gmn:P70_19_documents_arbitrator": [
            {"@id": "http://example.org/persons/arbitrator_1"}
        ]
    }
    
    result_3 = transform_p70_19_documents_arbitrator(test_data_3)
    print("Test 3 - Activity pre-exists:")
    print(json.dumps(result_3, indent=2))
    print()
    
    # Test Case 4: String URI instead of object
    test_data_4 = {
        "@id": "http://example.org/contracts/arb004",
        "@type": "gmn:E31_3_Arbitration_Agreement",
        "gmn:P70_19_documents_arbitrator": "http://example.org/persons/arbitrator_1"
    }
    
    result_4 = transform_p70_19_documents_arbitrator(test_data_4)
    print("Test 4 - String URI:")
    print(json.dumps(result_4, indent=2))
    print()
    
    # Test Case 5: Property doesn't exist (should return unchanged)
    test_data_5 = {
        "@id": "http://example.org/contracts/arb005",
        "@type": "gmn:E31_3_Arbitration_Agreement"
    }
    
    result_5 = transform_p70_19_documents_arbitrator(test_data_5)
    print("Test 5 - No property:")
    print(json.dumps(result_5, indent=2))
    print()

# Uncomment to run tests:
# if __name__ == "__main__":
#     test_transform_p70_19()

# ==============================================================================
# VALIDATION CHECKLIST
# ==============================================================================

# After adding this function, verify:
# ✓ Function is defined in the script
# ✓ Function is called in the main pipeline
# ✓ AAT_ARBITRATION constant is defined
# ✓ Required imports (uuid4) are present
# ✓ Function handles list and single values
# ✓ Function creates activity if needed
# ✓ Function reuses existing activity
# ✓ Function adds to P14_carried_out_by correctly
# ✓ Function removes GMN property
# ✓ Function returns modified data
# ✓ Test cases pass successfully
# ✓ Integration with P70.18 and P70.20 works

# ==============================================================================
# NOTES
# ==============================================================================

# Shared Activity Pattern:
# - All three arbitration properties (P70.18, P70.19, P70.20) share one activity
# - Each function checks for existing cidoc:P70_documents
# - Each function reuses the first element if it exists
# - Each function creates activity only if none exists
# - This ensures semantic unity: one arbitration = one activity

# Actor Typing:
# - All arbitrators are typed as cidoc:E39_Actor
# - E39_Actor can be persons (E21_Person) or groups (E74_Group)
# - Both are valid arbitrators in the medieval context

# Multiple Arbitrators:
# - Fully supported through list processing
# - Each arbitrator added individually to P14_carried_out_by
# - No limit on panel size
# - Typical panels: 1 (single), 3 (majority decision), or 5+ (large disputes)

# ==============================================================================
# VERSION INFORMATION
# ==============================================================================

# Version: 1.0
# Date: 2025-10-17
# Last Modified: 2025-10-18
# Compatibility: Python 3.6+, GMN Transform Script v1.0+

# ==============================================================================
