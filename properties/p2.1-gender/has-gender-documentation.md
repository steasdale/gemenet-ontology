# Has Sex/Gender Property - Ontology Documentation

## Table of Contents
1. [Property Overview](#property-overview)
2. [Semantic Definition](#semantic-definition)
3. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
4. [Controlled Vocabulary](#controlled-vocabulary)
5. [Usage Patterns](#usage-patterns)
6. [Transformation Logic](#transformation-logic)
7. [Examples](#examples)
8. [Best Practices](#best-practices)

---

## Property Overview

### Basic Information

**Property URI**: `gmn:P2_1_gender`

**Label**: "P2.1 has sex/gender" @en

**Definition**: Simplified property for expressing biological characteristics and physiological traits that distinguish the males and females of a species.

**Created**: 2025-10-16

**Status**: Active

### Quick Reference

| Aspect | Value |
|--------|-------|
| **Domain** | `cidoc:E21_Person` |
| **Range** | Controlled vocabulary (three AAT terms) |
| **Superproperty** | `cidoc:P2_has_type` |
| **Cardinality** | 0..1 (optional, single value) |
| **Functional** | Yes (one gender value per person) |

---

## Semantic Definition

### Full RDF/OWL Definition

```turtle
gmn:P2_1_gender
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P2.1 has sex/gender"@en ;
    rdfs:comment "Simplified property for expressing biological characteristics and physiological traits that distinguish the males and females of a species. This is an extension of the CIDOC-CRM path: E21_Person > P2_has_type > E55_Type. The range is restricted to a controlled vocabulary of three Getty AAT terms: male (300189559), female (300189557), and intersex (300417544)."@en ;
    rdfs:subPropertyOf cidoc:P2_has_type ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range [
        a owl:Class ;
        owl:oneOf (
            aat:300189559  # male
            aat:300189557  # female
            aat:300417544  # intersex
        )
    ] ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P2_has_type, aat:300189559, aat:300189557, aat:300417544 .
```

### Scope and Purpose

**Purpose**: The `gmn:P2_1_gender` property serves to record the biological sex characteristics of persons in historical documents. It provides a standardized, semantically rich way to capture this information while maintaining compatibility with CIDOC-CRM standards.

**Scope**: 
- Applies to instances of `E21_Person`
- Records biological sex only (not gender identity or social roles)
- Uses controlled vocabulary for consistency and interoperability
- Represents information as documented in historical sources

**Rationale**: 
Historical documents often reference the biological sex of individuals, which can be:
- Important for understanding social and legal contexts
- Relevant for prosopographical research
- Necessary for identifying specific individuals
- Part of the documentary evidence

This property provides a structured way to record such information when it appears in source documents.

---

## CIDOC-CRM Alignment

### Relationship to CIDOC-CRM

The `gmn:P2_1_gender` property is a **subproperty of** `cidoc:P2_has_type`.

#### CIDOC-CRM P2_has_type

**Domain**: `E1_CRM_Entity`  
**Range**: `E55_Type`  
**Definition**: "This property allows sub typing of CRM entities - a form of specialisation – through the use of a terminological hierarchy, or thesaurus."

**Quantification**: many to many (0,n:0,n)

### Why P2_has_type?

The CIDOC-CRM uses P2_has_type for classification and typing of entities. Using this pattern for gender:

1. **Semantic clarity**: Gender is a type/classification of person
2. **Standard pattern**: Consistent with CRM typing conventions
3. **Extensibility**: Allows additional types alongside gender
4. **Vocabulary support**: Integrates with controlled vocabularies (AAT)

### Simplified Property Pattern

**Simplified GMN Form**:
```
E21_Person --gmn:P2_1_gender--> E55_Type (AAT term)
```

**Equivalent CIDOC-CRM Form**:
```
E21_Person --P2_has_type--> E55_Type (AAT term with gender semantics)
```

The simplified property:
- Makes data entry more intuitive
- Enforces controlled vocabulary at ontology level
- Still maintains CIDOC-CRM compatibility through subproperty relationship
- Transforms to standard P2_has_type in output

---

## Controlled Vocabulary

### Getty AAT Terms

The property range is restricted to exactly three Getty Art & Architecture Thesaurus (AAT) terms:

#### 1. Male (aat:300189559)

**Full URI**: `http://vocab.getty.edu/page/aat/300189559`

**Getty Definition**: "Biological sex characteristic of producing small, typically mobile gametes (sperm or pollen)."

**Scope note**: Used for male biological sex in humans and other species.

**Hierarchical Position**:
```
Physical Attributes (Attributes and Properties)
  └─ sex (biological concept)
      └─ male (biological concept)
```

**Use when**: Historical documents explicitly identify an individual as male, or when biological sex is clearly indicated through context.

#### 2. Female (aat:300189557)

**Full URI**: `http://vocab.getty.edu/page/aat/300189557`

**Getty Definition**: "Biological sex characteristic of producing large, typically immobile gametes (eggs or ovules)."

**Scope note**: Used for female biological sex in humans and other species.

**Hierarchical Position**:
```
Physical Attributes (Attributes and Properties)
  └─ sex (biological concept)
      └─ female (biological concept)
```

**Use when**: Historical documents explicitly identify an individual as female, or when biological sex is clearly indicated through context.

#### 3. Intersex (aat:300417544)

**Full URI**: `http://vocab.getty.edu/page/aat/300417544`

**Getty Definition**: "Refers to people born with reproductive or sexual anatomy that doesn't seem to fit typical definitions of male or female."

**Scope note**: Used for individuals with intersex characteristics or variations in sex characteristics.

**Hierarchical Position**:
```
Physical Attributes (Attributes and Properties)
  └─ sex (biological concept)
      └─ intersex
```

**Use when**: Historical documents indicate intersex characteristics, or when sources explicitly use terms for intersex individuals.

### Vocabulary Enforcement

The ontology enforces this controlled vocabulary through OWL enumeration:

```turtle
rdfs:range [
    a owl:Class ;
    owl:oneOf (
        aat:300189559  # male
        aat:300189557  # female
        aat:300417544  # intersex
    )
]
```

**Benefits**:
- **Validation**: Invalid values rejected at ontology level
- **Consistency**: Ensures uniform data entry
- **Interoperability**: Compatible with other systems using AAT
- **Semantic richness**: Each term carries full AAT semantics

**Restrictions**:
- Only these three URIs are valid
- String labels (e.g., "male", "female") are NOT valid
- Other AAT terms are NOT valid
- Custom values are NOT valid

---

## Usage Patterns

### Basic Usage

**Pattern 1: Direct Assignment**
```json
{
  "@id": "person/p123",
  "@type": "cidoc:E21_Person",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  }
}
```

**Pattern 2: With Full Person Data**
```json
{
  "@id": "person/p456",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Abraham ben Moses",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  },
  "gmn:P107i_3_has_occupation": "merchant",
  "gmn:P11i_1_earliest_attestation_date": "1150"
}
```

**Pattern 3: String URI Format** (also valid)
```json
{
  "@id": "person/p789",
  "@type": "cidoc:E21_Person",
  "gmn:P2_1_gender": "aat:300189557"
}
```

### Integration with Other Properties

Gender information often appears alongside other person properties:

**With Family Relationships**:
```json
{
  "@id": "person/daughter",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Sarah bat Isaac",
  "gmn:P2_1_gender": {"@id": "aat:300189557"},
  "gmn:P97_1_has_father": {"@id": "person/father"},
  "gmn:P96_1_has_mother": {"@id": "person/mother"}
}
```

**With Occupational Information**:
```json
{
  "@id": "person/merchant",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Jacob ibn David",
  "gmn:P2_1_gender": {"@id": "aat:300189559"},
  "gmn:P107i_3_has_occupation": "merchant",
  "gmn:P107i_2_has_social_category": "Jewish"
}
```

**With Marital Relationships**:
```json
{
  "@id": "person/wife",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Miriam bat David",
  "gmn:P2_1_gender": {"@id": "aat:300189557"},
  "gmn:P11i_3_has_spouse": {"@id": "person/husband"}
}
```

### When NOT to Use

**Avoid using this property when**:

1. **Gender is inferred only from name**
   - Example: Don't assume "Abraham" = male without documentary evidence
   - Name conventions vary by culture and period

2. **Source is ambiguous**
   - If the document doesn't clearly indicate gender
   - When pronouns or terms are unclear

3. **Recording social roles instead of biological sex**
   - Social gender roles should use occupation or social category properties
   - Gender expression ≠ biological sex

4. **No documentary evidence**
   - Speculation should not be recorded
   - Leave property absent rather than guessing

5. **Modern gender identity concepts**
   - This property records historical biological sex documentation
   - Not for modern gender identity terminology

---

## Transformation Logic

### Transformation Overview

The transformation converts the simplified `gmn:P2_1_gender` property to the standard CIDOC-CRM `P2_has_type` pattern with proper `E55_Type` instances.

### Transformation Steps

**Step 1: Check for Property**
```python
if 'gmn:P2_1_gender' not in data:
    return data  # No gender property, continue
```

**Step 2: Extract Gender URI**
```python
gender = data['gmn:P2_1_gender']

if isinstance(gender, str):
    gender_uri = gender
elif isinstance(gender, dict) and '@id' in gender:
    gender_uri = gender['@id']
else:
    return data  # Invalid format, skip
```

**Step 3: Create E55_Type Instance**
```python
gender_type = {
    '@id': gender_uri,
    '@type': 'cidoc:E55_Type'
}
```

**Step 4: Add to P2_has_type**
```python
if 'cidoc:P2_has_type' not in data:
    data['cidoc:P2_has_type'] = []
elif not isinstance(data['cidoc:P2_has_type'], list):
    data['cidoc:P2_has_type'] = [data['cidoc:P2_has_type']]

data['cidoc:P2_has_type'].append(gender_type)
```

**Step 5: Remove Simplified Property**
```python
del data['gmn:P2_1_gender']
```

### Why This Transformation?

**Semantic Preservation**: 
- Gender AAT URIs carry semantic meaning
- E55_Type classification is CIDOC-CRM compliant
- Preserves relationship to controlled vocabulary

**Structural Compliance**:
- Conforms to CIDOC-CRM P2_has_type pattern
- Allows multiple types on same person
- Maintains proper class hierarchy

**Practical Benefits**:
- Simplifies data entry (use gmn:P2_1_gender)
- Ensures output compliance (transforms to P2_has_type)
- Validates input at ontology level
- Produces queryable CIDOC-CRM output

### Handling Multiple Types

When a person has multiple P2_has_type values (e.g., gender + occupation), they are maintained in an array:

**Input**:
```json
{
  "@id": "person/p123",
  "gmn:P2_1_gender": {"@id": "aat:300189559"},
  "gmn:P107i_3_has_occupation": "scholar"
}
```

**Output** (after both transformations):
```json
{
  "@id": "person/p123",
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300025565",
      "@type": "cidoc:E55_Type"
    },
    {
      "@id": "aat:300189559",
      "@type": "cidoc:E55_Type"
    }
  ]
}
```

---

## Examples

### Example 1: Basic Male Person

**Input (GMN Simplified)**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://data.geniza.org/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "person/p001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Abraham ben Moses",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  }
}
```

**Output (CIDOC-CRM Compliant)**:
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "https://data.geniza.org/ontology/",
    "aat": "http://vocab.getty.edu/page/aat/"
  },
  "@id": "person/p001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p001/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Abraham ben Moses"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300189559",
      "@type": "cidoc:E55_Type"
    }
  ]
}
```

### Example 2: Female Person with Relationships

**Input**:
```json
{
  "@id": "person/p002",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Esther bat David",
  "gmn:P2_1_gender": {
    "@id": "aat:300189557"
  },
  "gmn:P97_1_has_father": {
    "@id": "person/father_david"
  },
  "gmn:P11i_3_has_spouse": {
    "@id": "person/husband_abraham"
  }
}
```

**Output**:
```json
{
  "@id": "person/p002",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p002/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Esther bat David"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300189557",
      "@type": "cidoc:E55_Type"
    }
  ],
  "cidoc:P96_by_mother_or_father": [
    {
      "@id": "person/p002/birth",
      "@type": "cidoc:E67_Birth",
      "cidoc:P97_from_father": {
        "@id": "person/father_david",
        "@type": "cidoc:E21_Person"
      }
    }
  ],
  "cidoc:P11i_participated_in": [
    {
      "@id": "person/p002/marriage",
      "@type": "cidoc:E7_Activity",
      "cidoc:P2_has_type": {
        "@id": "aat:300055971",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P11_had_participant": {
        "@id": "person/husband_abraham",
        "@type": "cidoc:E21_Person"
      }
    }
  ]
}
```

### Example 3: Intersex Person

**Input**:
```json
{
  "@id": "person/p003",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Person Name",
  "gmn:P2_1_gender": {
    "@id": "aat:300417544"
  },
  "gmn:P11i_1_earliest_attestation_date": "1175"
}
```

**Output**:
```json
{
  "@id": "person/p003",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p003/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Person Name"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300417544",
      "@type": "cidoc:E55_Type"
    }
  ],
  "cidoc:P92i_was_brought_into_existence_by": {
    "@id": "person/p003/birth",
    "@type": "cidoc:E67_Birth",
    "cidoc:P4_has_time-span": {
      "@id": "person/p003/birth/timespan/earliest",
      "@type": "cidoc:E52_Time-Span",
      "cidoc:P82a_begin_of_the_begin": "1175"
    }
  }
}
```

### Example 4: Person Without Gender

**Input**:
```json
{
  "@id": "person/p004",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Unknown Person",
  "gmn:P107i_3_has_occupation": "scribe"
}
```

**Output**:
```json
{
  "@id": "person/p004",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p004/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Unknown Person"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300025161",
      "@type": "cidoc:E55_Type"
    }
  ]
}
```

**Note**: Gender is absent, only occupation type appears. This is correct behavior.

### Example 5: Person with Multiple Types

**Input**:
```json
{
  "@id": "person/p005",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Moses ibn Maimon",
  "gmn:P2_1_gender": {
    "@id": "aat:300189559"
  },
  "gmn:P107i_3_has_occupation": "scholar",
  "gmn:P107i_2_has_social_category": "Jewish"
}
```

**Output**:
```json
{
  "@id": "person/p005",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "person/p005/appellation/name",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "aat:300404651",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Moses ibn Maimon"
    }
  ],
  "cidoc:P2_has_type": [
    {
      "@id": "aat:300025565",
      "@type": "cidoc:E55_Type"
    },
    {
      "@id": "aat:300189559",
      "@type": "cidoc:E55_Type"
    }
  ],
  "cidoc:P107i_is_current_or_former_member_of": [
    {
      "@id": "person/p005/membership/jewish",
      "@type": "cidoc:E74_Group",
      "cidoc:P2_has_type": {
        "@id": "aat:300025658",
        "@type": "cidoc:E55_Type"
      }
    }
  ]
}
```

---

## Best Practices

### Data Entry Guidelines

#### 1. Use Documentary Evidence

✅ **Correct**: Record gender when explicitly stated in documents
```
Document states: "Abraham the merchant, son of Moses"
Action: Add gmn:P2_1_gender with aat:300189559 (male)
```

❌ **Incorrect**: Infer from name alone
```
Name is "Abraham"
Action: DO NOT automatically assume male
```

#### 2. Use Correct URIs

✅ **Correct**: Use full AAT URI
```json
"gmn:P2_1_gender": {"@id": "aat:300189559"}
```

❌ **Incorrect**: Use text label
```json
"gmn:P2_1_gender": "male"  // INVALID
```

❌ **Incorrect**: Use wrong namespace
```json
"gmn:P2_1_gender": {"@id": "gmn:male"}  // INVALID
```

#### 3. Handle Uncertainty

✅ **Correct**: Omit property when uncertain
```json
{
  "@id": "person/uncertain",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Unknown Person"
  // No gender property - left blank
}
```

❌ **Incorrect**: Guess or infer without evidence
```json
{
  "@id": "person/uncertain",
  "gmn:P2_1_gender": {"@id": "aat:300189559"}  // NO EVIDENCE
}
```

#### 4. Document Sources

When recording gender, note the source:

✅ **Best Practice**: Add editorial note referencing source
```json
{
  "@id": "person/p123",
  "gmn:P1_1_has_name": "Person Name",
  "gmn:P2_1_gender": {"@id": "aat:300189559"},
  "gmn:P3_1_has_editorial_note": "Gender identified as male in marriage contract dated 1150"
}
```

#### 5. Respect Privacy and Sensitivity

- Record only what historical documents state
- Avoid anachronistic interpretations
- Be sensitive to cultural and historical contexts
- Don't impose modern categories on historical persons

### Validation Checklist

Before entering gender data, verify:

- [ ] Gender is explicitly stated in source document
- [ ] Correct AAT URI is used (one of the three allowed terms)
- [ ] URI format is correct (aat:XXXXXXX)
- [ ] Not inferring from name, role, or other indirect evidence
- [ ] Source document is cited in editorial notes
- [ ] Cultural and historical context is appropriate

### Query Examples

**Find all male persons**:
```sparql
SELECT ?person ?name
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P2_has_type aat:300189559 ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
}
```

**Find persons without recorded gender**:
```sparql
SELECT ?person ?name
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P1_is_identified_by/cidoc:P190_has_symbolic_content ?name .
  FILTER NOT EXISTS {
    ?person cidoc:P2_has_type ?gender .
    FILTER(?gender IN (aat:300189559, aat:300189557, aat:300417544))
  }
}
```

**Count persons by gender**:
```sparql
SELECT ?gender (COUNT(?person) AS ?count)
WHERE {
  ?person a cidoc:E21_Person ;
          cidoc:P2_has_type ?gender .
  FILTER(?gender IN (aat:300189559, aat:300189557, aat:300417544))
}
GROUP BY ?gender
```

---

## Cross-References

### Related GMN Properties

- **gmn:P1_1_has_name**: Person's primary name
- **gmn:P11i_3_has_spouse**: Marital relationships
- **gmn:P96_1_has_mother**: Maternal relationship
- **gmn:P97_1_has_father**: Paternal relationship
- **gmn:P107i_2_has_social_category**: Social group membership
- **gmn:P107i_3_has_occupation**: Professional roles

### Related CIDOC-CRM Classes

- **E21_Person**: Domain of the property
- **E55_Type**: Range of the transformed property
- **E67_Birth**: May reference gender at birth
- **E74_Group**: For gender-based group memberships (if relevant)

### External Resources

- **Getty AAT**: http://vocab.getty.edu/
- **CIDOC-CRM**: http://www.cidoc-crm.org/
- **GMN Project**: https://data.geniza.org/

---

*This documentation reflects current GMN ontology standards and CIDOC-CRM version 7.1.3. For the most up-to-date information, consult the official ontology files and project documentation.*
