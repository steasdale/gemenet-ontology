# ============================================================================
# E31.6 CORRESPONDENCE - PYTHON ADDITIONS FOR gmn_to_cidoc_transform_script.py
# ============================================================================
# Version: 1.0
# Date: 2025-10-18
#
# INSTRUCTIONS:
# 1. Add the AAT_CORRESPONDENCE constant to the constants section
# 2. Add all six transformation functions after existing P70 functions
# 3. Add the six function calls to transform_item()
# 4. Update the module docstring
# ============================================================================

# ============================================================================
# SECTION 1: ADD CONSTANT
# ============================================================================
# Add this constant with the other AAT constants (around line 20-40)

AAT_CORRESPONDENCE = "http://vocab.getty.edu/page/aat/300026877"


# ============================================================================
# SECTION 2: TRANSFORMATION FUNCTIONS
# ============================================================================
# Add these six functions after existing P70 transformation functions

def transform_p70_26_indicates_sender(data):
    """
    Transform gmn:P70_26_indicates_sender to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_26_indicates_sender' not in data:
        return data
    
    senders = data['gmn:P70_26_indicates_sender']
    if not isinstance(senders, list):
        senders = [senders]
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if correspondence activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Look for existing correspondence activity
        for activity in data['cidoc:P70_documents']:
            if isinstance(activity, dict) and activity.get('@id', '').endswith('/correspondence'):
                existing_activity = activity
                break
    
    if existing_activity is None:
        # Create new correspondence activity
        activity_uri = f"{subject_uri}/correspondence"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }
        if 'cidoc:P70_documents' not in data:
            data['cidoc:P70_documents'] = []
        data['cidoc:P70_documents'].append(existing_activity)
    
    # Initialize P14_carried_out_by if not exists
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Add senders
    for sender_obj in senders:
        # Handle both URI references and full objects
        if isinstance(sender_obj, dict):
            sender_data = sender_obj.copy()
            if '@type' not in sender_data:
                sender_data['@type'] = 'cidoc:E39_Actor'
        else:
            sender_uri = str(sender_obj)
            sender_data = {
                '@id': sender_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to activity
        existing_activity['cidoc:P14_carried_out_by'].append(sender_data)
    
    # Remove shortcut property
    del data['gmn:P70_26_indicates_sender']
    
    return data


def transform_p70_27_has_address_of_origin(data):
    """
    Transform gmn:P70_27_has_address_of_origin to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P7_took_place_at > E53_Place
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_27_has_address_of_origin' not in data:
        return data
    
    origin_places = data['gmn:P70_27_has_address_of_origin']
    if not isinstance(origin_places, list):
        origin_places = [origin_places]
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if correspondence activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        for activity in data['cidoc:P70_documents']:
            if isinstance(activity, dict) and activity.get('@id', '').endswith('/correspondence'):
                existing_activity = activity
                break
    
    if existing_activity is None:
        # Create new correspondence activity
        activity_uri = f"{subject_uri}/correspondence"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }
        if 'cidoc:P70_documents' not in data:
            data['cidoc:P70_documents'] = []
        data['cidoc:P70_documents'].append(existing_activity)
    
    # Add origin places
    for place_obj in origin_places:
        # Handle both URI references and full objects
        if isinstance(place_obj, dict):
            place_data = place_obj.copy()
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        # Set P7_took_place_at (typically only one origin)
        existing_activity['cidoc:P7_took_place_at'] = place_data
    
    # Remove shortcut property
    del data['gmn:P70_27_has_address_of_origin']
    
    return data


def transform_p70_28_indicates_recipient(data):
    """
    Transform gmn:P70_28_indicates_recipient to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P01_has_domain > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_28_indicates_recipient' not in data:
        return data
    
    recipients = data['gmn:P70_28_indicates_recipient']
    if not isinstance(recipients, list):
        recipients = [recipients]
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if correspondence activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        for activity in data['cidoc:P70_documents']:
            if isinstance(activity, dict) and activity.get('@id', '').endswith('/correspondence'):
                existing_activity = activity
                break
    
    if existing_activity is None:
        # Create new correspondence activity
        activity_uri = f"{subject_uri}/correspondence"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }
        if 'cidoc:P70_documents' not in data:
            data['cidoc:P70_documents'] = []
        data['cidoc:P70_documents'].append(existing_activity)
    
    # Initialize P01_has_domain if not exists
    if 'cidoc:P01_has_domain' not in existing_activity:
        existing_activity['cidoc:P01_has_domain'] = []
    
    # Add recipients
    for recipient_obj in recipients:
        # Handle both URI references and full objects
        if isinstance(recipient_obj, dict):
            recipient_data = recipient_obj.copy()
            if '@type' not in recipient_data:
                recipient_data['@type'] = 'cidoc:E39_Actor'
        else:
            recipient_uri = str(recipient_obj)
            recipient_data = {
                '@id': recipient_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to activity
        existing_activity['cidoc:P01_has_domain'].append(recipient_data)
    
    # Remove shortcut property
    del data['gmn:P70_28_indicates_recipient']
    
    return data


def transform_p70_29_indicates_holder_of_item(data):
    """
    Transform gmn:P70_29_indicates_holder_of_item to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E7_Activity > P14_carried_out_by > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_29_indicates_holder_of_item' not in data:
        return data
    
    holders = data['gmn:P70_29_indicates_holder_of_item']
    if not isinstance(holders, list):
        holders = [holders]
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if correspondence activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        for activity in data['cidoc:P70_documents']:
            if isinstance(activity, dict) and activity.get('@id', '').endswith('/correspondence'):
                existing_activity = activity
                break
    
    if existing_activity is None:
        # Create new correspondence activity
        activity_uri = f"{subject_uri}/correspondence"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }
        if 'cidoc:P70_documents' not in data:
            data['cidoc:P70_documents'] = []
        data['cidoc:P70_documents'].append(existing_activity)
    
    # Initialize P16_used_specific_object if not exists
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Create holding activities for each holder
    for idx, holder_obj in enumerate(holders):
        # Create holding activity
        holding_activity_uri = f"{subject_uri}/holding_activity_{idx}"
        holding_activity = {
            '@id': holding_activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': 'http://vocab.getty.edu/page/aat/300077993',  # AAT: holding
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Handle both URI references and full objects
        if isinstance(holder_obj, dict):
            holder_data = holder_obj.copy()
            if '@type' not in holder_data:
                holder_data['@type'] = 'cidoc:E39_Actor'
        else:
            holder_uri = str(holder_obj)
            holder_data = {
                '@id': holder_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        holding_activity['cidoc:P14_carried_out_by'] = holder_data
        
        # Add holding activity to correspondence activity
        existing_activity['cidoc:P16_used_specific_object'].append(holding_activity)
    
    # Remove shortcut property
    del data['gmn:P70_29_indicates_holder_of_item']
    
    return data


def transform_p70_30_refers_to_described_event(data):
    """
    Transform gmn:P70_30_refers_to_described_event to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E5_Event
    
    Note: This property has domain E31_Document, so it can be used with any document type.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_30_refers_to_described_event' not in data:
        return data
    
    events = data['gmn:P70_30_refers_to_described_event']
    if not isinstance(events, list):
        events = [events]
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if an activity already exists (could be correspondence, declaration, etc.)
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use the first activity found
        for item in data['cidoc:P70_documents']:
            if isinstance(item, dict) and item.get('@type') == 'cidoc:E7_Activity':
                existing_activity = item
                break
    
    if existing_activity is None:
        # Create new activity (type depends on document class)
        # For correspondence, use correspondence activity
        activity_uri = f"{subject_uri}/activity"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }
        if 'cidoc:P70_documents' not in data:
            data['cidoc:P70_documents'] = []
        data['cidoc:P70_documents'].append(existing_activity)
    
    # Initialize P16_used_specific_object if not exists
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Add described events
    for event_obj in events:
        # Handle both URI references and full objects
        if isinstance(event_obj, dict):
            event_data = event_obj.copy()
            if '@type' not in event_data:
                event_data['@type'] = 'cidoc:E5_Event'
        else:
            event_uri = str(event_obj)
            event_data = {
                '@id': event_uri,
                '@type': 'cidoc:E5_Event'
            }
        
        # Add to activity
        existing_activity['cidoc:P16_used_specific_object'].append(event_data)
    
    # Remove shortcut property
    del data['gmn:P70_30_refers_to_described_event']
    
    return data


def transform_p70_31_has_address_of_destination(data):
    """
    Transform gmn:P70_31_has_address_of_destination to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P26_moved_to > E53_Place
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_31_has_address_of_destination' not in data:
        return data
    
    destination_places = data['gmn:P70_31_has_address_of_destination']
    if not isinstance(destination_places, list):
        destination_places = [destination_places]
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if correspondence activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        for activity in data['cidoc:P70_documents']:
            if isinstance(activity, dict) and activity.get('@id', '').endswith('/correspondence'):
                existing_activity = activity
                break
    
    if existing_activity is None:
        # Create new correspondence activity
        activity_uri = f"{subject_uri}/correspondence"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }
        if 'cidoc:P70_documents' not in data:
            data['cidoc:P70_documents'] = []
        data['cidoc:P70_documents'].append(existing_activity)
    
    # Add destination places
    for place_obj in destination_places:
        # Handle both URI references and full objects
        if isinstance(place_obj, dict):
            place_data = place_obj.copy()
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        # Set P26_moved_to (typically only one destination)
        existing_activity['cidoc:P26_moved_to'] = place_data
    
    # Remove shortcut property
    del data['gmn:P70_31_has_address_of_destination']
    
    return data


# ============================================================================
# SECTION 3: UPDATE transform_item() FUNCTION
# ============================================================================
# Add these calls to the transform_item() function, recommended location is
# after declaration properties and before donation properties

def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # ... existing transformations ...
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    item = transform_p70_27_has_address_of_origin(item)
    item = transform_p70_28_indicates_recipient(item)
    item = transform_p70_29_indicates_holder_of_item(item)
    item = transform_p70_30_refers_to_described_event(item)
    item = transform_p70_31_has_address_of_destination(item)
    
    # ... rest of transformations ...
    
    return item


# ============================================================================
# SECTION 4: UPDATE MODULE DOCSTRING
# ============================================================================
# Update the module docstring at the top of the file to include E31.6:

"""
Transform GMN shortcut properties to full CIDOC-CRM compliant structure.

This script reads JSON-LD export from Omeka-S and transforms custom shortcut
properties (like gmn:P1_1_has_name) into their full CIDOC-CRM equivalents.

Updated to reflect expanded class hierarchy including:
- gmn:E31_1_Contract (general contract class)
- gmn:E31_2_Sales_Contract (specialized sales contract)
- gmn:E31_3_Arbitration_Agreement
- gmn:E31_4_Cession_of_Rights_Contract
- gmn:E31_5_Declaration
- gmn:E31_6_Correspondence
- gmn:E31_7_Donation_Contract
"""

# ============================================================================
# END OF PYTHON ADDITIONS
# ============================================================================