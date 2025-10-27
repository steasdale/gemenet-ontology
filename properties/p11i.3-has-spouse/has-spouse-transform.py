# Python Additions for gmn_to_cidoc_transform.py
# Function: transform_p11i_3_has_spouse
# Add this function to the transformation script

# ============================================================================
# CONSTANT DEFINITIONS (Add to top of file, around line 20-30)
# ============================================================================

AAT_MARRIAGE = "http://vocab.getty.edu/aat/300055475"

# ============================================================================
# TRANSFORMATION FUNCTION (Add after transform_p11i_2_latest_attestation_date)
# ============================================================================

def transform_p11i_3_has_spouse(data):
    """
    Transform gmn:P11i_3_has_spouse to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event (marriage) > P11_had_participant > E21_Person
    
    This function transforms the simplified has spouse property into a complete
    CIDOC-CRM event-based structure. Each spouse relationship is represented as
    a marriage event (E5_Event) typed with AAT 300055475 (marriages), in which
    both the subject person and the spouse participated.
    
    Args:
        data: Dictionary representing a JSON-LD entity with potential spouse information
    
    Returns:
        Dictionary with transformed CIDOC-CRM compliant structure
    
    Examples:
        Input:
        {
            "@id": "person:alice",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_3_has_spouse": [
                {"@id": "person:bob", "@type": "cidoc:E21_Person"}
            ]
        }
        
        Output:
        {
            "@id": "person:alice",
            "@type": "cidoc:E21_Person",
            "cidoc:P11i_participated_in": [
                {
                    "@id": "person:alice/event/marriage_a1b2c3d4",
                    "@type": "cidoc:E5_Event",
                    "cidoc:P2_has_type": {
                        "@id": "http://vocab.getty.edu/aat/300055475",
                        "@type": "cidoc:E55_Type"
                    },
                    "cidoc:P11_had_participant": [
                        {"@id": "person:bob", "@type": "cidoc:E21_Person"}
                    ]
                }
            ]
        }
    """
    # Check if the property exists in the data
    if 'gmn:P11i_3_has_spouse' not in data:
        return data
    
    # Extract spouse list and subject URI
    spouses = data['gmn:P11i_3_has_spouse']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P11i_participated_in array if it doesn't exist
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    # Process each spouse
    for spouse_obj in spouses:
        # Handle both dictionary and string formats
        if isinstance(spouse_obj, dict):
            spouse_uri = spouse_obj.get('@id', '')
            spouse_data = spouse_obj.copy()
        else:
            spouse_uri = str(spouse_obj)
            spouse_data = {
                '@id': spouse_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique event URI using hash
        event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
        event_uri = f"{subject_uri}/event/marriage_{event_hash}"
        
        # Create marriage event structure
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P2_has_type': {
                '@id': AAT_MARRIAGE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P11_had_participant': [spouse_data]
        }
        
        # Add event to participation list
        data['cidoc:P11i_participated_in'].append(event)
    
    # Remove the simplified property
    del data['gmn:P11i_3_has_spouse']
    return data

# ============================================================================
# PIPELINE REGISTRATION (Add to transform_item function)
# ============================================================================
#
# Locate the transform_item() function (around line 700-900) and add this call
# in the "Person attestation and relationship properties" section:
#
#   def transform_item(item, include_internal=False):
#       """Transform a single JSON-LD item."""
#       
#       # ... existing transformations ...
#       
#       # Person attestation and relationship properties
#       item = transform_p11i_1_earliest_attestation_date(item)
#       item = transform_p11i_2_latest_attestation_date(item)
#       item = transform_p11i_3_has_spouse(item)  # <-- ADD THIS LINE
#       
#       # Property ownership and occupation
#       item = transform_p22_1_has_owner(item)
#       # ... rest of function ...
#
# ============================================================================
# IMPORTS REQUIRED
# ============================================================================
#
# Ensure these imports are at the top of the file:
#
# from uuid import uuid4
# import json
#
# ============================================================================
# TESTING
# ============================================================================
#
# Test the function with sample data:
#
# test_data = {
#     "@id": "person:test",
#     "@type": "cidoc:E21_Person",
#     "gmn:P11i_3_has_spouse": [
#         {"@id": "person:spouse1", "@type": "cidoc:E21_Person"}
#     ]
# }
#
# result = transform_p11i_3_has_spouse(test_data)
# print(json.dumps(result, indent=2))
#
# Expected output should include:
# - cidoc:P11i_participated_in array
# - E5_Event with type AAT 300055475
# - P11_had_participant with spouse data
# - Original gmn:P11i_3_has_spouse removed
#
# ============================================================================
# NOTES
# ============================================================================
#
# 1. The function handles both dictionary and string input formats
# 2. Each spouse creates a separate marriage event
# 3. Event URIs are deterministically generated using hash function
# 4. The hash ensures consistency: same spouse = same event URI
# 5. Multiple spouses are supported (sequential or concurrent marriages)
# 6. The function preserves existing P11i_participated_in events
# 7. Marriage events are automatically typed with AAT 300055475
#
# ============================================================================
# ERROR HANDLING
# ============================================================================
#
# The function handles:
# - Missing property (returns data unchanged)
# - Missing subject @id (generates UUID)
# - Dictionary spouse objects (extracts @id and copies data)
# - String spouse values (creates minimal E21_Person structure)
# - Multiple spouse values (processes each in loop)
# - Existing P11i_participated_in array (appends to it)
#
# ============================================================================
# PERFORMANCE CONSIDERATIONS
# ============================================================================
#
# - Time complexity: O(n) where n = number of spouses
# - Space complexity: O(n) for storing events
# - Hash computation: O(1) average case
# - No database queries or external calls
# - Suitable for batch processing large datasets
#
# ============================================================================
