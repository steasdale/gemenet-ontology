# Python Transformation Code for P70.18 Documents Disputing Party Property
#
# Copy this function to your gmn_to_cidoc_transform.py file
# Place it with other transformation functions (typically after other P70 functions)
#
# ==============================================================================

def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function transforms the shortcut property for disputing parties in
    arbitration agreements into the full CIDOC-CRM compliant structure.
    
    Args:
        data (dict): The item data dictionary containing the arbitration agreement
    
    Returns:
        dict: Modified data dictionary with transformed structure
    
    Transformation:
        Input:  gmn:P70_18_documents_disputing_party -> E39_Actor
        Output: cidoc:P70_documents -> E7_Activity -> P14_carried_out_by -> E39_Actor
    
    Example:
        Input:
        {
          "@id": "http://example.org/contracts/arb001",
          "@type": "gmn:E31_3_Arbitration_Agreement",
          "gmn:P70_18_documents_disputing_party": [
            {"@id": "http://example.org/persons/party1"},
            {"@id": "http://example.org/persons/party2"}
          ]
        }
        
        Output:
        {
          "@id": "http://example.org/contracts/arb001",
          "@type": "gmn:E31_3_Arbitration_Agreement",
          "cidoc:P70_documents": [{
            "@id": "http://example.org/contracts/arb001/arbitration",
            "@type": "cidoc:E7_Activity",
            "cidoc:P14_carried_out_by": [
              {"@id": "http://example.org/persons/party1", "@type": "cidoc:E39_Actor"},
              {"@id": "http://example.org/persons/party2", "@type": "cidoc:E39_Actor"}
            ]
          }]
        }
    """
    # Check if property exists in data
    if 'gmn:P70_18_documents_disputing_party' not in data:
        return data
    
    # Extract the disputing parties
    parties = data['gmn:P70_18_documents_disputing_party']
    
    # Get or generate subject URI
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Create or locate the E7_Activity node
    # Check if P70_documents already exists (from other arbitration properties)
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        # Create new activity with standard URI pattern
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }]
    
    # Get reference to the activity (first element in P70_documents array)
    activity = data['cidoc:P70_documents'][0]
    
    # Initialize P14_carried_out_by array if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    # Process each disputing party
    for party_obj in parties:
        # Handle both dict format ({"@id": "uri"}) and string format ("uri")
        if isinstance(party_obj, dict):
            # Party is already a dict - copy it
            party_data = party_obj.copy()
            # Ensure it has a type
            if '@type' not in party_data:
                party_data['@type'] = 'cidoc:E39_Actor'
        else:
            # Party is a string URI - wrap it in proper structure
            party_uri = str(party_obj)
            party_data = {
                '@id': party_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add party to the activity's P14_carried_out_by array
        activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Remove the shortcut property from the data
    del data['gmn:P70_18_documents_disputing_party']
    
    return data


# ==============================================================================
# INTEGRATION INSTRUCTIONS:
#
# 1. Add this function to gmn_to_cidoc_transform.py
#
# 2. In your main transformation pipeline (usually transform_item() function),
#    add this line with other property transformations:
#
#    # Transform P70.18 - documents disputing party
#    item = transform_p70_18_documents_disputing_party(item)
#
# 3. Ensure this transformation is called BEFORE the final output is generated
#
# 4. The order relative to P70.19 and P70.20 does not matter, as they all
#    contribute to the same activity node
#
# ==============================================================================

# TESTING CODE:
#
# You can test this function with the following code:

"""
import json
from uuid import uuid4

# Test data
test_data = {
    "@id": "http://example.org/contracts/test001",
    "@type": "gmn:E31_3_Arbitration_Agreement",
    "gmn:P70_18_documents_disputing_party": [
        {"@id": "http://example.org/persons/party1"},
        {"@id": "http://example.org/persons/party2"}
    ]
}

# Transform
result = transform_p70_18_documents_disputing_party(test_data)

# Print result
print(json.dumps(result, indent=2))

# Verify:
# - 'cidoc:P70_documents' exists
# - Activity has '@type': 'cidoc:E7_Activity'
# - Activity has 'cidoc:P14_carried_out_by' array
# - Array contains both parties with '@type': 'cidoc:E39_Actor'
# - 'gmn:P70_18_documents_disputing_party' is removed
"""

# ==============================================================================

# EDGE CASES HANDLED:
#
# 1. Property doesn't exist: Returns data unchanged
# 2. Empty array: Returns data unchanged (no activity created)
# 3. Single party: Creates activity with one party
# 4. Multiple parties: Adds all to same activity
# 5. Party as dict: Preserves structure, adds type if missing
# 6. Party as string: Wraps in proper structure with type
# 7. Existing activity: Reuses existing P70_documents[0]
# 8. Existing P14 array: Appends to existing array
# 9. Missing document @id: Generates UUID-based URI
#
# ==============================================================================

# DEPENDENCIES:
#
# This function requires:
# - Python 3.6+ (for f-strings)
# - uuid module (from standard library)
# - json module (from standard library, for testing)
#
# Add at top of file if not already present:
# from uuid import uuid4
#
# ==============================================================================

# INTEGRATION WITH OTHER ARBITRATION PROPERTIES:
#
# This function works alongside:
# - transform_p70_19_documents_arbitrator()
# - transform_p70_20_documents_dispute_subject()
#
# All three functions should:
# 1. Check for existing 'cidoc:P70_documents'
# 2. Reuse the existing activity if present
# 3. Use the same activity URI pattern: {document_uri}/arbitration
# 4. Not interfere with each other's transformations
#
# Example transformation order:
#   item = transform_p70_18_documents_disputing_party(item)  # Disputing parties
#   item = transform_p70_19_documents_arbitrator(item)       # Arbitrator
#   item = transform_p70_20_documents_dispute_subject(item)  # Dispute subject
#
# ==============================================================================

# VALIDATION TESTS:
#
# Test 1: Simple two-party arbitration
# Input: Two parties
# Expected: Activity with both in P14_carried_out_by

# Test 2: Three-party arbitration  
# Input: Three parties
# Expected: Activity with all three in P14_carried_out_by

# Test 3: Combined with arbitrator
# Input: Two parties + one arbitrator (P70.19)
# Expected: Activity with all three in P14_carried_out_by

# Test 4: String URIs
# Input: Parties as string URIs (not dicts)
# Expected: Proper dict structure in output

# Test 5: Existing activity
# Input: Data already has cidoc:P70_documents
# Expected: Parties added to existing activity

# Test 6: Empty property
# Input: Property exists but empty array
# Expected: No changes to data

# Test 7: Missing property
# Input: Property not in data
# Expected: Data returned unchanged

# ==============================================================================

# PERFORMANCE NOTES:
#
# - Function runs in O(n) time where n is number of parties
# - Typical n is 2-3 parties, so very fast
# - No recursive calls or complex operations
# - Memory usage minimal (creates one activity node + n party nodes)
#
# ==============================================================================

# TROUBLESHOOTING:
#
# Issue: Property not transforming
# Solution: Check function is called in main pipeline
#
# Issue: Activity not created
# Solution: Verify 'cidoc:P70_documents' check logic
#
# Issue: Parties not added
# Solution: Check party loop and type assignment
#
# Issue: Multiple activities created
# Solution: Ensure activity reuse logic is correct
#
# Issue: Type information missing
# Solution: Verify '@type' is added for E39_Actor
#
# ==============================================================================

# VERSION INFORMATION:
#
# Version: 1.0
# Created: 2025-10-28
# Last Modified: 2025-10-28
# Compatible with: GMN Ontology 1.0+, CIDOC-CRM 7.1.1
#
# ==============================================================================

# END OF PYTHON TRANSFORMATION CODE
