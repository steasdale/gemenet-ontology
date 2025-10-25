#!/usr/bin/env python3
"""
Donation Contract Transformation Functions
Add these functions to gmn_to_cidoc_transform.py
"""

# ============================================================
# SNIPPET 1: Add these functions after correspondence transformations
# (around line 1800)
# ============================================================

def transform_p70_32_indicates_donor(data):
    """
    Transform gmn:P70_32_indicates_donor to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor
    """
    if 'gmn:P70_32_indicates_donor' not in data:
        return data
    
    donors = data['gmn:P70_32_indicates_donor']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P23_transferred_title_from' not in acquisition:
        acquisition['cidoc:P23_transferred_title_from'] = []
    
    for donor_obj in donors:
        if isinstance(donor_obj, dict):
            donor_data = donor_obj.copy()
            if '@type' not in donor_data:
                donor_data['@type'] = 'cidoc:E39_Actor'
        else:
            donor_uri = str(donor_obj)
            donor_data = {
                '@id': donor_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        acquisition['cidoc:P23_transferred_title_from'].append(donor_data)
    
    del data['gmn:P70_32_indicates_donor']
    return data


def transform_p70_33_indicates_object_of_donation(data):
    """
    Transform gmn:P70_33_indicates_object_of_donation to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_33_indicates_object_of_donation' not in data:
        return data
    
    objects = data['gmn:P70_33_indicates_object_of_donation']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P24_transferred_title_of' not in acquisition:
        acquisition['cidoc:P24_transferred_title_of'] = []
    
    for obj_obj in objects:
        if isinstance(obj_obj, dict):
            obj_data = obj_obj.copy()
            if '@type' not in obj_data:
                obj_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            obj_uri = str(obj_obj)
            obj_data = {
                '@id': obj_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        acquisition['cidoc:P24_transferred_title_of'].append(obj_data)
    
    del data['gmn:P70_33_indicates_object_of_donation']
    return data


# ============================================================
# SNIPPET 2: UPDATE transform_p70_22_indicates_receiving_party function
# Add the donation handling section to the existing function
# ============================================================

def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    For cessions: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    For declarations: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    For donations: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    """
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    item_type = data.get('@type', '')
    
    # Determine document type
    is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_4_Cession_of_Rights_Contract'
    is_declaration = 'gmn:E31_5_Declaration' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_5_Declaration'
    is_donation = 'gmn:E31_7_Donation_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_7_Donation_Contract'
    
    if is_donation:
        # For donations, use E8_Acquisition
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            acquisition_uri = f"{subject_uri}/acquisition"
            data['cidoc:P70_documents'] = [{
                '@id': acquisition_uri,
                '@type': 'cidoc:E8_Acquisition'
            }]
        
        acquisition = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P22_transferred_title_to' not in acquisition:
            acquisition['cidoc:P22_transferred_title_to'] = []
        
        for party_obj in receiving_parties:
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
            
            acquisition['cidoc:P22_transferred_title_to'].append(party_data)
    
    elif is_declaration:
        # For declarations, use P01_has_domain
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/declaration"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': AAT_DECLARATION,
                    '@type': 'cidoc:E55_Type'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P01_has_domain' not in activity:
            activity['cidoc:P01_has_domain'] = []
        
        for party_obj in receiving_parties:
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
            
            activity['cidoc:P01_has_domain'].append(party_data)
    
    elif is_cession:
        # For cessions, use P14_carried_out_by
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/cession"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': AAT_TRANSFER_OF_RIGHTS,
                    '@type': 'cidoc:E55_Type'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P14_carried_out_by' not in activity:
            activity['cidoc:P14_carried_out_by'] = []
        
        for party_obj in receiving_parties:
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
            
            activity['cidoc:P14_carried_out_by'].append(party_data)
    
    del data['gmn:P70_22_indicates_receiving_party']
    return data


# ============================================================
# SNIPPET 3: UPDATE transform_item function
# Add these two lines after correspondence transformations (around line 2200)
# ============================================================

def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing transformations ...
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    item = transform_p70_27_has_address_of_origin(item)
    item = transform_p70_28_indicates_addressee(item)
    item = transform_p70_29_describes_subject(item)
    item = transform_p70_30_mentions_person(item)
    item = transform_p70_31_has_address_of_destination(item)
    
    # Donation properties (P70.32-P70.33)  <-- ADD THESE TWO LINES
    item = transform_p70_32_indicates_donor(item)
    item = transform_p70_33_indicates_object_of_donation(item)
    
    # ... rest of transformations ...
    return item


# ============================================================
# SNIPPET 4: UPDATE main function help text
# Add E31_7_Donation_Contract to the supported contract types list
# ============================================================

def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python gmn_to_cidoc_transform_script.py <input_file.json> <output_file.json> [--include-internal]")
        print("\nOptions:")
        print("  --include-internal    Include editorial notes in output (default: exclude)")
        print("\nExamples:")
        print("  python gmn_to_cidoc_transform_script.py omeka_export.json public_output.json")
        print("  python gmn_to_cidoc_transform_script.py omeka_export.json full_output.json --include-internal")
        print("\nSupported contract types:")
        print("  - gmn:E31_1_Contract (general contracts)")
        print("  - gmn:E31_2_Sales_Contract")
        print("  - gmn:E31_4_Cession_of_Rights_Contract")
        print("  - gmn:E31_5_Declaration")
        print("  - gmn:E31_6_Correspondence")
        print("  - gmn:E31_7_Donation_Contract")  # <-- ADD THIS LINE
        sys.exit(1)
    
    # ... rest of main function ...


# ============================================================
# IMPLEMENTATION CHECKLIST
# ============================================================
# □ Add transform_p70_32_indicates_donor() function
# □ Add transform_p70_33_indicates_object_of_donation() function
# □ Update transform_p70_22_indicates_receiving_party() function
# □ Update transform_item() function (add 2 lines)
# □ Update main() help text (add 1 line)
# □ Test with sample donation contract data
# □ Verify CIDOC-CRM compliance of output
