#!/usr/bin/env python3
"""
Arbitration Agreement Transformation Functions
Version: 1.0
Date: 2025-10-26

This file contains the Python code to add to gmn_to_cidoc_transform_script.py
for transforming arbitration agreement shortcut properties to CIDOC-CRM.
"""

# ============================================================================
# SECTION 1: CONSTANT ADDITION
# Location: Add to constants section (after AAT_WITNESS, before functions)
# Action: ADD this constant
# ============================================================================

# Getty AAT URI for arbitration (process)
AAT_ARBITRATION = "http://vocab.getty.edu/page/aat/300417271"


# ============================================================================
# SECTION 2: TRANSFORMATION FUNCTIONS
# Location: Add after sales contract functions, before transform_item()
# Action: ADD these three complete functions
# ============================================================================

def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_18_documents_disputing_party' not in data:
        return data
    
    parties = data['gmn:P70_18_documents_disputing_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if arbitration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new arbitration activity
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Add disputing parties
    for party_obj in parties:
        # Handle both URI references and full objects
        if isinstance(party_obj, dict):
            party_data = party_obj.copy()
            if '@type' not in party_data:
                party_data['@type'] = 'cidoc:E39_Actor'
        else:
            party_uri = str(party_obj)
            party_data = {
                '@id': party_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to arbitration activity
        existing_activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Remove shortcut property
    del data['gmn:P70_18_documents_disputing_party']
    
    return data


def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if arbitration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new arbitration activity
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Add arbitrators
    for arbitrator_obj in arbitrators:
        # Handle both URI references and full objects
        if isinstance(arbitrator_obj, dict):
            arbitrator_data = arbitrator_obj.copy()
            if '@type' not in arbitrator_data:
                arbitrator_data['@type'] = 'cidoc:E39_Actor'
        else:
            arbitrator_uri = str(arbitrator_obj)
            arbitrator_data = {
                '@id': arbitrator_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to arbitration activity
        existing_activity['cidoc:P14_carried_out_by'].append(arbitrator_data)
    
    # Remove shortcut property
    del data['gmn:P70_19_documents_arbitrator']
    
    return data


def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    subjects = data['gmn:P70_20_documents_dispute_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if arbitration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new arbitration activity
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P16 if it doesn't exist
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Add dispute subjects
    for subject_obj in subjects:
        # Handle both URI references and full objects
        if isinstance(subject_obj, dict):
            subject_data = subject_obj.copy()
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            subject_uri_ref = str(subject_obj)
            subject_data = {
                '@id': subject_uri_ref,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add to arbitration activity
        existing_activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Remove shortcut property
    del data['gmn:P70_20_documents_dispute_subject']
    
    return data


# ============================================================================
# SECTION 3: FUNCTION CALL ADDITIONS
# Location: Inside transform_item() function, in arbitration section
# Action: ADD these three function calls
# ============================================================================

# Add these lines to transform_item() function:
# (Insert after sales contract properties, before return statement)

def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    """
    # ... existing transformations for names, dates, etc. ...
    
    # Sales contract properties
    # ... existing sales contract transformations ...
    
    # Arbitration agreement properties
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    
    return item


# ============================================================================
# INTEGRATION NOTES
# ============================================================================

"""
INTEGRATION STEPS:

1. ADD AAT_ARBITRATION CONSTANT (Section 1)
   - Location: In constants section after AAT_WITNESS
   - This must be added BEFORE the transformation functions

2. ADD THREE TRANSFORMATION FUNCTIONS (Section 2)
   - Location: After sales contract functions, before transform_item()
   - Copy all three functions exactly as written
   - Maintain proper indentation (4 spaces)

3. ADD FUNCTION CALLS (Section 3)
   - Location: Inside transform_item() function
   - Add after sales contract property transformations
   - Add before the final "return item" statement
   - These three lines call the functions defined in Section 2

4. VERIFY IMPORTS
   - Ensure "from uuid import uuid4" is at top of file
   - No additional imports are required

5. TEST
   - Run: python3 -m py_compile gmn_to_cidoc_transform_script.py
   - Should compile without errors
   - Test with sample arbitration agreement JSON

NOTES:
- All three functions share the same E7_Activity node pattern
- Order of function calls doesn't matter (they detect existing activity)
- Functions handle both URI references and full object representations
- Activity URI pattern: {contract_uri}/arbitration

RELATED FILES:
- arbitration-agreement-ontology.ttl: TTL additions for RDF ontology
- arbitration-agreement-documentation.md: Complete semantic docs
- arbitration-agreement-implementation-guide.md: Step-by-step guide
"""
