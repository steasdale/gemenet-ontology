# Implementation Guide: P46i.1 Is Contained In
## Step-by-Step Instructions for GMN Ontology Integration

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Ontology Implementation](#ontology-implementation)
4. [Python Transformation Implementation](#python-transformation-implementation)
5. [Testing Procedures](#testing-procedures)
6. [Integration Checklist](#integration-checklist)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides complete instructions for implementing the `gmn:P46i_1_is_contained_in` property in the GMN ontology ecosystem. This property enables documents to reference their containing archival units.

**Implementation Type**: Direct property mapping (no intermediate nodes)
**Estimated Time**: 30-45 minutes
**Difficulty Level**: Beginner to Intermediate

---

## Prerequisites

### Required Files
- `gmn_ontology.ttl` - Main ontology file
- `gmn_to_cidoc_transform.py` - Transformation script

### Required Knowledge
- Basic understanding of RDF/Turtle syntax
- Basic Python programming
- Familiarity with CIDOC-CRM structure
- Understanding of archival concepts

### Required Tools
- Text editor or IDE
- Python 3.7 or higher
- RDFLib library (`pip install rdflib`)
- Access to GMN ontology repository

---

## Ontology Implementation

### Step 1: Verify Property Definition

**Status Check**: The property is already defined in `gmn_ontology.ttl`. Verify it exists:

```bash
grep -A 10 "P46i_1_is_contained_in" gmn_ontology.ttl
```

**Expected Output**:
```turtle
gmn:P46i_1_is_contained_in
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P46i.1 is contained in"@en ;
    rdfs:comment "Simplified property for expressing that a document forms part of a larger archival unit or collection. Use this to link individual contracts to the registers, filze (bundles of contracts tied with string), folders, or other archival containers in which they are physically housed. This represents the direct CIDOC-CRM property P46i_forms_part_of. The range can be any archival unit or collection, including registers (E31_Document subtype), filze, folders, or institutional archives. This captures the archival context and provenance of individual documents."@en ;
    rdfs:subPropertyOf cidoc:P46i_forms_part_of ;
    rdfs:domain cidoc:E31_Document ;
    rdfs:range cidoc:E78_Curated_Holding ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P46i_forms_part_of .
```

✅ **If present**: Continue to Python implementation
❌ **If missing**: Add the definition from `is-contained-in-ontology.ttl`

### Step 2: Validate Ontology Syntax

```python
from rdflib import Graph

g = Graph()
try:
    g.parse("gmn_ontology.ttl", format="turtle")
    print("✓ Ontology syntax valid")
except Exception as e:
    print(f"✗ Syntax error: {e}")
```

---

## Python Transformation Implementation

### Step 3: Locate Transformation Function Section

Open `gmn_to_cidoc_transform.py` and find the section with direct property mappings. Look for functions like:
- `transform_p1_1_has_name()`
- `transform_p102_1_has_title()`
- Other direct mapping functions

### Step 4: Add Transformation Function

**Location**: Add after other direct mapping functions (around line 200-300)

**Copy this code**:

```python
def transform_p46i_1_is_contained_in(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> Graph:
    """
    Transform gmn:P46i_1_is_contained_in to cidoc:P46i_forms_part_of.
    
    This is a direct property mapping with no intermediate nodes.
    Links documents to their containing archival units.
    
    Pattern:
        Input:  ?doc gmn:P46i_1_is_contained_in ?container
        Output: ?doc cidoc:P46i_forms_part_of ?container
    
    Args:
        graph: RDF graph containing GMN data
        gmn_ns: GMN namespace
        cidoc_ns: CIDOC-CRM namespace
    
    Returns:
        Modified graph with CIDOC-CRM compliant structure
    """
    # Find all uses of P46i_1_is_contained_in
    triples_to_transform = list(graph.triples((None, gmn_ns.P46i_1_is_contained_in, None)))
    
    for subject, predicate, obj in triples_to_transform:
        # Remove the shortcut property
        graph.remove((subject, predicate, obj))
        
        # Add the CIDOC-CRM property
        graph.add((subject, cidoc_ns.P46i_forms_part_of, obj))
    
    if triples_to_transform:
        print(f"  ✓ Transformed {len(triples_to_transform)} P46i_1_is_contained_in statement(s)")
    
    return graph
```

### Step 5: Register Function in Main Transform

Find the `transform_all()` or main transformation function. Add the function call:

```python
def transform_all(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> Graph:
    """Main transformation orchestrator."""
    
    # ... existing transformations ...
    
    # Direct property mappings
    graph = transform_p1_1_has_name(graph, gmn_ns, cidoc_ns)
    graph = transform_p102_1_has_title(graph, gmn_ns, cidoc_ns)
    graph = transform_p46i_1_is_contained_in(graph, gmn_ns, cidoc_ns)  # ADD THIS LINE
    
    # ... more transformations ...
    
    return graph
```

### Step 6: Add to Property Registry (Optional)

If your script maintains a property registry for documentation:

```python
DIRECT_MAPPING_PROPERTIES = {
    'P1_1_has_name': 'P1_is_identified_by',
    'P102_1_has_title': 'P102_has_title',
    'P46i_1_is_contained_in': 'P46i_forms_part_of',  # ADD THIS LINE
    # ... other mappings ...
}
```

---

## Testing Procedures

### Step 7: Create Test Data

Create a test file `test_p46i_1.ttl`:

```turtle
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/contracts/test_contract_001> 
    a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Test Sales Contract"@en ;
    gmn:P46i_1_is_contained_in <http://example.org/archives/register_1450> .

<http://example.org/archives/register_1450>
    a cidoc:E31_Document ;
    a cidoc:E78_Curated_Holding ;
    gmn:P1_1_has_name "Notarial Register 1450"@en .
```

### Step 8: Run Transformation

```python
from rdflib import Graph, Namespace

# Load test data
g = Graph()
g.parse("test_p46i_1.ttl", format="turtle")

# Define namespaces
GMN = Namespace("http://www.genoesemerchantnetworks.com/ontology#")
CIDOC = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

# Run transformation
g = transform_p46i_1_is_contained_in(g, GMN, CIDOC)

# Serialize result
print(g.serialize(format="turtle"))
```

### Step 9: Verify Output

**Expected Output**:
```turtle
<http://example.org/contracts/test_contract_001> 
    a gmn:E31_2_Sales_Contract ;
    cidoc:P1_is_identified_by <http://example.org/contracts/test_contract_001/appellation/1> ;
    cidoc:P46i_forms_part_of <http://example.org/archives/register_1450> .  # TRANSFORMED!

<http://example.org/archives/register_1450>
    a cidoc:E31_Document ;
    a cidoc:E78_Curated_Holding ;
    cidoc:P1_is_identified_by <http://example.org/archives/register_1450/appellation/1> .
```

**Verification Checklist**:
- ✅ `gmn:P46i_1_is_contained_in` has been removed
- ✅ `cidoc:P46i_forms_part_of` has been added with same subject and object
- ✅ No intermediate nodes created (direct mapping)
- ✅ Container entity remains unchanged

### Step 10: Test Edge Cases

#### Test 10.1: Multiple Containment

```turtle
<http://example.org/contracts/multi_container>
    a gmn:E31_2_Sales_Contract ;
    gmn:P46i_1_is_contained_in <http://example.org/archives/register_A> ;
    gmn:P46i_1_is_contained_in <http://example.org/archives/filza_B> .
```

**Expected**: Both containment relationships transformed correctly.

#### Test 10.2: Different Document Types

```turtle
<http://example.org/letters/letter_001>
    a gmn:E31_6_Correspondence ;
    gmn:P46i_1_is_contained_in <http://example.org/archives/letterbook> .

<http://example.org/wills/will_001>
    a cidoc:E31_Document ;
    gmn:P46i_1_is_contained_in <http://example.org/archives/will_register> .
```

**Expected**: Works for all E31_Document subtypes.

#### Test 10.3: No Containment

```turtle
<http://example.org/contracts/orphan_contract>
    a gmn:E31_2_Sales_Contract ;
    gmn:P1_1_has_name "Orphan Contract"@en .
```

**Expected**: Document remains unchanged, no errors thrown.

### Step 11: SPARQL Query Testing

Test with SPARQL to verify proper transformation:

```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

# Should return 0 results (all shortcut properties transformed)
SELECT ?doc ?container
WHERE {
    ?doc gmn:P46i_1_is_contained_in ?container .
}

# Should return all containment relationships
SELECT ?doc ?container
WHERE {
    ?doc cidoc:P46i_forms_part_of ?container .
}
```

---

## Integration Checklist

### Pre-Implementation
- [ ] Backup current ontology and transformation files
- [ ] Review semantic documentation
- [ ] Verify CIDOC-CRM P46i_forms_part_of documentation
- [ ] Understand archival context requirements

### Ontology Integration
- [ ] Property definition present in `gmn_ontology.ttl`
- [ ] Syntax validation passed
- [ ] Property metadata complete (label, comment, domain, range)
- [ ] Superproperty relationship correct

### Python Integration
- [ ] Transformation function added
- [ ] Function registered in main transform
- [ ] Proper namespace handling
- [ ] Error handling implemented
- [ ] Logging/progress messages included

### Testing
- [ ] Basic transformation test passed
- [ ] Multiple containment test passed
- [ ] Different document types test passed
- [ ] Edge cases handled correctly
- [ ] SPARQL queries return expected results
- [ ] No regression in existing functionality

### Documentation
- [ ] Added to property catalog
- [ ] Usage examples documented
- [ ] Transformation pattern documented
- [ ] Added to user guide

### Deployment
- [ ] Code reviewed
- [ ] Version control committed
- [ ] Testing environment validated
- [ ] Production deployment planned

---

## Troubleshooting

### Problem: Syntax Error in Ontology

**Symptoms**: Parser fails to load ontology file

**Solution**:
```python
from rdflib import Graph
g = Graph()
try:
    g.parse("gmn_ontology.ttl", format="turtle")
except Exception as e:
    print(f"Error at: {e}")
    # Check for missing prefixes, unclosed strings, etc.
```

### Problem: Transformation Not Applied

**Symptoms**: Shortcut property still present after transformation

**Checklist**:
1. ✓ Function defined correctly?
2. ✓ Function called in main transform?
3. ✓ Namespaces defined correctly?
4. ✓ Graph passed by reference?

**Debug**:
```python
def transform_p46i_1_is_contained_in(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> Graph:
    triples = list(graph.triples((None, gmn_ns.P46i_1_is_contained_in, None)))
    print(f"DEBUG: Found {len(triples)} triples to transform")
    for s, p, o in triples:
        print(f"DEBUG: Transforming {s} -> {o}")
    # ... rest of function
```

### Problem: Wrong Property Applied

**Symptoms**: Incorrect CIDOC-CRM property in output

**Check**: Verify you're using `cidoc:P46i_forms_part_of` (not `P46_forms_part_of`)

**Correct**:
```python
graph.add((subject, cidoc_ns.P46i_forms_part_of, obj))
```

### Problem: Container Not Recognized

**Symptoms**: Range validation fails

**Solution**: Ensure container is properly typed:
```turtle
<http://example.org/archives/register>
    a cidoc:E78_Curated_Holding .  # Or more specific subclass
```

### Problem: Multiple Containers Cause Issues

**Symptoms**: Only one containment relationship transformed

**Solution**: The code handles this correctly. Verify:
```python
triples_to_transform = list(graph.triples((None, gmn_ns.P46i_1_is_contained_in, None)))
# This gets ALL triples, not just first one
```

---

## Performance Considerations

### Efficiency Notes

- **Direct mapping**: O(n) where n = number of P46i_1 triples
- **Memory**: Minimal overhead, no new nodes created
- **Best practice**: Process in batches for large datasets

### Large Dataset Optimization

```python
def transform_p46i_1_is_contained_in_batch(graph: Graph, gmn_ns: Namespace, 
                                           cidoc_ns: Namespace, batch_size: int = 1000) -> Graph:
    """Batch processing version for large datasets."""
    triples = list(graph.triples((None, gmn_ns.P46i_1_is_contained_in, None)))
    
    for i in range(0, len(triples), batch_size):
        batch = triples[i:i + batch_size]
        for subject, predicate, obj in batch:
            graph.remove((subject, predicate, obj))
            graph.add((subject, cidoc_ns.P46i_forms_part_of, obj))
        
        print(f"  ✓ Processed batch {i//batch_size + 1} ({len(batch)} triples)")
    
    return graph
```

---

## Next Steps

After successful implementation:

1. **Update Documentation**: Add property to main documentation using `is-contained-in-doc-note.txt`
2. **Training**: Brief team on new property usage
3. **Data Migration**: Transform existing data if needed
4. **Monitoring**: Track usage and issues in production
5. **Feedback**: Collect user feedback on property utility

---

## Additional Resources

- **CIDOC-CRM Documentation**: http://www.cidoc-crm.org/
- **P46i_forms_part_of Specification**: [CIDOC-CRM Definition]
- **Archival Standards**: ISAD(G), EAD, Dublin Core
- **GMN Ontology Repository**: [Your repository URL]

---

**Implementation Complete?** ✅ 

Move on to updating your main documentation with content from `is-contained-in-doc-note.txt`!
