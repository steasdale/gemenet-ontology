# Python Additions for gmn:P11i_2_latest_attestation_date
# Ready-to-copy Python code for gmn_to_cidoc_transform.py

## STATUS: ✅ ALREADY IMPLEMENTED
## This file contains the CURRENT transformation function for reference

---

## Complete Transformation Function

```python
def transform_p11i_2_latest_attestation_date(data):
    """
    Transform gmn:P11i_2_latest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82b_end_of_the_end
    """
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for date_obj in dates:
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        if not date_value:
            continue
        
        event_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_2_latest_attestation_date']
    return data
```

---

## Required Imports

```python
from uuid import uuid4
import json
```

**Note:** These should already be at the top of `gmn_to_cidoc_transform.py`

---

## Integration in transform_item()

Add function call in the main transformation pipeline:

```python
def transform_item(data, include_internal=False):
    """Transform a single JSON-LD item from GMN to CIDOC-CRM format."""
    
    # ... earlier transformations ...
    
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)  # ← Add this line
    item = transform_p11i_3_has_spouse(item)
    
    # ... later transformations ...
    
    return item
```

**Location:** After `transform_p11i_1_earliest_attestation_date` and before `transform_p11i_3_has_spouse`

---

## Function Breakdown with Annotations

```python
def transform_p11i_2_latest_attestation_date(data):
    """
    Transform gmn:P11i_2_latest_attestation_date to full CIDOC-CRM structure.
    
    Args:
        data (dict): JSON-LD item containing person data
        
    Returns:
        dict: Modified JSON-LD item with expanded CIDOC-CRM structure
        
    Transformation:
        INPUT:  gmn:P11i_2_latest_attestation_date: "1595-08-20"
        OUTPUT: cidoc:P11i_participated_in → E5_Event → P4_has_time-span 
                → E52_Time-Span → P82b_end_of_the_end: "1595-08-20"
    """
    
    # Step 1: Check if property exists
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        return data  # Nothing to transform, return unchanged
    
    # Step 2: Extract date values and subject URI
    dates = data['gmn:P11i_2_latest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Initialize P11i_participated_in array if needed
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    # Step 4: Process each date value
    for date_obj in dates:
        # Handle both JSON-LD objects and simple strings
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        # Skip empty dates
        if not date_value:
            continue
        
        # Step 5: Generate deterministic URIs
        event_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        # Step 6: Build CIDOC-CRM event structure
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': date_value
            }
        }
        
        # Step 7: Add event to participation array
        data['cidoc:P11i_participated_in'].append(event)
    
    # Step 8: Remove simplified property
    del data['gmn:P11i_2_latest_attestation_date']
    
    return data
```

---

## Alternative Implementation: With Logging

```python
def transform_p11i_2_latest_attestation_date(data, verbose=False):
    """
    Transform gmn:P11i_2_latest_attestation_date with optional logging.
    """
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        if verbose:
            print("  [P11i_2] Property not found, skipping")
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if verbose:
        print(f"  [P11i_2] Transforming {len(dates)} latest attestation date(s)")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for i, date_obj in enumerate(dates):
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        if not date_value:
            if verbose:
                print(f"  [P11i_2] Skipping empty date at index {i}")
            continue
        
        event_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        if verbose:
            print(f"  [P11i_2] Creating event {event_uri} for date {date_value}")
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_2_latest_attestation_date']
    
    if verbose:
        print(f"  [P11i_2] Transformation complete")
    
    return data
```

---

## Unit Tests

```python
import unittest
from uuid import uuid4

class TestLatestAttestationTransform(unittest.TestCase):
    
    def test_single_date(self):
        """Test transformation of single date value."""
        input_data = {
            "@id": "person:p001",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
        }
        
        result = transform_p11i_2_latest_attestation_date(input_data)
        
        # Check property was removed
        self.assertNotIn("gmn:P11i_2_latest_attestation_date", result)
        
        # Check CIDOC structure was created
        self.assertIn("cidoc:P11i_participated_in", result)
        self.assertEqual(len(result["cidoc:P11i_participated_in"]), 1)
        
        # Check event structure
        event = result["cidoc:P11i_participated_in"][0]
        self.assertEqual(event["@type"], "cidoc:E5_Event")
        self.assertIn("cidoc:P4_has_time-span", event)
        
        # Check timespan structure
        timespan = event["cidoc:P4_has_time-span"]
        self.assertEqual(timespan["@type"], "cidoc:E52_Time-Span")
        self.assertEqual(timespan["cidoc:P82b_end_of_the_end"], "1595-08-20")
    
    def test_multiple_dates(self):
        """Test transformation of multiple date values."""
        input_data = {
            "@id": "person:p002",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": [
                "1590-03-15",
                "1595-08-20"
            ]
        }
        
        result = transform_p11i_2_latest_attestation_date(input_data)
        
        # Check multiple events created
        self.assertEqual(len(result["cidoc:P11i_participated_in"]), 2)
        
        # Check URIs are different
        uri1 = result["cidoc:P11i_participated_in"][0]["@id"]
        uri2 = result["cidoc:P11i_participated_in"][1]["@id"]
        self.assertNotEqual(uri1, uri2)
    
    def test_jsonld_date_object(self):
        """Test transformation of JSON-LD date object."""
        input_data = {
            "@id": "person:p003",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": [
                {"@value": "1595-08-20", "@type": "xsd:date"}
            ]
        }
        
        result = transform_p11i_2_latest_attestation_date(input_data)
        
        # Check date value extracted correctly
        timespan = result["cidoc:P11i_participated_in"][0]["cidoc:P4_has_time-span"]
        self.assertEqual(timespan["cidoc:P82b_end_of_the_end"], "1595-08-20")
    
    def test_missing_property(self):
        """Test handling when property is not present."""
        input_data = {
            "@id": "person:p004",
            "@type": "cidoc:E21_Person",
            "gmn:P1_1_has_name": "Test Person"
        }
        
        result = transform_p11i_2_latest_attestation_date(input_data)
        
        # Check data unchanged
        self.assertEqual(result, input_data)
        self.assertNotIn("cidoc:P11i_participated_in", result)
    
    def test_empty_date(self):
        """Test handling of empty date value."""
        input_data = {
            "@id": "person:p005",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": [""]
        }
        
        result = transform_p11i_2_latest_attestation_date(input_data)
        
        # Check property removed but no events created
        self.assertNotIn("gmn:P11i_2_latest_attestation_date", result)
        
        # P11i array may exist but should be empty
        if "cidoc:P11i_participated_in" in result:
            self.assertEqual(len(result["cidoc:P11i_participated_in"]), 0)
    
    def test_uri_generation(self):
        """Test that URIs are deterministic."""
        input_data1 = {
            "@id": "person:p006",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
        }
        
        input_data2 = {
            "@id": "person:p006",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
        }
        
        result1 = transform_p11i_2_latest_attestation_date(input_data1)
        result2 = transform_p11i_2_latest_attestation_date(input_data2)
        
        # Same input should produce same URIs
        uri1 = result1["cidoc:P11i_participated_in"][0]["@id"]
        uri2 = result2["cidoc:P11i_participated_in"][0]["@id"]
        self.assertEqual(uri1, uri2)
    
    def test_coexistence_with_earliest(self):
        """Test that latest works alongside earliest attestation."""
        input_data = {
            "@id": "person:p007",
            "@type": "cidoc:E21_Person",
            "gmn:P11i_1_earliest_attestation_date": ["1580-01-10"],
            "gmn:P11i_2_latest_attestation_date": ["1595-08-20"]
        }
        
        # Transform both
        result = transform_p11i_1_earliest_attestation_date(input_data)
        result = transform_p11i_2_latest_attestation_date(result)
        
        # Should have two events
        self.assertEqual(len(result["cidoc:P11i_participated_in"]), 2)
        
        # Check one has P82a and one has P82b
        timespans = [
            e["cidoc:P4_has_time-span"] 
            for e in result["cidoc:P11i_participated_in"]
        ]
        has_earliest = any("cidoc:P82a_begin_of_the_begin" in ts for ts in timespans)
        has_latest = any("cidoc:P82b_end_of_the_end" in ts for ts in timespans)
        
        self.assertTrue(has_earliest)
        self.assertTrue(has_latest)

if __name__ == '__main__':
    unittest.main()
```

---

## Usage Examples

### Example 1: Transform Single Record

```python
# Input data
person_data = {
    "@id": "person:francesco_corner",
    "@type": "cidoc:E21_Person",
    "gmn:P1_1_has_name": "Francesco Corner",
    "gmn:P11i_2_latest_attestation_date": "1592-06-15"
}

# Transform
result = transform_p11i_2_latest_attestation_date(person_data)

# Output
print(json.dumps(result, indent=2))
```

### Example 2: Transform File

```python
def transform_file(input_path, output_path):
    """Transform an entire JSON-LD file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle array of items
    if isinstance(data, list):
        transformed = [
            transform_p11i_2_latest_attestation_date(item) 
            for item in data
        ]
    # Handle single item
    elif isinstance(data, dict):
        if '@graph' in data:
            data['@graph'] = [
                transform_p11i_2_latest_attestation_date(item)
                for item in data['@graph']
            ]
            transformed = data
        else:
            transformed = transform_p11i_2_latest_attestation_date(data)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Transformed {input_path} → {output_path}")

# Usage
transform_file('persons_gmn.json', 'persons_cidoc.json')
```

### Example 3: Batch Processing

```python
def batch_transform_latest_attestations(items):
    """Transform latest attestation dates for multiple items."""
    results = []
    
    for item in items:
        try:
            transformed = transform_p11i_2_latest_attestation_date(item)
            results.append(transformed)
        except Exception as e:
            print(f"Error transforming {item.get('@id', 'unknown')}: {e}")
            results.append(item)  # Keep original on error
    
    return results

# Usage
persons = [...]  # List of person records
transformed_persons = batch_transform_latest_attestations(persons)
```

---

## Performance Considerations

### Time Complexity

- **Best Case:** O(1) - Property not present
- **Average Case:** O(n) where n = number of dates
- **Worst Case:** O(n) where n = number of dates

### Space Complexity

- O(n) additional space for n date values (event structures)

### Optimization Tips

1. **For Large Datasets:**
   ```python
   # Process in chunks to manage memory
   def transform_chunked(items, chunk_size=1000):
       for i in range(0, len(items), chunk_size):
           chunk = items[i:i+chunk_size]
           yield [transform_p11i_2_latest_attestation_date(item) for item in chunk]
   ```

2. **For Repeated Transformations:**
   ```python
   # Cache hash results if processing same dates frequently
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def generate_event_hash(date_value):
       return str(hash(date_value + 'latest'))[-8:]
   ```

---

## Error Handling

### Enhanced Version with Error Handling

```python
def transform_p11i_2_latest_attestation_date(data):
    """
    Transform gmn:P11i_2_latest_attestation_date with comprehensive error handling.
    """
    try:
        if 'gmn:P11i_2_latest_attestation_date' not in data:
            return data
        
        dates = data['gmn:P11i_2_latest_attestation_date']
        
        # Validate dates is a list
        if not isinstance(dates, list):
            dates = [dates]
        
        subject_uri = data.get('@id')
        if not subject_uri:
            # Generate UUID if no ID present
            subject_uri = f"urn:uuid:{uuid4()}"
            data['@id'] = subject_uri
        
        if 'cidoc:P11i_participated_in' not in data:
            data['cidoc:P11i_participated_in'] = []
        
        for date_obj in dates:
            try:
                if isinstance(date_obj, dict):
                    date_value = date_obj.get('@value', '')
                else:
                    date_value = str(date_obj)
                
                if not date_value or date_value.strip() == '':
                    continue
                
                # Validate date format (basic check)
                date_value = date_value.strip()
                
                event_hash = str(hash(date_value + 'latest'))[-8:]
                event_uri = f"{subject_uri}/event/latest_{event_hash}"
                timespan_uri = f"{event_uri}/timespan"
                
                event = {
                    '@id': event_uri,
                    '@type': 'cidoc:E5_Event',
                    'cidoc:P4_has_time-span': {
                        '@id': timespan_uri,
                        '@type': 'cidoc:E52_Time-Span',
                        'cidoc:P82b_end_of_the_end': date_value
                    }
                }
                
                data['cidoc:P11i_participated_in'].append(event)
                
            except Exception as e:
                print(f"Warning: Error processing date {date_obj}: {e}")
                continue
        
        del data['gmn:P11i_2_latest_attestation_date']
        return data
        
    except Exception as e:
        print(f"Error in transform_p11i_2_latest_attestation_date: {e}")
        return data  # Return original data on error
```

---

## Debugging Tips

### Debug Print Function

```python
def transform_p11i_2_latest_attestation_date_debug(data):
    """Version with detailed debug output."""
    print(f"\n=== P11i_2 Transformation Debug ===")
    print(f"Input data ID: {data.get('@id', 'NO ID')}")
    
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        print("Property not found in data")
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
    print(f"Found {len(dates)} date(s): {dates}")
    
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    print(f"Subject URI: {subject_uri}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
        print("Created P11i_participated_in array")
    else:
        print(f"P11i_participated_in already has {len(data['cidoc:P11i_participated_in'])} events")
    
    for i, date_obj in enumerate(dates):
        print(f"\nProcessing date {i}:")
        print(f"  Type: {type(date_obj)}")
        print(f"  Value: {date_obj}")
        
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
            print(f"  Extracted from dict: '{date_value}'")
        else:
            date_value = str(date_obj)
            print(f"  Converted to string: '{date_value}'")
        
        if not date_value:
            print("  SKIPPED: Empty date")
            continue
        
        event_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        print(f"  Generated hash: {event_hash}")
        print(f"  Event URI: {event_uri}")
        print(f"  Timespan URI: {timespan_uri}")
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
        print("  Event added to P11i_participated_in")
    
    del data['gmn:P11i_2_latest_attestation_date']
    print("\nSimplified property removed")
    print(f"Final P11i_participated_in count: {len(data['cidoc:P11i_participated_in'])}")
    print("=== End Debug ===\n")
    
    return data
```

---

## Summary

This file provides:
- ✅ Complete transformation function code
- ✅ Integration instructions
- ✅ Comprehensive unit tests
- ✅ Usage examples
- ✅ Performance considerations
- ✅ Error handling patterns
- ✅ Debugging utilities

**Status:** Function is fully implemented in `gmn_to_cidoc_transform.py`  
**Action Required:** None - reference only

For new implementations, copy the function and add the call to `transform_item()`.
