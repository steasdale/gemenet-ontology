            # Preserve existing type or default to E18_Physical_Thing
            if '@type' not in object_data:
                object_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            object_uri = str(object_obj)
            object_data = {
                '@id': object_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        # Add to acquisition event
        existing_acquisition['cidoc:P24_transferred_title_of'].append(object_data)
    
    # Remove shortcut property
    del data['gmn:P70_3_documents_transfer_of']
    
    return data

def transform_p70_4_documents_sellers_procurator(data):
    """
    Transform gmn:P70_4_documents_sellers_procurator to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person
    with P17_was_motivated_by linking to the seller
    
    Also adds gmn:is_represented_by property from seller to procurator.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_4_documents_sellers_procurator' not in data:
        return data
    
    procurators = data['gmn:P70_4_documents_sellers_procurator']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Get seller URI and data for P17 link and is_represented_by (if P23 exists)
    seller_uri = None
    seller_data = None
    if 'cidoc:P23_transferred_title_from' in existing_acquisition:
        sellers = existing_acquisition['cidoc:P23_transferred_title_from']
        if len(sellers) > 0:
            seller_obj = sellers[0]
            if isinstance(seller_obj, dict):
                seller_uri = seller_obj.get('@id')
                seller_data = seller_obj
            else:
                seller_uri = str(seller_obj)
                seller_data = {'@id': seller_uri, '@type': 'cidoc:E21_Person'}
    
    # Transform each procurator into an E7_Activity
    for procurator_obj in procurators:
        # Handle both URI references and full objects
        if isinstance(procurator_obj, dict):
            procurator_uri = procurator_obj.get('@id', '')
            procurator_data = procurator_obj.copy()
            if '@type' not in procurator_data:
                procurator_data['@type'] = 'cidoc:E21_Person'
        else:
            procurator_uri = str(procurator_obj)
            procurator_data = {
                '@id': procurator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add is_represented_by relationship from seller to procurator
        # Note: In a real implementation, you'd need to update the seller entity separately
        # For now, we'll note this in a special field for post-processing
        if seller_uri:
            if '_representation_links' not in data:
                data['_representation_links'] = []
            data['_representation_links'].append({
                'principal': seller_uri,
                'agent': procurator_uri,
                'property': 'gmn:is_represented_by'
            })
        
        # Create activity URI
        activity_hash = str(hash(procurator_uri + 'seller_procurator'))[-8:]
        activity_uri = f"{subject_uri}/activity/sellers_procurator_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [procurator_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_AGENT,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if we have seller
        if seller_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_4_documents_sellers_procurator']
    
    return data

def transform_p70_5_documents_buyers_procurator(data):
    """
    Transform gmn:P70_5_documents_buyers_procurator to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person
    with P17_was_motivated_by linking to the buyer
    
    Also adds gmn:is_represented_by property from buyer to procurator.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_5_documents_buyers_procurator' not in data:
        return data
    
    procurators = data['gmn:P70_5_documents_buyers_procurator']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Get buyer URI and data for P17 link and is_represented_by (if P22 exists)
    buyer_uri = None
    buyer_data = None
    if 'cidoc:P22_transferred_title_to' in existing_acquisition:
        buyers = existing_acquisition['cidoc:P22_transferred_title_to']
        if len(buyers) > 0:
            buyer_obj = buyers[0]
            if isinstance(buyer_obj, dict):
                buyer_uri = buyer_obj.get('@id')
                buyer_data = buyer_obj
            else:
                buyer_uri = str(buyer_obj)
                buyer_data = {'@id': buyer_uri, '@type': 'cidoc:E21_Person'}
    
    # Transform each procurator into an E7_Activity
    for procurator_obj in procurators:
        # Handle both URI references and full objects
        if isinstance(procurator_obj, dict):
            procurator_uri = procurator_obj.get('@id', '')
            procurator_data = procurator_obj.copy()
            if '@type' not in procurator_data:
                procurator_data['@type'] = 'cidoc:E21_Person'
        else:
            procurator_uri = str(procurator_obj)
            procurator_data = {
                '@id': procurator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add is_represented_by relationship from buyer to procurator
        if buyer_uri:
            if '_representation_links' not in data:
                data['_representation_links'] = []
            data['_representation_links'].append({
                'principal': buyer_uri,
                'agent': procurator_uri,
                'property': 'gmn:is_represented_by'
            })
        
        # Create activity URI
        activity_hash = str(hash(procurator_uri + 'buyer_procurator'))[-8:]
        activity_uri = f"{subject_uri}/activity/buyers_procurator_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [procurator_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_AGENT,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if we have buyer
        if buyer_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': buyer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_5_documents_buyers_procurator']
    
    return data

def transform_p70_6_documents_sellers_guarantor(data):
    """
    Transform gmn:P70_6_documents_sellers_guarantor to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person
    with P17_was_motivated_by linking to the seller
    
    Also adds gmn:is_guaranteed_by property from seller to guarantor.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_6_documents_sellers_guarantor' not in data:
        return data
    
    guarantors = data['gmn:P70_6_documents_sellers_guarantor']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Get seller URI and data for P17 link and is_guaranteed_by (if P23 exists)
    seller_uri = None
    seller_data = None
    if 'cidoc:P23_transferred_title_from' in existing_acquisition:
        sellers = existing_acquisition['cidoc:P23_transferred_title_from']
        if len(sellers) > 0:
            seller_obj = sellers[0]
            if isinstance(seller_obj, dict):
                seller_uri = seller_obj.get('@id')
                seller_data = seller_obj
            else:
                seller_uri = str(seller_obj)
                seller_data = {'@id': seller_uri, '@type': 'cidoc:E21_Person'}
    
    # Transform each guarantor into an E7_Activity
    for guarantor_obj in guarantors:
        # Handle both URI references and full objects
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
            if '@type' not in guarantor_data:
                guarantor_data['@type'] = 'cidoc:E21_Person'
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add is_guaranteed_by relationship from seller to guarantor
        if seller_uri:
            if '_guarantee_links' not in data:
                data['_guarantee_links'] = []
            data['_guarantee_links'].append({
                'principal': seller_uri,
                'guarantor': guarantor_uri,
                'property': 'gmn:is_guaranteed_by'
            })
        
        # Create activity URI
        activity_hash = str(hash(guarantor_uri + 'seller_guarantor'))[-8:]
        activity_uri = f"{subject_uri}/activity/sellers_guarantor_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if we have seller
        if seller_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_6_documents_sellers_guarantor']
    
    return data

def transform_p70_7_documents_buyers_guarantor(data):
    """
    Transform gmn:P70_7_documents_buyers_guarantor to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person
    with P17_was_motivated_by linking to the buyer
    
    Also adds gmn:is_guaranteed_by property from buyer to guarantor.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_7_documents_buyers_guarantor' not in data:
        return data
    
    guarantors = data['gmn:P70_7_documents_buyers_guarantor']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Get buyer URI and data for P17 link and is_guaranteed_by (if P22 exists)
    buyer_uri = None
    buyer_data = None
    if 'cidoc:P22_transferred_title_to' in existing_acquisition:
        buyers = existing_acquisition['cidoc:P22_transferred_title_to']
        if len(buyers) > 0:
            buyer_obj = buyers[0]
            if isinstance(buyer_obj, dict):
                buyer_uri = buyer_obj.get('@id')
                buyer_data = buyer_obj
            else:
                buyer_uri = str(buyer_obj)
                buyer_data = {'@id': buyer_uri, '@type': 'cidoc:E21_Person'}
    
    # Transform each guarantor into an E7_Activity
    for guarantor_obj in guarantors:
        # Handle both URI references and full objects
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
            if '@type' not in guarantor_data:
                guarantor_data['@type'] = 'cidoc:E21_Person'
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add is_guaranteed_by relationship from buyer to guarantor
        if buyer_uri:
            if '_guarantee_links' not in data:
                data['_guarantee_links'] = []
            data['_guarantee_links'].append({
                'principal': buyer_uri,
                'guarantor': guarantor_uri,
                'property': 'gmn:is_guaranteed_by'
            })
        
        # Create activity URI
        activity_hash = str(hash(guarantor_uri + 'buyer_guarantor'))[-8:]
        activity_uri = f"{subject_uri}/activity/buyers_guarantor_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if we have buyer
        if buyer_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': buyer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_7_documents_buyers_guarantor']
    
    return data

def transform_p70_8_documents_broker(data):
    """
    Transform gmn:P70_8_documents_broker to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P14_carried_out_by > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_8_documents_broker' not in data:
        return data
    
    brokers = data['gmn:P70_8_documents_broker']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_acquisition:
        existing_acquisition['cidoc:P14_carried_out_by'] = []
    
    # Add brokers to acquisition event
    for broker_obj in brokers:
        # Handle both URI references and full objects
        if isinstance(broker_obj, dict):
            broker_data = broker_obj.copy()
            if '@type' not in broker_data:
                broker_data['@type'] = 'cidoc:E21_Person'
        else:
            broker_uri = str(broker_obj)
            broker_data = {
                '@id': broker_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add broker directly to acquisition event via P14
        existing_acquisition['cidoc:P14_carried_out_by'].append(broker_data)
    
    # Add role type for brokers if any were added
    if len(brokers) > 0:
        if 'cidoc:P14.1_in_the_role_of' not in existing_acquisition:
            existing_acquisition['cidoc:P14.1_in_the_role_of'] = []
        
        # Add broker role type
        broker_role = {
            '@id': AAT_BROKER,
            '@type': 'cidoc:E55_Type'
        }
        existing_acquisition['cidoc:P14.1_in_the_role_of'].append(broker_role)
    
    # Remove shortcut property
    del data['gmn:P70_8_documents_broker']
    
    return data

def transform_p70_9_documents_payment_provider_for_buyer(data):
    """
    Transform gmn:P70_9_documents_payment_provider_for_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person
    with P17_was_motivated_by linking to the buyer
    
    Also adds gmn:has_payment_provided_by property from buyer to payment provider.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_9_documents_payment_provider_for_buyer' not in data:
        return data
    
    payment_providers = data['gmn:P70_9_documents_payment_provider_for_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Get buyer URI and data for P17 link and has_payment_provided_by (if P22 exists)
    buyer_uri = None
    buyer_data = None
    if 'cidoc:P22_transferred_title_to' in existing_acquisition:
        buyers = existing_acquisition['cidoc:P22_transferred_title_to']
        if len(buyers) > 0:
            buyer_obj = buyers[0]
            if isinstance(buyer_obj, dict):
                buyer_uri = buyer_obj.get('@id')
                buyer_data = buyer_obj
            else:
                buyer_uri = str(buyer_obj)
                buyer_data = {'@id': buyer_uri, '@type': 'cidoc:E21_Person'}
    
    # Transform each payment provider into an E7_Activity
    for provider_obj in payment_providers:
        # Handle both URI references and full objects
        if isinstance(provider_obj, dict):
            provider_uri = provider_obj.get('@id', '')
            provider_data = provider_obj.copy()
            if '@type' not in provider_data:
                provider_data['@type'] = 'cidoc:E21_Person'
        else:
            provider_uri = str(provider_obj)
            provider_data = {
                '@id': provider_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add has_payment_provided_by relationship from buyer to payment provider
        if buyer_uri:
            if '_payment_provider_links' not in data:
                data['_payment_provider_links'] = []
            data['_payment_provider_links'].append({
                'buyer': buyer_uri,
                'payment_provider': provider_uri,
                'property': 'gmn:has_payment_provided_by'
            })
        
        # Create activity URI
        activity_hash = str(hash(provider_uri + 'payment_provider'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_provider_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [provider_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYER,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if we have buyer
        if buyer_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': buyer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_9_documents_payment_provider_for_buyer']
    
    return data

def transform_p70_10_documents_payment_recipient_for_seller(data):
    """
    Transform gmn:P70_10_documents_payment_recipient_for_seller to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person
    with P17_was_motivated_by linking to the seller
    
    Also adds gmn:has_payment_received_by property from seller to payment recipient.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_10_documents_payment_recipient_for_seller' not in data:
        return data
    
    payment_recipients = data['gmn:P70_10_documents_payment_recipient_for_seller']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Get seller URI and data for P17 link and has_payment_received_by (if P23 exists)
    seller_uri = None
    seller_data = None
    if 'cidoc:P23_transferred_title_from' in existing_acquisition:
        sellers = existing_acquisition['cidoc:P23_transferred_title_from']
        if len(sellers) > 0:
            seller_obj = sellers[0]
            if isinstance(seller_obj, dict):
                seller_uri = seller_obj.get('@id')
                seller_data = seller_obj
            else:
                seller_uri = str(seller_obj)
                seller_data = {'@id': seller_uri, '@type': 'cidoc:E21_Person'}
    
    # Transform each payment recipient into an E7_Activity
    for recipient_obj in payment_recipients:
        # Handle both URI references and full objects
        if isinstance(recipient_obj, dict):
            recipient_uri = recipient_obj.get('@id', '')
            recipient_data = recipient_obj.copy()
            if '@type' not in recipient_data:
                recipient_data['@type'] = 'cidoc:E21_Person'
        else:
            recipient_uri = str(recipient_obj)
            recipient_data = {
                '@id': recipient_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add has_payment_received_by relationship from seller to payment recipient
        if seller_uri:
            if '_payment_recipient_links' not in data:
                data['_payment_recipient_links'] = []
            data['_payment_recipient_links'].append({
                'seller': seller_uri,
                'payment_recipient': recipient_uri,
                'property': 'gmn:has_payment_received_by'
            })
        
        # Create activity URI
        activity_hash = str(hash(recipient_uri + 'payment_recipient'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_recipient_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [recipient_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYEE,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add P17_was_motivated_by if we have seller
        if seller_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_10_documents_payment_recipient_for_seller']
    
    return data

def transform_p70_11_documents_referenced_person(data):
    """
    Transform gmn:P70_11_documents_referenced_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    
    This creates a direct relationship between the document and referenced persons
    without implying their participation in the acquisition event. Used for persons
    mentioned in the contract text who are not parties to the transaction (witnesses,
    deceased persons, neighbors, etc.).
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_11_documents_referenced_person' not in data:
        return data
    
    referenced_persons = data['gmn:P70_11_documents_referenced_person']
    
    # Initialize P67 if it doesn't exist
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Add referenced persons directly to the document
    for person_obj in referenced_persons:
        # Handle both URI references and full objects
        if isinstance(person_obj, dict):
            person_data = person_obj.copy()
            if '@type' not in person_data:
                person_data['@type'] = 'cidoc:E21_Person'
        else:
            person_uri = str(person_obj)
            person_data = {
                '@id': person_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add person directly to document via P67_refers_to
        data['cidoc:P67_refers_to'].append(person_data)
    
    # Remove shortcut property
    del data['gmn:P70_11_documents_referenced_person']
    
    return data

def transform_p70_12_documents_payment_through_organization(data):
    """
    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E74_Group
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        return data
    
    organizations = data['gmn:P70_12_documents_payment_through_organization']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P9 if it doesn't exist
    if 'cidoc:P9_consists_of' not in existing_acquisition:
        existing_acquisition['cidoc:P9_consists_of'] = []
    
    # Transform each organization into an E7_Activity
    for org_obj in organizations:
        # Handle both URI references and full objects
        if isinstance(org_obj, dict):
            org_uri = org_obj.get('@id', '')
            org_data = org_obj.copy()
            if '@type' not in org_data:
                org_data['@type'] = 'cidoc:E74_Group'
        else:
            org_uri = str(org_obj)
            org_data = {
                '@id': org_uri,
                '@type': 'cidoc:E74_Group'
            }
        
        # Create activity URI
        activity_hash = str(hash(org_uri + 'payment_organization'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_organization_{activity_hash}"
        
        # Create E7_Activity
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [org_data],
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add activity to acquisition
        existing_acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove shortcut property
    del data['gmn:P70_12_documents_payment_through_organization']
    
    return data

def transform_p70_13_documents_referenced_place(data):
    """
    Transform gmn:P70_13_documents_referenced_place to full CIDOC-CRM structure:
    P67_refers_to > E53_Place
    
    This creates a direct relationship between the document and referenced places
    mentioned in the contract text (neighbors, landmarks, districts, etc.).
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_13_documents_referenced_place' not in data:
        return data
    
    referenced_places = data['gmn:P70_13_documents_referenced_place']
    
    # Initialize P67 if it doesn't exist
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Add referenced places directly to the document
    for place_obj in referenced_places:
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
        
        # Add place directly to document via P67_refers_to
        data['cidoc:P67_refers_to'].append(place_data)
    
    # Remove shortcut property
    del data['gmn:P70_13_documents_referenced_place']
    
    return data

def transform_p70_14_documents_referenced_object(data):
    """
    Transform gmn:P70_14_documents_referenced_object to full CIDOC-CRM structure:
    P67_refers_to > E1_CRM_Entity
    
    This creates a direct relationship between the document and referenced objects
    (both legal objects like rights, obligations, debts, and physical objects) 
    mentioned in the contract.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_14_documents_referenced_object' not in data:
        return data
    
    referenced_objects = data['gmn:P70_14_documents_referenced_object']
    
    # Initialize P67 if it doesn't exist
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Add referenced objects directly to the document
    for obj in referenced_objects:
        # Handle both URI references and full objects
        if isinstance(obj, dict):
            obj_data = obj.copy()
            if '@type' not in obj_data:
                obj_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            obj_uri = str(obj)
            obj_data = {
                '@id': obj_uri,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add object directly to document via P67_refers_to
        data['cidoc:P67_refers_to'].append(obj_data)
    
    # Remove shortcut property
    del data['gmn:P70_14_documents_referenced_object']
    
    return data

def transform_p70_15_documents_witness(data):
    """
    Transform gmn:P70_15_documents_witness to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P11_had_participant > E21_Person
    
    Witnesses are participants in the acquisition event who observed and validated
    the transaction.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_15_documents_witness' not in data:
        return data
    
    witnesses = data['gmn:P70_15_documents_witness']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P11 if it doesn't exist
    if 'cidoc:P11_had_participant' not in existing_acquisition:
        existing_acquisition['cidoc:P11_had_participant'] = []
    
    # Add witnesses to acquisition event
    for witness_obj in witnesses:
        # Handle both URI references and full objects
        if isinstance(witness_obj, dict):
            witness_data = witness_obj.copy()
            if '@type' not in witness_data:
                witness_data['@type'] = 'cidoc:E21_Person'
        else:
            witness_uri = str(witness_obj)
            witness_data = {
                '@id': witness_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add witness to acquisition event via P11
        existing_acquisition['cidoc:P11_had_participant'].append(witness_data)
    
    # Add role type for witnesses if any were added
    if len(witnesses) > 0:
        if 'cidoc:P11.1_in_the_role_of' not in existing_acquisition:
            existing_acquisition['cidoc:P11.1_in_the_role_of'] = []
        
        # Add witness role type
        witness_role = {
            '@id': AAT_WITNESS,
            '@type': 'cidoc:E55_Type'
        }
        # Check if witness role not already present
        role_already_present = any(
            isinstance(r, dict) and r.get('@id') == AAT_WITNESS
            for r in existing_acquisition['cidoc:P11.1_in_the_role_of']
        )
        if not role_already_present:
            existing_acquisition['cidoc:P11.1_in_the_role_of'].append(witness_role)
    
    # Remove shortcut property
    del data['gmn:P70_15_documents_witness']
    
    return data

def transform_p70_16_documents_sale_price_amount(data):
    """
    Transform gmn:P70_16_documents_sale_price_amount to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P181_has_amount
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_16_documents_sale_price_amount' not in data:
        return data
    
    amounts = data['gmn:P70_16_documents_sale_price_amount']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Check if monetary amount already exists
    existing_monetary_amount = None
    if 'cidoc:P177_assigned_property_of_type' in existing_acquisition:
        # Use existing monetary amount if it exists
        existing_monetary_amount = existing_acquisition['cidoc:P177_assigned_property_of_type']
    else:
        # Create new monetary amount
        monetary_amount_uri = f"{subject_uri}/monetary_amount"
        existing_monetary_amount = {
            '@id': monetary_amount_uri,
            '@type': 'cidoc:E97_Monetary_Amount'
        }
        existing_acquisition['cidoc:P177_assigned_property_of_type'] = existing_monetary_amount
    
    # Add amounts (typically only one, but handle multiple)
    for amount_obj in amounts:
        # Handle both simple values and object values
        if isinstance(amount_obj, dict):
            amount_value = amount_obj.get('@value', '')
            amount_type = amount_obj.get('@type', 'http://www.w3.org/2001/XMLSchema#decimal')
        else:
            amount_value = str(amount_obj)
            amount_type = 'http://www.w3.org/2001/XMLSchema#decimal'
        
        # Set P181_has_amount
        existing_monetary_amount['cidoc:P181_has_amount'] = {
            '@value': amount_value,
            '@type': amount_type
        }
    
    # Remove shortcut property
    del data['gmn:P70_16_documents_sale_price_amount']
    
    return data

def transform_p70_17_documents_sale_price_currency(data):
    """
    Transform gmn:P70_17_documents_sale_price_currency to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P180_has_currency > E98_Currency
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_17_documents_sale_price_currency' not in data:
        return data
    
    currencies = data['gmn:P70_17_documents_sale_price_currency']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Check if monetary amount already exists
    existing_monetary_amount = None
    if 'cidoc:P177_assigned_property_of_type' in existing_acquisition:
        # Use existing monetary amount if it exists
        existing_monetary_amount = existing_acquisition['cidoc:P177_assigned_property_of_type']
    else:
        # Create new monetary amount
        monetary_amount_uri = f"{subject_uri}/monetary_amount"
        existing_monetary_amount = {
            '@id': monetary_amount_uri,
            '@type': 'cidoc:E97_Monetary_Amount'
        }
        existing_acquisition['cidoc:P177_assigned_property_of_type'] = existing_monetary_amount
    
    # Add currencies (typically only one, but handle multiple)
    for currency_obj in currencies:
        # Handle both URI references and full objects
        if isinstance(currency_obj, dict):
            currency_data = currency_obj.copy()
            if '@type' not in currency_data:
                currency_data['@type'] = 'cidoc:E98_Currency'
        else:
            currency_uri = str(currency_obj)
            currency_data = {
                '@id': currency_uri,
                '@type': 'cidoc:E98_Currency'
            }
        
        # Set P180_has_currency
        existing_monetary_amount['cidoc:P180_has_currency'] = currency_data
    
    # Remove shortcut property
    del data['gmn:P70_17_documents_sale_price_currency']
    
    return data

# Arbitration Agreement transformation functions

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

def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    """
    # Name and identification properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p102_1_has_title(item)
    
    # Editorial notes
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    # Biographical properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
    item = transform_p96_1_has_mother(item)
    item = transform_p97_1_has_father(item)
    
    # Group membership properties
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)
    
    # Document creation properties
    item = transform_p94i_1_was_created_by(item)
    item = transform_p94i_2_has_enactment_date(item)
    item = transform_p94i_3_has_place_of_enactment(item)
    item = transform_p138i_1_has_representation(item)
    
    # Sales contract properties
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
    item = transform_p70_15_documents_witness(item)
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # Arbitration agreement properties
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    
    return item

def transform_export(input_file, output_file, include_internal=False):
    """
    Transform an entire JSON-LD export file.
    
    Args:
        input_file: Path to input JSON-LD file
        output_file: Path to output CIDOC-CRM compliant file
        include_internal: If True, transform internal notes. If False (default), remove them.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single items and arrays of items
        if isinstance(data, list):
            transformed = [transform_item(item, include_internal) for item in data]
        elif isinstance(data, dict) and '@graph' in data:
            # Handle JSON-LD with @graph
            data['@graph'] = [transform_item(item, include_internal) for item in data['@graph']]
            transformed = data
        else:
            transformed = transform_item(data, include_internal)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Transformation complete: {output_file}")
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: Input file '{input_file}' not found", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON in input file: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Error during transformation: {e}", file=sys.stderr)
        return False

def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python transform_gmn.py <input_file.json> <output_file.json> [--include-internal]")
        print("\nOptions:")
        print("  --include-internal    Include editorial notes in output (default: exclude)")
        print("\nExamples:")
        print("  python transform_gmn.py omeka_export.json public_output.json")
        print("  python transform_gmn.py omeka_export.json full_output.json --include-internal")
        print("\nNote: This script handles gmn:E31_1_Contract, gmn:E31_2_Sales_Contract,")
        print("      and gmn:E31_3_Arbitration_Agreement")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    include_internal = '--include-internal' in sys.argv
    
    if include_internal:
        print("Note: Including internal editorial notes in output")
    else:
        print("Note: Excluding internal editorial notes from output")
    
    success = transform_export(input_file, output_file, include_internal)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
    if 'cidoc:P53i_is_former_or_current_location_of' not in data:
        data['cidoc:P53i_is_former_or_current_location_of'] = []
    
    # Transform each occupant (each represents a separate move)
    for occupant_obj in occupants:
        # Handle both URI references and full objects
        if isinstance(occupant_obj, dict):
            occupant_uri = occupant_obj.get('@id', '')
            occupant_data = occupant_obj.copy()
            if '@type' not in occupant_data:
                occupant_data['@type'] = 'cidoc:E21_Person'
        else:
            occupant_uri = str(occupant_obj)
            occupant_data = {
                '@id': occupant_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Create move event URI
        occupant_hash = str(hash(occupant_uri + 'move'))[-8:]
        move_uri = f"{subject_uri}/move/{occupant_hash}"
        
        # Create full CIDOC-CRM structure
        move_event = {
            '@id': move_uri,
            '@type': 'cidoc:E9_Move',
            'cidoc:P25_moved': occupant_data,
            'cidoc:P26_moved_to': {
                '@id': subject_uri,
                '@type': 'gmn:E22_1_Building'
            }
        }
        
        # Add to P53i
        data['cidoc:P53i_is_former_or_current_location_of'].append(move_event)
    
    # Remove shortcut property
    del data['gmn:P53_1_has_occupant']
    
    return data

def transform_p96_1_has_mother(data):
    """
    Transform gmn:P96_1_has_mother to full CIDOC-CRM structure:
    P98i_was_born > E67_Birth > P96_by_mother > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P96_1_has_mother' not in data:
        return data
    
    mothers = data['gmn:P96_1_has_mother']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if birth event already exists
    existing_birth = None
    if 'cidoc:P98i_was_born' in data and len(data['cidoc:P98i_was_born']) > 0:
        # Use existing birth event
        existing_birth = data['cidoc:P98i_was_born'][0]
    else:
        # Create new birth event
        birth_uri = f"{subject_uri}/birth"
        existing_birth = {
            '@id': birth_uri,
            '@type': 'cidoc:E67_Birth'
        }
        data['cidoc:P98i_was_born'] = [existing_birth]
    
    # Add mothers to birth event
    for mother_obj in mothers:
        # Handle both URI references and full objects
        if isinstance(mother_obj, dict):
            mother_data = mother_obj.copy()
            if '@type' not in mother_data:
                mother_data['@type'] = 'cidoc:E21_Person'
        else:
            mother_uri = str(mother_obj)
            mother_data = {
                '@id': mother_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add to birth event
        if 'cidoc:P96_by_mother' not in existing_birth:
            existing_birth['cidoc:P96_by_mother'] = []
        existing_birth['cidoc:P96_by_mother'].append(mother_data)
    
    # Remove shortcut property
    del data['gmn:P96_1_has_mother']
    
    return data

def transform_p97_1_has_father(data):
    """
    Transform gmn:P97_1_has_father to full CIDOC-CRM structure:
    P98i_was_born > E67_Birth > P97_from_father > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P97_1_has_father' not in data:
        return data
    
    fathers = data['gmn:P97_1_has_father']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if birth event already exists
    existing_birth = None
    if 'cidoc:P98i_was_born' in data and len(data['cidoc:P98i_was_born']) > 0:
        # Use existing birth event
        existing_birth = data['cidoc:P98i_was_born'][0]
    else:
        # Create new birth event
        birth_uri = f"{subject_uri}/birth"
        existing_birth = {
            '@id': birth_uri,
            '@type': 'cidoc:E67_Birth'
        }
        data['cidoc:P98i_was_born'] = [existing_birth]
    
    # Add fathers to birth event
    for father_obj in fathers:
        # Handle both URI references and full objects
        if isinstance(father_obj, dict):
            father_data = father_obj.copy()
            if '@type' not in father_data:
                father_data['@type'] = 'cidoc:E21_Person'
        else:
            father_uri = str(father_obj)
            father_data = {
                '@id': father_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add to birth event
        if 'cidoc:P97_from_father' not in existing_birth:
            existing_birth['cidoc:P97_from_father'] = []
        existing_birth['cidoc:P97_from_father'].append(father_data)
    
    # Remove shortcut property
    del data['gmn:P97_1_has_father']
    
    return data

def transform_p102_1_has_title(data):
    """
    Transform gmn:P102_1_has_title to full CIDOC-CRM structure:
    P102_has_title > E35_Title > P190_has_symbolic_content
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P102_1_has_title' not in data:
        return data
    
    titles = data['gmn:P102_1_has_title']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P102 if it doesn't exist
    if 'cidoc:P102_has_title' not in data:
        data['cidoc:P102_has_title'] = []
    
    # Transform each title
    for title_obj in titles:
        # Handle both simple string values and object values
        if isinstance(title_obj, dict):
            title_value = title_obj.get('@value', '')
            language = title_obj.get('@language', None)
        else:
            title_value = str(title_obj)
            language = None
        
        # Create title URI
        title_hash = str(hash(title_value + 'title'))[-8:]
        title_uri = f"{subject_uri}/title/{title_hash}"
        
        # Build P190 content
        p190_content = {'@value': title_value}
        if language:
            p190_content['@language'] = language
        
        # Create full CIDOC-CRM structure
        title_entity = {
            '@id': title_uri,
            '@type': 'cidoc:E35_Title',
            'cidoc:P190_has_symbolic_content': [p190_content]
        }
        
        # Add to P102
        data['cidoc:P102_has_title'].append(title_entity)
    
    # Remove shortcut property
    del data['gmn:P102_1_has_title']
    
    return data

def transform_p107i_1_has_regional_provenance(data):
    """
    Transform gmn:P107i_1_has_regional_provenance to full CIDOC-CRM structure:
    P107i_is_current_or_former_member_of > gmn:E74_1_Regional_Provenance with P2_has_type (AAT 300055490)
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P107i_1_has_regional_provenance' not in data:
        return data
    
    groups = data['gmn:P107i_1_has_regional_provenance']
    
    # Initialize P107i if it doesn't exist
    if 'cidoc:P107i_is_current_or_former_member_of' not in data:
        data['cidoc:P107i_is_current_or_former_member_of'] = []
    
    # Transform each group reference
    for group_obj in groups:
        # Handle both URI references and full objects
        if isinstance(group_obj, dict):
            group_uri = group_obj.get('@id', '')
            # If it's already a full object, preserve it and add type
            group_data = group_obj.copy()
        else:
            group_uri = str(group_obj)
            group_data = {'@id': group_uri}
        
        # Ensure it has the gmn:E74_1_Regional_Provenance type
        if '@type' not in group_data:
            group_data['@type'] = ['cidoc:E74_Group', 'gmn:E74_1_Regional_Provenance']
        elif isinstance(group_data['@type'], str):
            group_data['@type'] = [group_data['@type'], 'gmn:E74_1_Regional_Provenance']
        elif 'gmn:E74_1_Regional_Provenance' not in group_data['@type']:
            group_data['@type'].append('gmn:E74_1_Regional_Provenance')
        
        # Add the regional type
        if 'cidoc:P2_has_type' not in group_data:
            group_data['cidoc:P2_has_type'] = []
        elif not isinstance(group_data['cidoc:P2_has_type'], list):
            group_data['cidoc:P2_has_type'] = [group_data['cidoc:P2_has_type']]
        
        # Add AAT regional type if not already present
        regional_type = {
            '@id': AAT_REGION,
            '@type': 'cidoc:E55_Type'
        }
        
        # Check if this type is already in the list
        type_already_present = any(
            isinstance(t, dict) and t.get('@id') == AAT_REGION 
            for t in group_data['cidoc:P2_has_type']
        )
        
        if not type_already_present:
            group_data['cidoc:P2_has_type'].append(regional_type)
        
        # Add to P107i
        data['cidoc:P107i_is_current_or_former_member_of'].append(group_data)
    
    # Remove shortcut property
    del data['gmn:P107i_1_has_regional_provenance']
    
    return data

def transform_p107i_2_has_social_category(data):
    """
    Transform gmn:P107i_2_has_social_category to full CIDOC-CRM structure:
    P107i_is_current_or_former_member_of > gmn:E74_2_Social_Category
    
    This is a simple rename without adding implicit types, allowing flexibility
    in how social groups are categorized.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P107i_2_has_social_category' not in data:
        return data
    
    groups = data['gmn:P107i_2_has_social_category']
    
    # Initialize P107i if it doesn't exist
    if 'cidoc:P107i_is_current_or_former_member_of' not in data:
        data['cidoc:P107i_is_current_or_former_member_of'] = []
    
    # Transform each group reference
    for group_obj in groups:
        # Handle both URI references and full objects
        if isinstance(group_obj, dict):
            group_data = group_obj.copy()
        else:
            group_uri = str(group_obj)
            group_data = {'@id': group_uri}
        
        # Ensure it has the gmn:E74_2_Social_Category type
        if '@type' not in group_data:
            group_data['@type'] = ['cidoc:E74_Group', 'gmn:E74_2_Social_Category']
        elif isinstance(group_data['@type'], str):
            group_data['@type'] = [group_data['@type'], 'gmn:E74_2_Social_Category']
        elif 'gmn:E74_2_Social_Category' not in group_data['@type']:
            group_data['@type'].append('gmn:E74_2_Social_Category')
        
        # Add to P107i
        data['cidoc:P107i_is_current_or_former_member_of'].append(group_data)
    
    # Remove shortcut property
    del data['gmn:P107i_2_has_social_category']
    
    return data

def transform_p107i_3_has_occupation(data):
    """
    Transform gmn:P107i_3_has_occupation to full CIDOC-CRM structure:
    P107i_is_current_or_former_member_of > gmn:E74_3_Occupational_Group
    
    This transforms occupational affiliations into group memberships.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P107i_3_has_occupation' not in data:
        return data
    
    groups = data['gmn:P107i_3_has_occupation']
    
    # Initialize P107i if it doesn't exist
    if 'cidoc:P107i_is_current_or_former_member_of' not in data:
        data['cidoc:P107i_is_current_or_former_member_of'] = []
    
    # Transform each group reference
    for group_obj in groups:
        # Handle both URI references and full objects
        if isinstance(group_obj, dict):
            group_data = group_obj.copy()
        else:
            group_uri = str(group_obj)
            group_data = {'@id': group_uri}
        
        # Ensure it has the gmn:E74_3_Occupational_Group type
        if '@type' not in group_data:
            group_data['@type'] = ['cidoc:E74_Group', 'gmn:E74_3_Occupational_Group']
        elif isinstance(group_data['@type'], str):
            group_data['@type'] = [group_data['@type'], 'gmn:E74_3_Occupational_Group']
        elif 'gmn:E74_3_Occupational_Group' not in group_data['@type']:
            group_data['@type'].append('gmn:E74_3_Occupational_Group')
        
        # Add to P107i
        data['cidoc:P107i_is_current_or_former_member_of'].append(group_data)
    
    # Remove shortcut property
    del data['gmn:P107i_3_has_occupation']
    
    return data

def transform_p94i_1_was_created_by(data):
    """
    Transform gmn:P94i_1_was_created_by to full CIDOC-CRM structure:
    P94i_was_created_by > E65_Creation > P14_carried_out_by > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P94i_1_was_created_by' not in data:
        return data
    
    creators = data['gmn:P94i_1_was_created_by']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if creation event already exists
    existing_creation = None
    if 'cidoc:P94i_was_created_by' in data and len(data['cidoc:P94i_was_created_by']) > 0:
        # Use existing creation event (assuming only one creation event per document)
        existing_creation = data['cidoc:P94i_was_created_by'][0]
    else:
        # Create new creation event
        creation_uri = f"{subject_uri}/creation"
        existing_creation = {
            '@id': creation_uri,
            '@type': 'cidoc:E65_Creation'
        }
        data['cidoc:P94i_was_created_by'] = [existing_creation]
    
    # Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_creation:
        existing_creation['cidoc:P14_carried_out_by'] = []
    
    # Add creators to creation event
    for creator_obj in creators:
        # Handle both URI references and full objects
        if isinstance(creator_obj, dict):
            creator_data = creator_obj.copy()
            if '@type' not in creator_data:
                creator_data['@type'] = 'cidoc:E21_Person'
        else:
            creator_uri = str(creator_obj)
            creator_data = {
                '@id': creator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add to creation event
        existing_creation['cidoc:P14_carried_out_by'].append(creator_data)
    
    # Remove shortcut property
    del data['gmn:P94i_1_was_created_by']
    
    return data

def transform_p94i_2_has_enactment_date(data):
    """
    Transform gmn:P94i_2_has_enactment_date to full CIDOC-CRM structure:
    P94i_was_created_by > E65_Creation > P4_has_time-span > E52_Time-Span > P82_at_some_time_within
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P94i_2_has_enactment_date' not in data:
        return data
    
    dates = data['gmn:P94i_2_has_enactment_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if creation event already exists
    existing_creation = None
    if 'cidoc:P94i_was_created_by' in data and len(data['cidoc:P94i_was_created_by']) > 0:
        # Use existing creation event
        existing_creation = data['cidoc:P94i_was_created_by'][0]
    else:
        # Create new creation event
        creation_uri = f"{subject_uri}/creation"
        existing_creation = {
            '@id': creation_uri,
            '@type': 'cidoc:E65_Creation'
        }
        data['cidoc:P94i_was_created_by'] = [existing_creation]
    
    # Initialize P4 if it doesn't exist
    if 'cidoc:P4_has_time-span' not in existing_creation:
        existing_creation['cidoc:P4_has_time-span'] = []
    
    # Transform each date
    for date_obj in dates:
        # Handle both simple string values and object values
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
            date_type = date_obj.get('@type', 'http://www.w3.org/2001/XMLSchema#date')
        else:
            date_value = str(date_obj)
            date_type = 'http://www.w3.org/2001/XMLSchema#date'
        
        # Create timespan URI
        date_hash = str(hash(date_value + 'enactment'))[-8:]
        timespan_uri = f"{subject_uri}/timespan/{date_hash}"
        
        # Create full CIDOC-CRM structure
        timespan = {
            '@id': timespan_uri,
            '@type': 'cidoc:E52_Time-Span',
            'cidoc:P82_at_some_time_within': {
                '@value': date_value,
                '@type': date_type
            }
        }
        
        # Add to creation event
        existing_creation['cidoc:P4_has_time-span'].append(timespan)
    
    # Remove shortcut property
    del data['gmn:P94i_2_has_enactment_date']
    
    return data

def transform_p94i_3_has_place_of_enactment(data):
    """
    Transform gmn:P94i_3_has_place_of_enactment to full CIDOC-CRM structure:
    P94i_was_created_by > E65_Creation > P7_took_place_at > E53_Place
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P94i_3_has_place_of_enactment' not in data:
        return data
    
    places = data['gmn:P94i_3_has_place_of_enactment']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if creation event already exists
    existing_creation = None
    if 'cidoc:P94i_was_created_by' in data and len(data['cidoc:P94i_was_created_by']) > 0:
        # Use existing creation event
        existing_creation = data['cidoc:P94i_was_created_by'][0]
    else:
        # Create new creation event
        creation_uri = f"{subject_uri}/creation"
        existing_creation = {
            '@id': creation_uri,
            '@type': 'cidoc:E65_Creation'
        }
        data['cidoc:P94i_was_created_by'] = [existing_creation]
    
    # Initialize P7 if it doesn't exist
    if 'cidoc:P7_took_place_at' not in existing_creation:
        existing_creation['cidoc:P7_took_place_at'] = []
    
    # Add places to creation event
    for place_obj in places:
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
        
        # Add to creation event
        existing_creation['cidoc:P7_took_place_at'].append(place_data)
    
    # Remove shortcut property
    del data['gmn:P94i_3_has_place_of_enactment']
    
    return data

def transform_p138i_1_has_representation(data):
    """
    Transform gmn:P138i_1_has_representation to full CIDOC-CRM structure:
    P138i_has_representation > D1_Digital_Object
    
    This links documents to their digital representations (JPEG, TIFF, PDF, etc.).
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P138i_1_has_representation' not in data:
        return data
    
    representations = data['gmn:P138i_1_has_representation']
    
    # Initialize P138i if it doesn't exist
    if 'cidoc:P138i_has_representation' not in data:
        data['cidoc:P138i_has_representation'] = []
    
    # Add digital representations to the document
    for rep_obj in representations:
        # Handle both URI references and full objects
        if isinstance(rep_obj, dict):
            rep_data = rep_obj.copy()
            if '@type' not in rep_data:
                rep_data['@type'] = 'cidoc:D1_Digital_Object'
        else:
            rep_uri = str(rep_obj)
            rep_data = {
                '@id': rep_uri,
                '@type': 'cidoc:D1_Digital_Object'
            }
        
        # Add digital object to document via P138i
        data['cidoc:P138i_has_representation'].append(rep_data)
    
    # Remove shortcut property
    del data['gmn:P138i_1_has_representation']
    
    return data

# Sales Contract transformation functions

def transform_p70_1_documents_seller(data):
    """
    Transform gmn:P70_1_documents_seller to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P23_transferred_title_from > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_1_documents_seller' not in data:
        return data
    
    sellers = data['gmn:P70_1_documents_seller']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event (assuming only one acquisition per contract)
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P23 if it doesn't exist
    if 'cidoc:P23_transferred_title_from' not in existing_acquisition:
        existing_acquisition['cidoc:P23_transferred_title_from'] = []
    
    # Add sellers to acquisition event
    for seller_obj in sellers:
        # Handle both URI references and full objects
        if isinstance(seller_obj, dict):
            seller_data = seller_obj.copy()
            if '@type' not in seller_data:
                seller_data['@type'] = 'cidoc:E21_Person'
        else:
            seller_uri = str(seller_obj)
            seller_data = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add to acquisition event
        existing_acquisition['cidoc:P23_transferred_title_from'].append(seller_data)
    
    # Remove shortcut property
    del data['gmn:P70_1_documents_seller']
    
    return data

def transform_p70_2_documents_buyer(data):
    """
    Transform gmn:P70_2_documents_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P22_transferred_title_to > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_2_documents_buyer' not in data:
        return data
    
    buyers = data['gmn:P70_2_documents_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P22 if it doesn't exist
    if 'cidoc:P22_transferred_title_to' not in existing_acquisition:
        existing_acquisition['cidoc:P22_transferred_title_to'] = []
    
    # Add buyers to acquisition event
    for buyer_obj in buyers:
        # Handle both URI references and full objects
        if isinstance(buyer_obj, dict):
            buyer_data = buyer_obj.copy()
            if '@type' not in buyer_data:
                buyer_data['@type'] = 'cidoc:E21_Person'
        else:
            buyer_uri = str(buyer_obj)
            buyer_data = {
                '@id': buyer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add to acquisition event
        existing_acquisition['cidoc:P22_transferred_title_to'].append(buyer_data)
    
    # Remove shortcut property
    del data['gmn:P70_2_documents_buyer']
    
    return data

def transform_p70_3_documents_transfer_of(data):
    """
    Transform gmn:P70_3_documents_transfer_of to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_3_documents_transfer_of' not in data:
        return data
    
    objects = data['gmn:P70_3_documents_transfer_of']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if acquisition event already exists
    existing_acquisition = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing acquisition event
        existing_acquisition = data['cidoc:P70_documents'][0]
    else:
        # Create new acquisition event
        acquisition_uri = f"{subject_uri}/acquisition"
        existing_acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
        data['cidoc:P70_documents'] = [existing_acquisition]
    
    # Initialize P24 if it doesn't exist
    if 'cidoc:P24_transferred_title_of' not in existing_acquisition:
        existing_acquisition['cidoc:P24_transferred_title_of'] = []
    
    # Add objects to acquisition event
    for object_obj in objects:
        # Handle both URI references and full objects
        if isinstance(object_obj, dict):
            object_data = object_obj.copy()
            # Preserve existing type or default to E18_Physical_Thing#!/usr/bin/env python3
"""
Transform GMN shortcut properties to full CIDOC-CRM compliant structure.

This script reads JSON-LD export from Omeka-S and transforms custom shortcut
properties (like gmn:P1_1_has_name) into their full CIDOC-CRM equivalents.

Updated to reflect class hierarchy:
- gmn:E31_1_Contract (general contract class)
- gmn:E31_2_Sales_Contract (specialized sales contract, subclass of E31_1_Contract)
- gmn:E31_3_Arbitration_Agreement (specialized arbitration agreement, subclass of E31_1_Contract)
"""

import json
import sys
from uuid import uuid4

# Getty AAT URI for names (general)
AAT_NAME = "http://vocab.getty.edu/page/aat/300404650"
# Getty AAT URI for names found in sources
AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"
# Getty AAT URI for patronymics (patrilineal names)
AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"
# Getty AAT URI for editorial notes
AAT_EDITORIAL_NOTE = "http://vocab.getty.edu/page/aat/300456627"
# Wikidata URI for loconyms
WIKIDATA_LOCONYM = "https://www.wikidata.org/wiki/Q17143070"
# Getty AAT URI for regions (geographic)
AAT_REGION = "http://vocab.getty.edu/page/aat/300055490"
# Getty AAT URI for marriages
AAT_MARRIAGE = "http://vocab.getty.edu/page/aat/300055475"
# Getty AAT URI for procurators/agents
AAT_AGENT = "http://vocab.getty.edu/page/aat/300025972"
# Getty AAT URI for guarantors
AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"
# Getty AAT URI for brokers
AAT_BROKER = "http://vocab.getty.edu/page/aat/300025234"
# Getty AAT URI for payers
AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"
# Getty AAT URI for payees
AAT_PAYEE = "http://vocab.getty.edu/page/aat/300386184"
# Getty AAT URI for financial transactions
AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"
# Getty AAT URI for witnesses
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"
# Getty AAT URI for arbitration (process)
AAT_ARBITRATION = "http://vocab.getty.edu/page/aat/300417271"

def generate_appellation_uri(subject_uri, name_value, suffix=""):
    """Generate a unique URI for an appellation resource."""
    # Create a deterministic URI based on subject and name
    name_hash = str(hash(name_value + suffix))[-8:]
    return f"{subject_uri}/appellation/{name_hash}"

def transform_name_property(data, property_name, aat_type_uri):
    """
    Generic function to transform name shortcut properties to full CIDOC-CRM structure.
    
    Args:
        data: The item data dictionary
        property_name: The shortcut property to transform (e.g., 'gmn:P1_1_has_name')
        aat_type_uri: The Getty AAT URI for the appellation type
    
    Returns:
        Modified data dictionary
    """
    if property_name not in data:
        return data
    
    names = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P1 if it doesn't exist
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    # Transform each name
    for name_obj in names:
        # Handle both simple string values and object values
        if isinstance(name_obj, dict):
            name_value = name_obj.get('@value', '')
            language = name_obj.get('@language', None)
        else:
            name_value = str(name_obj)
            language = None
        
        # Create appellation URI (use property name as suffix for uniqueness)
        appellation_uri = generate_appellation_uri(subject_uri, name_value, property_name)
        
        # Build P190 content
        p190_content = {'@value': name_value}
        if language:
            p190_content['@language'] = language
        
        # Create full CIDOC-CRM structure
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': aat_type_uri,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': [p190_content]
        }
        
        # Add to P1
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    # Remove shortcut property
    del data[property_name]
    
    return data

def transform_p1_1_has_name(data):
    """
    Transform gmn:P1_1_has_name to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (AAT 300404650) > P190_has_symbolic_content
    
    Note: This now applies to any E1_CRM_Entity, not just E21_Person.
    """
    return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)

def transform_p1_2_has_name_from_source(data):
    """
    Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (AAT 300456607) > P190_has_symbolic_content
    """
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)

def transform_p1_3_has_patrilineal_name(data):
    """
    Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (AAT 300404651) > P190_has_symbolic_content
    
    This captures patrilineal names that include patronymic ancestry chains,
    such as "Giacomo Spinola q. Antonio" (son of the late Antonio).
    """
    return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)

def transform_p1_4_has_loconym(data):
    """
    Transform gmn:P1_4_has_loconym to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (Wikidata Q17143070) > P67_refers_to > E53_Place
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P1_4_has_loconym' not in data:
        return data
    
    places = data['gmn:P1_4_has_loconym']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P1 if it doesn't exist
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    # Transform each place reference
    for place_obj in places:
        # Handle both URI references and objects
        if isinstance(place_obj, dict):
            place_uri = place_obj.get('@id', place_obj.get('@value', ''))
        else:
            place_uri = str(place_obj)
        
        # Create appellation URI
        place_hash = str(hash(place_uri + 'loconym'))[-8:]
        appellation_uri = f"{subject_uri}/appellation/loconym_{place_hash}"
        
        # Create full CIDOC-CRM structure
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': WIKIDATA_LOCONYM,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P67_refers_to': {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        }
        
        # Add to P1
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    # Remove shortcut property
    del data['gmn:P1_4_has_loconym']
    
    return data

def transform_p3_1_has_editorial_note(data, include_internal=False):
    """
    Transform gmn:P3_1_has_editorial_note to full CIDOC-CRM structure:
    P67i_is_referred_to_by > E33_Linguistic_Object > P2_has_type (AAT 300456627) > P190_has_symbolic_content
    
    Args:
        data: The item data dictionary
        include_internal: If False (default), removes editorial notes entirely. 
                         If True, transforms them to full CIDOC-CRM structure.
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P3_1_has_editorial_note' not in data:
        return data
    
    # If we're not including internal notes, just remove them
    if not include_internal:
        del data['gmn:P3_1_has_editorial_note']
        return data
    
    notes = data['gmn:P3_1_has_editorial_note']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P67i if it doesn't exist
    if 'cidoc:P67i_is_referred_to_by' not in data:
        data['cidoc:P67i_is_referred_to_by'] = []
    
    # Transform each note
    for note_obj in notes:
        # Handle both simple string values and object values
        if isinstance(note_obj, dict):
            note_value = note_obj.get('@value', '')
            language = note_obj.get('@language', None)
        else:
            note_value = str(note_obj)
            language = None
        
        # Create linguistic object URI
        note_hash = str(hash(note_value + 'editorial'))[-8:]
        linguistic_obj_uri = f"{subject_uri}/linguistic_object/{note_hash}"
        
        # Build P190 content
        p190_content = {'@value': note_value}
        if language:
            p190_content['@language'] = language
        
        # Create full CIDOC-CRM structure
        linguistic_object = {
            '@id': linguistic_obj_uri,
            '@type': 'cidoc:E33_Linguistic_Object',
            'cidoc:P2_has_type': {
                '@id': AAT_EDITORIAL_NOTE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': [p190_content]
        }
        
        # Add to P67i
        data['cidoc:P67i_is_referred_to_by'].append(linguistic_object)
    
    # Remove shortcut property
    del data['gmn:P3_1_has_editorial_note']
    
    return data

def transform_p11i_1_earliest_attestation_date(data):
    """
    Transform gmn:P11i_1_earliest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82a_begin_of_the_begin
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P11i_1_earliest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_1_earliest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P11i if it doesn't exist
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    # Transform each date
    for date_obj in dates:
        # Handle both simple string values and object values
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
            date_type = date_obj.get('@type', 'http://www.w3.org/2001/XMLSchema#date')
        else:
            date_value = str(date_obj)
            date_type = 'http://www.w3.org/2001/XMLSchema#date'
        
        # Create event and timespan URIs
        date_hash = str(hash(date_value + 'earliest'))[-8:]
        event_uri = f"{subject_uri}/event/earliest_attestation_{date_hash}"
        timespan_uri = f"{subject_uri}/timespan/earliest_attestation_{date_hash}"
        
        # Create full CIDOC-CRM structure
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82a_begin_of_the_begin': {
                    '@value': date_value,
                    '@type': date_type
                }
            }
        }
        
        # Add to P11i
        data['cidoc:P11i_participated_in'].append(event)
    
    # Remove shortcut property
    del data['gmn:P11i_1_earliest_attestation_date']
    
    return data

def transform_p11i_2_latest_attestation_date(data):
    """
    Transform gmn:P11i_2_latest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82b_end_of_the_end
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P11i if it doesn't exist
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    # Transform each date
    for date_obj in dates:
        # Handle both simple string values and object values
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
            date_type = date_obj.get('@type', 'http://www.w3.org/2001/XMLSchema#date')
        else:
            date_value = str(date_obj)
            date_type = 'http://www.w3.org/2001/XMLSchema#date'
        
        # Create event and timespan URIs
        date_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_attestation_{date_hash}"
        timespan_uri = f"{subject_uri}/timespan/latest_attestation_{date_hash}"
        
        # Create full CIDOC-CRM structure
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': {
                    '@value': date_value,
                    '@type': date_type
                }
            }
        }
        
        # Add to P11i
        data['cidoc:P11i_participated_in'].append(event)
    
    # Remove shortcut property
    del data['gmn:P11i_2_latest_attestation_date']
    
    return data

def transform_p11i_3_has_spouse(data):
    """
    Transform gmn:P11i_3_has_spouse to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event (marriage) > P11_had_participant > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P11i_3_has_spouse' not in data:
        return data
    
    spouses = data['gmn:P11i_3_has_spouse']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P11i if it doesn't exist
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    # Transform each spouse (each represents a separate marriage)
    for spouse_obj in spouses:
        # Handle both URI references and full objects
        if isinstance(spouse_obj, dict):
            spouse_uri = spouse_obj.get('@id', '')
            spouse_data = spouse_obj.copy()
            if '@type' not in spouse_data:
                spouse_data['@type'] = 'cidoc:E21_Person'
        else:
            spouse_uri = str(spouse_obj)
            spouse_data = {
                '@id': spouse_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Create marriage event URI
        spouse_hash = str(hash(spouse_uri + 'marriage'))[-8:]
        marriage_uri = f"{subject_uri}/marriage/{spouse_hash}"
        
        # Create full CIDOC-CRM structure
        marriage_event = {
            '@id': marriage_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P2_has_type': {
                '@id': AAT_MARRIAGE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P11_had_participant': [
                {
                    '@id': subject_uri,
                    '@type': 'cidoc:E21_Person'
                },
                spouse_data
            ]
        }
        
        # Add to P11i
        data['cidoc:P11i_participated_in'].append(marriage_event)
    
    # Remove shortcut property
    del data['gmn:P11i_3_has_spouse']
    
    return data

def transform_p22_1_has_owner(data):
    """
    Transform gmn:P22_1_has_owner to full CIDOC-CRM structure:
    P24i_changed_ownership_through > E8_Acquisition > P22_transferred_title_to > E21_Person
    
    Works for both buildings (gmn:E22_1_Building) and moveable property (gmn:E22_2_Moveable_Property).
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P22_1_has_owner' not in data:
        return data
    
    owners = data['gmn:P22_1_has_owner']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Determine the type of the object (building or moveable property)
    object_type = 'cidoc:E22_Human-Made_Object'
    if '@type' in data:
        if isinstance(data['@type'], list):
            if 'gmn:E22_1_Building' in data['@type']:
                object_type = 'gmn:E22_1_Building'
            elif 'gmn:E22_2_Moveable_Property' in data['@type']:
                object_type = 'gmn:E22_2_Moveable_Property'
        elif data['@type'] in ['gmn:E22_1_Building', 'gmn:E22_2_Moveable_Property']:
            object_type = data['@type']
    
    # Initialize P24i if it doesn't exist
    if 'cidoc:P24i_changed_ownership_through' not in data:
        data['cidoc:P24i_changed_ownership_through'] = []
    
    # Transform each owner (each represents a separate acquisition)
    for owner_obj in owners:
        # Handle both URI references and full objects
        if isinstance(owner_obj, dict):
            owner_uri = owner_obj.get('@id', '')
            owner_data = owner_obj.copy()
            if '@type' not in owner_data:
                owner_data['@type'] = 'cidoc:E21_Person'
        else:
            owner_uri = str(owner_obj)
            owner_data = {
                '@id': owner_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Create acquisition event URI
        owner_hash = str(hash(owner_uri + 'acquisition'))[-8:]
        acquisition_uri = f"{subject_uri}/acquisition/{owner_hash}"
        
        # Create full CIDOC-CRM structure
        acquisition_event = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P24_transferred_title_of': {
                '@id': subject_uri,
                '@type': object_type
            },
            'cidoc:P22_transferred_title_to': owner_data
        }
        
        # Add to P24i
        data['cidoc:P24i_changed_ownership_through'].append(acquisition_event)
    
    # Remove shortcut property
    del data['gmn:P22_1_has_owner']
    
    return data

def transform_p53_1_has_occupant(data):
    """
    Transform gmn:P53_1_has_occupant to full CIDOC-CRM structure:
    P53i_is_former_or_current_location_of > E9_Move > P25_moved > E21_Person
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P53_1_has_occupant' not in data:
        return data
    
    occupants = data['gmn:P53_1_has_occupant']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P53i if it doesn't exist
    if 'ci