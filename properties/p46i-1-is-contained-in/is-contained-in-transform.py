# Python Transformation Code for P46i.1 Is Contained In
# Add this to gmn_to_cidoc_transform.py

"""
This file contains the transformation function for gmn:P46i_1_is_contained_in property.
This is a DIRECT PROPERTY MAPPING - no intermediate nodes are created.
"""

# ==============================================================================
# MAIN TRANSFORMATION FUNCTION
# ==============================================================================

def transform_p46i_1_is_contained_in(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> Graph:
    """
    Transform gmn:P46i_1_is_contained_in to cidoc:P46i_forms_part_of.
    
    This is a direct property mapping with no intermediate nodes.
    Links documents to their containing archival units (registers, filze, folders, archives).
    
    Transformation Pattern:
    ---------------------
    Input:  ?doc gmn:P46i_1_is_contained_in ?container
    Output: ?doc cidoc:P46i_forms_part_of ?container
    
    No intermediate nodes are created.
    
    Args:
        graph: RDF graph containing GMN data
        gmn_ns: GMN namespace (http://www.genoesemerchantnetworks.com/ontology#)
        cidoc_ns: CIDOC-CRM namespace (http://www.cidoc-crm.org/cidoc-crm/)
    
    Returns:
        Modified graph with CIDOC-CRM compliant structure
    
    Examples:
        >>> # Input
        >>> <contract_001> gmn:P46i_1_is_contained_in <register_1450> .
        >>> 
        >>> # Output
        >>> <contract_001> cidoc:P46i_forms_part_of <register_1450> .
    
    Usage:
        from rdflib import Graph, Namespace
        
        g = Graph()
        g.parse("data.ttl", format="turtle")
        
        GMN = Namespace("http://www.genoesemerchantnetworks.com/ontology#")
        CIDOC = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        
        g = transform_p46i_1_is_contained_in(g, GMN, CIDOC)
    """
    # Find all uses of P46i_1_is_contained_in
    triples_to_transform = list(graph.triples((None, gmn_ns.P46i_1_is_contained_in, None)))
    
    for subject, predicate, obj in triples_to_transform:
        # Remove the GMN shortcut property
        graph.remove((subject, predicate, obj))
        
        # Add the CIDOC-CRM property
        graph.add((subject, cidoc_ns.P46i_forms_part_of, obj))
    
    # Log transformation results
    if triples_to_transform:
        print(f"  ✓ Transformed {len(triples_to_transform)} P46i_1_is_contained_in statement(s)")
    
    return graph


# ==============================================================================
# INTEGRATION INSTRUCTIONS
# ==============================================================================

"""
STEP 1: Add this function to your gmn_to_cidoc_transform.py file
---------------------------------------------------------------
Copy the transform_p46i_1_is_contained_in() function above and paste it into your
transformation script, typically in the section with other direct property mappings.

Recommended location: After other simple mapping functions like:
- transform_p1_1_has_name()
- transform_p102_1_has_title()
- transform_p138i_1_has_representation()


STEP 2: Register in main transformation function
------------------------------------------------
Add a call to this function in your main transformation orchestrator:

def transform_all(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> Graph:
    '''Main transformation orchestrator.'''
    
    print("Starting GMN to CIDOC-CRM transformation...")
    
    # Direct property mappings
    print("\\nTransforming direct property mappings...")
    graph = transform_p1_1_has_name(graph, gmn_ns, cidoc_ns)
    graph = transform_p102_1_has_title(graph, gmn_ns, cidoc_ns)
    graph = transform_p46i_1_is_contained_in(graph, gmn_ns, cidoc_ns)  # ADD THIS LINE
    
    # Complex property transformations
    print("\\nTransforming complex properties...")
    # ... other transformations ...
    
    return graph


STEP 3: Test the transformation
-------------------------------
Run the test code below to verify correct implementation.
"""


# ==============================================================================
# TESTING CODE
# ==============================================================================

def test_p46i_1_transformation():
    """
    Test function for P46i_1_is_contained_in transformation.
    Run this to verify the transformation works correctly.
    """
    from rdflib import Graph, Namespace, Literal
    from rdflib.namespace import RDF, RDFS, XSD
    
    # Setup
    print("=" * 70)
    print("TESTING P46i.1 Is Contained In Transformation")
    print("=" * 70)
    
    g = Graph()
    GMN = Namespace("http://www.genoesemerchantnetworks.com/ontology#")
    CIDOC = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
    EX = Namespace("http://example.org/")
    
    g.bind("gmn", GMN)
    g.bind("cidoc", CIDOC)
    g.bind("ex", EX)
    
    # Test Case 1: Single containment
    print("\nTest Case 1: Single document in register")
    print("-" * 70)
    
    g.add((EX.contract_001, RDF.type, GMN.E31_2_Sales_Contract))
    g.add((EX.contract_001, GMN.P1_1_has_name, Literal("Test Contract", lang="en")))
    g.add((EX.contract_001, GMN.P46i_1_is_contained_in, EX.register_1450))
    
    g.add((EX.register_1450, RDF.type, CIDOC.E31_Document))
    g.add((EX.register_1450, RDF.type, CIDOC.E78_Curated_Holding))
    g.add((EX.register_1450, GMN.P1_1_has_name, Literal("Register 1450", lang="en")))
    
    print("Input:")
    for s, p, o in g.triples((EX.contract_001, GMN.P46i_1_is_contained_in, None)):
        print(f"  {s} {p} {o}")
    
    # Transform
    g = transform_p46i_1_is_contained_in(g, GMN, CIDOC)
    
    print("\nOutput:")
    for s, p, o in g.triples((EX.contract_001, CIDOC.P46i_forms_part_of, None)):
        print(f"  {s} {p} {o}")
    
    # Verify
    assert (EX.contract_001, CIDOC.P46i_forms_part_of, EX.register_1450) in g
    assert (EX.contract_001, GMN.P46i_1_is_contained_in, EX.register_1450) not in g
    print("✓ Test passed!")
    
    # Test Case 2: Multiple containment levels
    print("\n\nTest Case 2: Hierarchical containment (contract → filza → busta)")
    print("-" * 70)
    
    g.add((EX.contract_002, RDF.type, GMN.E31_2_Sales_Contract))
    g.add((EX.contract_002, GMN.P46i_1_is_contained_in, EX.filza_23))
    
    g.add((EX.filza_23, RDF.type, CIDOC.E78_Curated_Holding))
    g.add((EX.filza_23, GMN.P46i_1_is_contained_in, EX.busta_5))
    
    g.add((EX.busta_5, RDF.type, CIDOC.E78_Curated_Holding))
    
    print("Input:")
    for s, p, o in g.triples((None, GMN.P46i_1_is_contained_in, None)):
        print(f"  {s} {p} {o}")
    
    # Transform
    g = transform_p46i_1_is_contained_in(g, GMN, CIDOC)
    
    print("\nOutput:")
    for s, p, o in g.triples((None, CIDOC.P46i_forms_part_of, None)):
        if s in [EX.contract_002, EX.filza_23]:  # Only show relevant triples
            print(f"  {s} {p} {o}")
    
    # Verify
    assert (EX.contract_002, CIDOC.P46i_forms_part_of, EX.filza_23) in g
    assert (EX.filza_23, CIDOC.P46i_forms_part_of, EX.busta_5) in g
    assert (EX.contract_002, GMN.P46i_1_is_contained_in, EX.filza_23) not in g
    print("✓ Test passed!")
    
    # Test Case 3: Multiple documents in same container
    print("\n\nTest Case 3: Multiple documents in same container")
    print("-" * 70)
    
    g.add((EX.contract_003, RDF.type, GMN.E31_2_Sales_Contract))
    g.add((EX.contract_003, GMN.P46i_1_is_contained_in, EX.register_1451))
    
    g.add((EX.contract_004, RDF.type, GMN.E31_2_Sales_Contract))
    g.add((EX.contract_004, GMN.P46i_1_is_contained_in, EX.register_1451))
    
    g.add((EX.register_1451, RDF.type, CIDOC.E78_Curated_Holding))
    
    print("Input:")
    for s, p, o in g.triples((None, GMN.P46i_1_is_contained_in, EX.register_1451)):
        print(f"  {s} {p} {o}")
    
    # Transform
    g = transform_p46i_1_is_contained_in(g, GMN, CIDOC)
    
    print("\nOutput:")
    for s, p, o in g.triples((None, CIDOC.P46i_forms_part_of, EX.register_1451)):
        print(f"  {s} {p} {o}")
    
    # Verify
    assert (EX.contract_003, CIDOC.P46i_forms_part_of, EX.register_1451) in g
    assert (EX.contract_004, CIDOC.P46i_forms_part_of, EX.register_1451) in g
    print("✓ Test passed!")
    
    # Test Case 4: No containment (should not break)
    print("\n\nTest Case 4: Document without containment")
    print("-" * 70)
    
    g.add((EX.orphan_contract, RDF.type, GMN.E31_2_Sales_Contract))
    g.add((EX.orphan_contract, GMN.P1_1_has_name, Literal("Orphan Contract", lang="en")))
    
    print("Input: Document with no P46i_1_is_contained_in")
    
    # Transform (should not error)
    g = transform_p46i_1_is_contained_in(g, GMN, CIDOC)
    
    print("Output: Document unchanged, no errors")
    
    # Verify no containment added
    assert len(list(g.triples((EX.orphan_contract, CIDOC.P46i_forms_part_of, None)))) == 0
    print("✓ Test passed!")
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
    
    return g


# ==============================================================================
# SPARQL VERIFICATION QUERIES
# ==============================================================================

def verify_transformation_sparql(graph: Graph):
    """
    Run SPARQL queries to verify transformation correctness.
    """
    print("\n" + "=" * 70)
    print("SPARQL VERIFICATION QUERIES")
    print("=" * 70)
    
    # Query 1: Check for any remaining GMN shortcut properties
    print("\nQuery 1: Any remaining GMN P46i_1_is_contained_in properties?")
    print("-" * 70)
    
    query1 = """
    PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
    
    SELECT (COUNT(*) AS ?count)
    WHERE {
        ?s gmn:P46i_1_is_contained_in ?o .
    }
    """
    result1 = graph.query(query1)
    for row in result1:
        count = int(row.count)
        print(f"Remaining GMN properties: {count}")
        assert count == 0, "Transformation incomplete!"
    print("✓ No GMN shortcut properties remaining")
    
    # Query 2: Count CIDOC-CRM properties
    print("\nQuery 2: How many CIDOC-CRM P46i_forms_part_of relationships?")
    print("-" * 70)
    
    query2 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    
    SELECT (COUNT(*) AS ?count)
    WHERE {
        ?s cidoc:P46i_forms_part_of ?o .
    }
    """
    result2 = graph.query(query2)
    for row in result2:
        count = int(row.count)
        print(f"CIDOC-CRM properties: {count}")
    print("✓ CIDOC-CRM properties present")
    
    # Query 3: List all containment relationships
    print("\nQuery 3: All containment relationships")
    print("-" * 70)
    
    query3 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    
    SELECT ?document ?container
    WHERE {
        ?document cidoc:P46i_forms_part_of ?container .
    }
    ORDER BY ?document
    """
    result3 = graph.query(query3)
    for row in result3:
        print(f"  {row.document} → {row.container}")
    
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE ✓")
    print("=" * 70)


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    """
    Run this script directly to execute tests.
    
    Usage:
        python is-contained-in-transform.py
    """
    
    print("\n" + "=" * 70)
    print("P46i.1 IS CONTAINED IN - TRANSFORMATION TEST SUITE")
    print("=" * 70)
    
    # Run transformation tests
    test_graph = test_p46i_1_transformation()
    
    # Run SPARQL verification
    verify_transformation_sparql(test_graph)
    
    print("\n" + "=" * 70)
    print("ALL TESTS AND VERIFICATIONS PASSED ✓")
    print("Ready for production deployment!")
    print("=" * 70)


# ==============================================================================
# HELPER FUNCTIONS (Optional)
# ==============================================================================

def count_containment_relationships(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> dict:
    """
    Count containment relationships before and after transformation.
    
    Returns:
        dict: Counts of GMN and CIDOC-CRM properties
    """
    gmn_count = len(list(graph.triples((None, gmn_ns.P46i_1_is_contained_in, None))))
    cidoc_count = len(list(graph.triples((None, cidoc_ns.P46i_forms_part_of, None))))
    
    return {
        "gmn_p46i_1": gmn_count,
        "cidoc_p46i": cidoc_count,
        "total": gmn_count + cidoc_count
    }


def get_containment_hierarchy(graph: Graph, cidoc_ns: Namespace, document_uri) -> list:
    """
    Get the full containment hierarchy for a document.
    
    Args:
        graph: RDF graph
        cidoc_ns: CIDOC-CRM namespace
        document_uri: URI of the document
    
    Returns:
        list: Chain of containers from document to top-level archive
    """
    hierarchy = [document_uri]
    current = document_uri
    
    # Traverse up the containment chain
    while True:
        containers = list(graph.objects(current, cidoc_ns.P46i_forms_part_of))
        if not containers:
            break
        container = containers[0]  # Take first if multiple
        hierarchy.append(container)
        current = container
    
    return hierarchy


def validate_containment_ranges(graph: Graph, gmn_ns: Namespace, cidoc_ns: Namespace) -> bool:
    """
    Validate that all containers are properly typed as E78_Curated_Holding.
    
    Returns:
        bool: True if all ranges are valid
    """
    from rdflib.namespace import RDF
    
    for s, p, o in graph.triples((None, gmn_ns.P46i_1_is_contained_in, None)):
        # Check if container has appropriate type
        types = list(graph.objects(o, RDF.type))
        is_curated_holding = any(
            cidoc_ns.E78_Curated_Holding in types or 
            str(t).endswith("E78_Curated_Holding") 
            for t in types
        )
        
        if not is_curated_holding:
            print(f"⚠ Warning: {o} is not typed as E78_Curated_Holding")
            return False
    
    return True


# ==============================================================================
# DOCUMENTATION STRINGS
# ==============================================================================

"""
Property Transformation: gmn:P46i_1_is_contained_in → cidoc:P46i_forms_part_of
============================================================================

Type: Direct Property Mapping
Complexity: Simple
Intermediate Nodes: None

Description:
-----------
This transformation converts the GMN shortcut property for archival containment
into its equivalent CIDOC-CRM property. No intermediate nodes are created.

Input Pattern:
-------------
?document gmn:P46i_1_is_contained_in ?container .

Output Pattern:
--------------
?document cidoc:P46i_forms_part_of ?container .

Domain: cidoc:E31_Document (and all subclasses)
Range: cidoc:E78_Curated_Holding (and all subclasses)

Common Use Cases:
----------------
1. Contracts in notarial registers
2. Letters in letterbooks
3. Documents in filze (bundles)
4. Documents in buste (boxes)
5. Any document in an archival collection

CIDOC-CRM Alignment:
-------------------
This property is a direct subproperty of cidoc:P46i_forms_part_of, which means
it inherits all the semantics of the parent property. The CIDOC-CRM definition
states: "This property associates an instance of E18 Physical Thing with another
instance of E18 Physical Thing that forms part of it."

Performance:
-----------
- Time Complexity: O(n) where n = number of P46i_1 statements
- Space Complexity: O(1) - no new nodes created
- Efficiency: Very high - simple property substitution

See Also:
--------
- CIDOC-CRM P46i_forms_part_of documentation
- ISAD(G) archival description standard
- EAD (Encoded Archival Description) standard
"""
