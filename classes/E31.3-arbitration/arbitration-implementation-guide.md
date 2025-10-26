# Arbitration Agreement Implementation Guide

**Version:** 1.0  
**Date:** October 26, 2025  
**Estimated Implementation Time:** 60-90 minutes  
**Difficulty Level:** Intermediate

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites and Preparation](#prerequisites-and-preparation)
3. [Understanding the Arbitration Agreement Model](#understanding-the-arbitration-agreement-model)
4. [Implementation Workflow](#implementation-workflow)
5. [Phase 1: Ontology Updates](#phase-1-ontology-updates)
6. [Phase 2: Transformation Script Updates](#phase-2-transformation-script-updates)
7. [Phase 3: Documentation Updates](#phase-3-documentation-updates)
8. [Phase 4: Testing and Validation](#phase-4-testing-and-validation)
9. [Omeka-S Integration](#omeka-s-integration)
10. [Advanced Usage and Considerations](#advanced-usage-and-considerations)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Reference Materials](#reference-materials)
13. [Appendix: Command Reference](#appendix-command-reference)

---

## Introduction

### What Are Arbitration Agreements?

Arbitration agreements are legal contracts that document a specific type of transaction in medieval and early modern commerce: the **transfer of the obligation to resolve a dispute** from the disputing parties to appointed arbitrator(s). In these agreements:

- Two or more parties acknowledge an existing dispute
- They agree to relinquish other forms of dispute resolution (litigation, negotiation, etc.)
- They transfer the authority to resolve the dispute to one or more neutral arbitrators
- All parties commit to accepting the arbitrator's binding decision
- The dispute concerns specific subject matter (property, debts, rights, contracts, etc.)

### Historical Context

In medieval Italian commerce, arbitration was preferred over formal court proceedings because:

1. **Speed**: Arbitration resolved disputes in weeks rather than months or years
2. **Expertise**: Arbitrators often had specialized knowledge of commercial practices
3. **Privacy**: Proceedings could be conducted discreetly
4. **Finality**: Decisions were binding and enforceable
5. **Flexibility**: Parties could choose arbitrators they trusted

### Why This Implementation?

This implementation provides:

- **Semantic accuracy**: Models arbitration as an E7_Activity (joint process) rather than forcing it into acquisition patterns
- **Active agency**: Uses P14_carried_out_by for all parties to reflect that everyone actively participates in the arbitration agreement
- **Flexibility**: Can model various dispute types and subjects
- **Consistency**: Follows the same document → event → actors pattern as sales contracts
- **Extensibility**: Can be enhanced with additional properties in the future

### What You'll Accomplish

By completing this guide, you will:

1. Add one new class (E31_3_Arbitration_Agreement) to the GMN ontology
2. Add three new properties (P70.18, P70.19, P70.20) to the GMN ontology
3. Implement three transformation functions in Python
4. Update project documentation
5. Test the implementation with sample data
6. Validate CIDOC-CRM compliance

### Implementation Components

This implementation adds:

**New Class:**
- `gmn:E31_3_Arbitration_Agreement` - subclass of `gmn:E31_1_Contract`

**New Properties:**
- `gmn:P70_18_documents_disputing_party` - links to parties in dispute
- `gmn:P70_19_documents_arbitrator` - links to appointed arbitrator(s)
- `gmn:P70_20_documents_dispute_subject` - links to subject matter of dispute

**Transformation Functions:**
- `transform_p70_18_documents_disputing_party()` - transforms disputing parties
- `transform_p70_19_documents_arbitrator()` - transforms arbitrators
- `transform_p70_20_documents_dispute_subject()` - transforms dispute subjects

---

## Prerequisites and Preparation

### Required Skills

- **Basic RDF/Turtle syntax**: Ability to read and edit Turtle files
- **Basic Python**: Understanding of functions, dictionaries, and lists
- **Text editing**: Comfortable using a text editor or IDE
- **Command line basics**: Ability to run commands in terminal
- **JSON-LD familiarity**: Understanding of JSON-LD structure (helpful but not required)

### Required Software

- **Text editor or IDE** (VS Code, Sublime Text, Atom, Notepad++, or similar)
- **Python 3.6+** installed and accessible from command line
- **RDF validator** (rapper command-line tool, online validator, or Protégé)
- **Optional**: Git for version control
- **Optional**: JSON validator or Python json.tool module

### Required Files

Locate these files in your project before beginning:

1. `gmn_ontology.rdf` - Main ontology file (RDF/Turtle format)
2. `gmn_to_cidoc_transform_script.py` - Transformation script (Python)
3. Main project documentation file (usually Markdown, Word, or text)

**Where to find them:**
- Ontology file typically in: `ontology/` or project root
- Transformation script typically in: `scripts/` or `tools/`
- Documentation typically in: `docs/` or project root

### Required Knowledge

Before implementing, ensure you understand:

1. **Existing contract structure**: Review how `gmn:E31_1_Contract` and `gmn:E31_2_Sales_Contract` are implemented
2. **Transformation pattern**: Review how sales contract properties (P70.1-P70.17) are transformed
3. **Project workflow**: Understand how data flows from Omeka-S through transformation to output

### Pre-Implementation Checklist

Complete these preparation steps before beginning:

- [ ] **Backup all files** you'll be modifying (use timestamped backups)
- [ ] **Test current transformation script** to ensure it works correctly
- [ ] **Review existing sales contract implementation** for comparison
- [ ] **Read the semantic documentation** (arbitration-agreement-documentation.md)
- [ ] **Set up test environment** for validation
- [ ] **Clear your workspace** - close unnecessary applications
- [ ] **Allocate uninterrupted time** (60-90 minutes recommended)
- [ ] **Have reference files ready** - keep .ttl and .py snippet files accessible
- [ ] **Verify ontology version** - should be 1.3 or higher
- [ ] **Check Python version** - run `python3 --version` (should be 3.6+)

### Understanding Your Starting Point

Before implementing, verify your current setup:

**Ontology Status:**
1. **Version**: Should be 1.3 or higher
2. **Existing contract classes**: Should include E31_1_Contract and E31_2_Sales_Contract
3. **Existing properties**: Should include P70.1 through P70.17
4. **Structure**: Classes and properties in alphabetical order

**Transformation Script Status:**
1. **Working**: Script should successfully transform sales contracts
2. **Constants defined**: Should have AAT constants (AAT_NAME, AAT_WITNESS, etc.)
3. **Pattern established**: Should have existing transform_p70_X functions
4. **transform_item() present**: Main transformation function exists

**Documentation Status:**
1. **Current**: Documentation describes existing ontology
2. **Organized**: Clear sections for classes, properties, examples
3. **Format**: Consistent formatting (usually Markdown)

### Creating Backups

Create timestamped backups of all files you'll modify:

```bash
# Navigate to project directory
cd /path/to/your/project

# Backup ontology (with timestamp)
cp gmn_ontology.rdf gmn_ontology.rdf.backup-$(date +%Y%m%d-%H%M%S)

# Backup transformation script
cp gmn_to_cidoc_transform_script.py gmn_to_cidoc_transform_script.py.backup-$(date +%Y%m%d-%H%M%S)

# Backup documentation
cp main_documentation.md main_documentation.md.backup-$(date +%Y%m%d-%H%M%S)

# Verify backups were created
ls -lh *.backup-*
```

**Why timestamped backups?**
- Multiple backups don't overwrite each other
- Easy to identify when backup was created
- Can roll back to specific points in time

### Setting Up Your Workspace

**Recommended window/tab layout:**

1. **Text editor**: Open with three tabs
   - Tab 1: gmn_ontology.rdf
   - Tab 2: gmn_to_cidoc_transform_script.py
   - Tab 3: main_documentation.md

2. **Reference files**: Open in separate editor or window
   - arbitration-agreement-ontology.ttl
   - arbitration-agreement-transform.py
   - arbitration-agreement-documentation.md

3. **Terminal/Command prompt**: For running validation commands

4. **Browser**: For online validators (optional)

### Time Management

**Recommended schedule:**

- **Phase 1 (Ontology)**: 20-25 minutes
- **Phase 2 (Python)**: 20-25 minutes
- **Phase 3 (Documentation)**: 15-20 minutes
- **Phase 4 (Testing)**: 20-30 minutes
- **Buffer**: 10-15 minutes for troubleshooting

**Tips for success:**
- Work through phases in order
- Don't skip validation steps
- Take a 5-minute break between phases
- If stuck for more than 10 minutes, consult troubleshooting section

---

## Understanding the Arbitration Agreement Model

### Conceptual Overview

The arbitration agreement model treats arbitration as a **collaborative activity** carried out jointly by all parties:

```
┌─────────────────────────────────────────────────────────────┐
│              Arbitration Agreement Document                  │
│              (E31_3_Arbitration_Agreement)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │ P70_documents
                       ▼
         ┌─────────────────────────────────┐
         │    Arbitration Activity          │
         │    (E7_Activity)                 │
         │    Type: AAT 300417271           │
         └──┬────────────────┬──────────┬───┘
            │                │          │
            │ P14            │ P14      │ P16
            ▼                ▼          ▼
    ┌──────────────┐  ┌──────────┐  ┌──────────────┐
    │ Disputing    │  │Arbitrator│  │   Dispute    │
    │ Parties      │  │          │  │   Subject    │
    │ (E39_Actor)  │  │(E39_Actor│  │(E1_CRM_Entity│
    └──────────────┘  └──────────┘  └──────────────┘
```

**Key insight**: All three properties contribute to ONE shared E7_Activity node.

### Semantic Foundation

**Why this model works:**

1. **Document → Activity relationship**: The contract document (E31) documents an activity (E7)
2. **Activity typing**: The E7_Activity is typed as "arbitration" via AAT 300417271
3. **Active participation**: All human actors use P14_carried_out_by (active agency)
4. **Object relationship**: Dispute subject uses P16_used_specific_object (operated on)

**What makes this special:**

Unlike passive documentation, this model emphasizes that arbitration is something all parties **actively do together**:
- Disputing parties actively consent to arbitration
- Arbitrators actively agree to render judgment
- All parties jointly carry out the arbitration agreement

### Key Semantic Decisions Explained

#### Decision 1: E7_Activity vs E8_Acquisition

**Question**: Why not use E8_Acquisition like sales contracts?

**Answer**: Arbitration agreements are not property acquisitions. They are legal processes/agreements where parties collaborate to transfer dispute resolution obligations.

**E7_Activity is better because:**
- ✅ Semantically accurate for collaborative processes
- ✅ Allows flexible typing via P2_has_type → AAT
- ✅ Doesn't force the wrong acquisition model
- ✅ Better represents the collaborative nature

**E8_Acquisition would be wrong because:**
- ❌ E8 is specifically for transferring ownership of physical objects
- ❌ While there is a transfer (of obligations), it's not a property transfer
- ❌ Would misrepresent the nature of arbitration
- ❌ Would create semantic confusion

**Real-world analogy**: 
- Sales contract = Person A gives object to Person B
- Arbitration = Persons A and B jointly transfer problem-solving to Person C

#### Decision 2: P14_carried_out_by for All Parties

**Question**: Why do both disputing parties AND arbitrators use the same property?

**Answer**: Because both are **active principals** who carry out the arbitration agreement.

**Disputing parties are active because they:**
- Actively consent to arbitration
- Agree to be bound by decision
- Participate in proceedings
- Carry out their role in the agreement

**Arbitrators are active because they:**
- Actively consent to serve
- Agree to render decision
- Conduct the arbitration
- Carry out their role in the agreement

**Why not P11_had_participant?**
- P11 implies passive presence ("was there")
- P14 implies active agency ("did it")
- Arbitration requires active consent from all parties
- This reflects historical reality: medieval arbitration required explicit agreement

**Real-world analogy**: Think of a mediated negotiation. All parties must actively agree to participate - it's not something done TO them, but something they all DO together.

#### Decision 3: P16_used_specific_object for Dispute Subject

**Question**: Why use P16 instead of P14 for the dispute subject?

**Answer**: Because the dispute subject is **operated on**, not a participant.

**Why P16_used_specific_object:**
- ✅ The activity operates on/examines/analyzes the subject
- ✅ Standard CIDOC-CRM pattern for activities involving objects
- ✅ Distinguishes subject from participants
- ✅ Range of E1_CRM_Entity provides maximum flexibility

**Why not P14_carried_out_by:**
- ❌ A building/debt/right doesn't "carry out" arbitration
- ❌ Would conflate objects with actors
- ❌ Semantically inaccurate

**Why not P67_refers_to:**
- ❌ Too generic - doesn't capture operational relationship
- ❌ Doesn't show activity operates on the subject
- ❌ Weaker semantic connection

**Real-world analogy**: In a trial, the disputed property doesn't participate in the trial - it's what the trial is about. Similarly, the dispute subject is what the arbitration operates on.

### Comparison with Sales Contracts

Understanding the parallel structure helps:

| Aspect | Sales Contract | Arbitration Agreement |
|--------|---------------|----------------------|
| **What's transferred?** | Ownership of property | Obligation to resolve dispute |
| **From whom?** | Seller (P23) | Disputing parties (P14) |
| **To whom?** | Buyer (P22) | Arbitrator(s) (P14) |
| **Event class** | E8_Acquisition | E7_Activity |
| **Event type** | Inherent to E8 | AAT 300417271 (via P2) |
| **Object link** | P24_transferred_title_of | P16_used_specific_object |
| **What changes hands?** | Physical object | Legal obligation |
| **Document property** | P70_documents | P70_documents |
| **Pattern** | E31 → P70 → E8 → P23/P22/P24 | E31 → P70 → E7 → P14/P16 |

**Key similarity**: Both use P70_documents to link document to event

**Key difference**: Sales uses different properties for seller/buyer; Arbitration uses same property (P14) for all actors

### The Shared Activity Pattern

All three properties (P70.18, P70.19, P70.20) contribute to **one shared E7_Activity node**:

**Visual representation:**

```turtle
# INPUT: Three separate shortcut properties
<contract> gmn:P70_18_documents_disputing_party <person1>, <person2> .
<contract> gmn:P70_19_documents_arbitrator <person3> .
<contract> gmn:P70_20_documents_dispute_subject <building> .

# OUTPUT: Single E7_Activity with all information
<contract> cidoc:P70_documents <contract/arbitration> .

<contract/arbitration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
    cidoc:P14_carried_out_by <person1>, <person2>, <person3> ;
    cidoc:P16_used_specific_object <building> .
```

**Why share one activity node?**

1. **Data integrity**: All information about one arbitration stays together
2. **Query efficiency**: Easy to retrieve complete arbitration information with one query
3. **Logical coherence**: One arbitration agreement = one arbitration activity
4. **Pattern consistency**: Matches sales contract structure (one acquisition event)
5. **Prevents fragmentation**: Avoids creating multiple disconnected activity nodes

**How is this achieved?**

Each transformation function:
1. Checks if `cidoc:P70_documents` already exists
2. If yes: uses the existing E7_Activity
3. If no: creates a new E7_Activity with consistent URI
4. Adds its information to the shared activity
5. Result: all properties contribute to same node

### URI Generation Pattern

**Activity URI formula**: `{contract_uri}/arbitration`

**Examples:**
- Contract: `http://example.org/contracts/123`
- Activity: `http://example.org/contracts/123/arbitration`

**Why this pattern?**
- Predictable and deterministic
- Easy to construct from contract URI
- Prevents duplicate activities
- Shows clear parent-child relationship
- Follows RESTful URI principles

### Transformation Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Input Document                         │
│  - P70.18: [party1, party2]                             │
│  - P70.19: [arbitrator1]                                │
│  - P70.20: [subject1]                                   │
└────────────┬────────────────────────────────────────────┘
             │
             ├─────► transform_p70_18() ──┐
             │                             │
             ├─────► transform_p70_19() ──┼─► Shared
             │                             │   E7_Activity
             └─────► transform_p70_20() ──┘
                                           │
┌──────────────────────────────────────────┴───────────────┐
│              Transformed Output                           │
│  cidoc:P70_documents: [                                   │
│    {                                                      │
│      @type: E7_Activity                                   │
│      P2_has_type: AAT 300417271                          │
│      P14_carried_out_by: [party1, party2, arbitrator1]   │
│      P16_used_specific_object: [subject1]                │
│    }                                                      │
│  ]                                                        │
└───────────────────────────────────────────────────────────┘
```

### Property Transformation Paths

**P70.18 Transformation Path:**
```
gmn:P70_18_documents_disputing_party
    ↓
E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor
```

**P70.19 Transformation Path:**
```
gmn:P70_19_documents_arbitrator
    ↓
E31_Document → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor
```

**P70.20 Transformation Path:**
```
gmn:P70_20_documents_dispute_subject
    ↓
E31_Document → P70_documents → E7_Activity → P16_used_specific_object → E1_CRM_Entity
```

**Key observation**: P70.18 and P70.19 have identical paths (both use P14)

---

## Implementation Workflow

### Overview of All Steps

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Ontology Updates (20-25 minutes)                   │
├─────────────────────────────────────────────────────────────┤
│ ✓ Update ontology metadata (version, date)                  │
│ ✓ Add E31_3_Arbitration_Agreement class                     │
│ ✓ Add P70.18 property (disputing party)                     │
│ ✓ Add P70.19 property (arbitrator)                          │
│ ✓ Add P70.20 property (dispute subject)                     │
│ ✓ Validate RDF syntax                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Transformation Script (20-25 minutes)              │
├─────────────────────────────────────────────────────────────┤
│ ✓ Add AAT_ARBITRATION constant                              │
│ ✓ Add transform_p70_18() function                           │
│ ✓ Add transform_p70_19() function                           │
│ ✓ Add transform_p70_20() function                           │
│ ✓ Update transform_item() to call new functions             │
│ ✓ Test Python syntax                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Documentation (15-20 minutes)                      │
├─────────────────────────────────────────────────────────────┤
│ ✓ Update class hierarchy section                            │
│ ✓ Add property descriptions                                 │
│ ✓ Add usage examples                                        │
│ ✓ Add workflow guidance                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Testing & Validation (20-30 minutes)               │
├─────────────────────────────────────────────────────────────┤
│ ✓ Create test data files                                    │
│ ✓ Run transformation script                                 │
│ ✓ Validate output structure                                 │
│ ✓ Test edge cases                                           │
│ ✓ CIDOC-CRM compliance check                                │
└─────────────────────────────────────────────────────────────┘
```

### Workflow Tips

**General principles:**
1. **Work sequentially**: Complete each phase before moving to next
2. **Validate frequently**: Test after each major addition
3. **Keep reference files accessible**: Have .ttl and .py files open
4. **Save often**: Save after each significant change
5. **Take breaks**: Step away if stuck for more than 10 minutes

**If something goes wrong:**
1. Don't panic - you have backups
2. Check the troubleshooting section
3. Validate syntax first (most common issue)
4. Compare your code to reference files
5. Test in isolation (one function at a time)

**Before moving to next phase:**
- ✓ Current phase completely finished
- ✓ All validation tests pass
- ✓ Files saved
- ✓ Quick review of what you added

---

## Phase 1: Ontology Updates

### Overview

In this phase, you will add one class and three properties to the RDF ontology file. The additions follow alphabetical ordering and maintain consistency with existing ontology patterns.

**Time estimate**: 20-25 minutes

**What you'll do:**
1. Update ontology metadata (version and date)
2. Add E31_3_Arbitration_Agreement class
3. Add three properties (P70.18, P70.19, P70.20)
4. Validate RDF syntax

**Files modified**: `gmn_ontology.rdf`

### Step 1.1: Locate and Open the Ontology File

**Navigate to your project directory:**
```bash
cd /path/to/your/project
```

**Locate the ontology file:**
```bash
ls -l gmn_ontology.rdf
```

**Create a backup** (if not already done):
```bash
cp gmn_ontology.rdf gmn_ontology.rdf.backup-$(date +%Y%m%d-%H%M%S)
```

**Open the file in your text editor:**
```bash
# Examples for different editors:
code gmn_ontology.rdf          # VS Code
subl gmn_ontology.rdf          # Sublime Text
atom gmn_ontology.rdf          # Atom
nano gmn_ontology.rdf          # Nano (command line)
```

**Understanding the file structure:**
```
gmn_ontology.rdf
├── @prefix declarations (lines 1-10)
├── Ontology declaration (lines 11-20)
├── Classes section (lines 21-300)
│   ├── E22_1_Building
│   ├── E22_2_Moveable_Property
│   ├── E31_1_Contract
│   ├── E31_2_Sales_Contract
│   ├── E74_1_Regional_Provenance
│   └── ... more classes ...
└── Properties section (lines 301-1500)
    ├── has_payment_provided_by
    ├── P1_1_has_name
    ├── ... many properties ...
    ├── P70_17_documents_sale_price_currency
    ├── P94i_1_was_created_by
    └── ... more properties ...
```

### Step 1.2: Update Ontology Metadata

**Location**: Near the top of the file (approximately lines 11-20)

**What to find:**
Look for the ontology declaration section that looks like this:

```turtle
<http://www.genoesemerchantnetworks.com/ontology> 
    a owl:Ontology ;
    rdfs:label "Genoese Merchant Networks CIDOC-CRM Extension"@en ;
    rdfs:comment "Custom vocabulary extending CIDOC-CRM..."@en ;
    dcterms:title "GMN CIDOC-CRM Extension Ontology"@en ;
    dcterms:creator "Genoese Merchant Networks Project" ;
    dcterms:created "2025-10-16"^^xsd:date ;
    dcterms:modified "2025-10-17"^^xsd:date ;  ← UPDATE THIS
    owl:versionInfo "1.3" ;                    ← UPDATE THIS
    owl:imports <http://www.cidoc-crm.org/cidoc-crm/> .
```

**What to change:**

1. Find the line with `dcterms:modified`
2. Change the date to today's date: `"2025-10-26"^^xsd:date`
3. Find the line with `owl:versionInfo`
4. Change the version to: `"1.4"`

**After editing, it should look like:**
```turtle
<http://www.genoesemerchantnetworks.com/ontology> 
    a owl:Ontology ;
    rdfs:label "Genoese Merchant Networks CIDOC-CRM Extension"@en ;
    rdfs:comment "Custom vocabulary extending CIDOC-CRM..."@en ;
    dcterms:title "GMN CIDOC-CRM Extension Ontology"@en ;
    dcterms:creator "Genoese Merchant Networks Project" ;
    dcterms:created "2025-10-16"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;  ← UPDATED
    owl:versionInfo "1.4" ;                    ← UPDATED
    owl:imports <http://www.cidoc-crm.org/cidoc-crm/> .
```

**Why this matters:**
- Version tracking helps manage ontology evolution
- Other systems may depend on version numbers
- Modified date documents when last changed
- Good practice for ontology maintenance

**Common mistakes:**
- ❌ Forgetting `^^xsd:date` after the date string
- ❌ Not using quotes around date
- ❌ Not using quotes around version number
- ❌ Forgetting semicolon at end of line
- ❌ Forgetting period after last property

### Step 1.3: Add the Arbitration Agreement Class

**Location**: In the Classes section, after `gmn:E31_2_Sales_Contract` and before `gmn:E74_1_Regional_Provenance`

**How to find the insertion point:**

1. Search for "E31.2 Sales Contract" (Ctrl+F or Cmd+F)
2. Scroll to the end of that class definition (look for the period `.`)
3. The next class should be E74_1_Regional_Provenance
4. Insert the new class BETWEEN these two

**Visual guide:**

```turtle
# Class: E31.2 Sales Contract
gmn:E31_2_Sales_Contract
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.2 Sales Contract"@en ;
    rdfs:comment "Specialized class..."@en ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract .   ← Period ends this class

# ← INSERT NEW CLASS HERE (blank line before comment)

# Class: E74.1 Regional Provenance
gmn:E74_1_Regional_Provenance
```

**What to insert:**

Copy this complete class definition:

```turtle
# Class: E31.3 Arbitration Agreement
gmn:E31_3_Arbitration_Agreement
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.3 Arbitration Agreement"@en ;
    rdfs:comment "Specialized class that describes arbitration agreement documents. This is a specialized type of gmn:E31_1_Contract used to represent legal documents that record the agreement between disputing parties to transfer the obligation to resolve their dispute to one or more arbitrators. In this transaction, two or more parties involved in a conflict agree to relinquish their right to pursue other forms of dispute resolution and instead accept the binding decision of the appointed arbitrator(s). The contract documents both the transfer of the dispute resolution obligation from the parties to the arbitrator(s) and the agreement by the parties to be bound by the arbitrator's decision. This represents a transfer of legal obligations similar to how sales contracts represent transfers of ownership rights. Instances of this class represent the physical or conceptual document itself, while the actual arbitration activity is modeled through E7_Activity that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E7_Activity, cidoc:P70_documents .
```

**Understanding each part of the class definition:**

```turtle
# Class: E31.3 Arbitration Agreement      ← Comment for human readers
gmn:E31_3_Arbitration_Agreement           ← Full URI using gmn prefix
    a owl:Class ;                          ← Declares as OWL class
    rdfs:subClassOf gmn:E31_1_Contract ;   ← Parent class
    rdfs:label "E31.3 Arbitration Agreement"@en ;  ← Display name
    rdfs:comment "Long description..."@en ;        ← Full description
    dcterms:created "2025-10-17"^^xsd:date ;      ← When first created
    dcterms:modified "2025-10-26"^^xsd:date ;     ← When last modified
    rdfs:seeAlso gmn:E31_1_Contract, ... .        ← Related classes
```

**Key points:**

- The class inherits from `gmn:E31_1_Contract` (same as Sales Contract)
- The comment explains the semantic meaning thoroughly
- Both created and modified dates are included
- The period at the end is critical - it terminates the definition
- rdfs:seeAlso links to related concepts for documentation

**After insertion:**

Your file should now look like this in the Classes section:

```turtle
# Class: E31.2 Sales Contract
gmn:E31_2_Sales_Contract
    a owl:Class ;
    ...
    rdfs:seeAlso gmn:E31_1_Contract .

# Class: E31.3 Arbitration Agreement
gmn:E31_3_Arbitration_Agreement
    a owl:Class ;
    ...
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E7_Activity, cidoc:P70_documents .

# Class: E74.1 Regional Provenance
gmn:E74_1_Regional_Provenance
```

**Common mistakes to avoid:**

- ❌ Missing the blank line before the comment
- ❌ Forgetting the period at the end of rdfs:seeAlso
- ❌ Wrong indentation (should be 4 spaces per level)
- ❌ Missing semicolons after each property except the last
- ❌ Typos in the class name (must match exactly)
- ❌ Missing `@en` language tags on labels and comments

**Checkpoint:**

- [ ] Class definition inserted in correct location
- [ ] All semicolons present except before final period
- [ ] Period present at end of definition
- [ ] Proper indentation maintained
- [ ] No syntax errors (editor highlighting looks correct)

### Step 1.4: Add the Three Arbitration Properties

Now we'll add three new properties to the Properties section of the ontology. These properties provide shortcuts for common arbitration relationships.

**Location**: In the Properties section, find where P70.17 ends and insert the new properties immediately after it.

**How to find the insertion point:**

1. Search for "P70.17" or "P70_17_documents_sale_price_currency" (Ctrl+F or Cmd+F)
2. Scroll to the end of that property definition (look for the period `.`)
3. The next property should be something like P94i_1_was_created_by
4. Insert the three new properties BETWEEN these two

**Visual guide:**

```turtle
# Property: P70.17 documents sale price currency
gmn:P70_17_documents_sale_price_currency
    a owl:ObjectProperty ;
    rdfs:label "P70.17 documents sale price currency"@en ;
    rdfs:comment "..."@en ;
    rdfs:domain gmn:E31_2_Sales_Contract ;
    rdfs:range cidoc:E55_Type ;
    dcterms:created "2025-10-17"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P180_has_currency .   ← Period ends this property

# ← INSERT NEW PROPERTIES HERE (blank line before comment)

# Property: P94i.1 was created by
gmn:P94i_1_was_created_by
```

#### Property 1: P70.18 - Documents Disputing Party

**Insert this complete property definition first:**

```turtle
# Property: P70.18 documents disputing party
gmn:P70_18_documents_disputing_party
    a owl:ObjectProperty ;
    rdfs:label "P70.18 documents disputing party"@en ;
    rdfs:comment "Shortcut property. This property documents that an arbitration agreement (E31_3_Arbitration_Agreement) records one of the parties involved in the dispute that is subject to arbitration. Expands to: E31_3_Arbitration_Agreement → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor. The disputing parties are active principals in the arbitration agreement - they jointly carry out the agreement to submit their dispute to arbitration and to be bound by the arbitrator's decision. Multiple instances of this property can be used when there are multiple disputing parties (which is common in medieval arbitration cases)."@en ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

**Understanding P70.18:**

- **Purpose**: Links arbitration agreement to the parties who are in dispute
- **Range**: E39_Actor (people or organizations)
- **Domain**: E31_3_Arbitration_Agreement only
- **Cardinality**: Can be used multiple times (usually 2+ parties in dispute)
- **Transformation**: Expands to P70 → E7 → P14 → E39
- **Semantic**: Uses P14 (carried out by) because parties actively participate

#### Property 2: P70.19 - Documents Arbitrator

**Insert this complete property definition second:**

```turtle
# Property: P70.19 documents arbitrator
gmn:P70_19_documents_arbitrator
    a owl:ObjectProperty ;
    rdfs:label "P70.19 documents arbitrator"@en ;
    rdfs:comment "Shortcut property. This property documents that an arbitration agreement (E31_3_Arbitration_Agreement) records an arbitrator appointed to resolve the dispute. Expands to: E31_3_Arbitration_Agreement → P70_documents → E7_Activity → P14_carried_out_by → E39_Actor. The arbitrator is the neutral third party (or parties) who carries out the arbitration activity. Like the disputing parties, arbitrators use P14_carried_out_by because they are active principals in conducting the arbitration process. Multiple instances of this property can be used when multiple arbitrators are appointed (panels were common in medieval commercial arbitration)."@en ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

**Understanding P70.19:**

- **Purpose**: Links arbitration agreement to the appointed arbitrator(s)
- **Range**: E39_Actor (people chosen to arbitrate)
- **Domain**: E31_3_Arbitration_Agreement only
- **Cardinality**: Can be used multiple times (panels of 2-3 arbitrators were common)
- **Transformation**: Expands to P70 → E7 → P14 → E39
- **Semantic**: Uses P14 (carried out by) because arbitrators actively conduct the arbitration

#### Property 3: P70.20 - Documents Dispute Subject

**Insert this complete property definition third:**

```turtle
# Property: P70.20 documents dispute subject
gmn:P70_20_documents_dispute_subject
    a owl:ObjectProperty ;
    rdfs:label "P70.20 documents dispute subject"@en ;
    rdfs:comment "Shortcut property. This property documents that an arbitration agreement (E31_3_Arbitration_Agreement) records the subject matter of the dispute being arbitrated. Expands to: E31_3_Arbitration_Agreement → P70_documents → E7_Activity → P16_used_specific_object → E1_CRM_Entity. The dispute subject is the matter that the arbitration concerns - this could be property (buildings, goods), rights, debts, contracts, or other entities. Unlike the parties and arbitrators (which use P14_carried_out_by), the dispute subject uses P16_used_specific_object because it is the object being operated upon by the arbitration activity, not a participant in it. Multiple instances of this property can be used when the dispute concerns multiple items or rights."@en ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .
```

**Understanding P70.20:**

- **Purpose**: Links arbitration agreement to what the dispute is about
- **Range**: E1_CRM_Entity (the broadest CIDOC-CRM class - can be anything)
- **Domain**: E31_3_Arbitration_Agreement only
- **Cardinality**: Can be used multiple times (disputes can involve multiple subjects)
- **Transformation**: Expands to P70 → E7 → P16 → E1
- **Semantic**: Uses P16 (used specific object) because the subject is operated upon

**After insertion, the Properties section should look like:**

```turtle
# Property: P70.17 documents sale price currency
gmn:P70_17_documents_sale_price_currency
    ...
    rdfs:seeAlso cidoc:P70_documents, cidoc:P180_has_currency .

# Property: P70.18 documents disputing party
gmn:P70_18_documents_disputing_party
    ...
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .

# Property: P70.19 documents arbitrator
gmn:P70_19_documents_arbitrator
    ...
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .

# Property: P70.20 documents dispute subject
gmn:P70_20_documents_dispute_subject
    ...
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .

# Property: P94i.1 was created by
gmn:P94i_1_was_created_by
```

**Key differences between the properties:**

| Property | Links to          | Uses CIDOC                 | Semantic reason              |
| -------- | ----------------- | -------------------------- | ---------------------------- |
| P70.18   | Disputing parties | P14 (carried out by)       | Parties actively participate |
| P70.19   | Arbitrators       | P14 (carried out by)       | Arbitrators actively conduct |
| P70.20   | Dispute subject   | P16 (used specific object) | Subject is operated upon     |

**Common mistakes to avoid:**

- ❌ Wrong property order (must be P70.18, P70.19, P70.20)
- ❌ Inconsistent indentation
- ❌ Missing blank lines between properties
- ❌ Forgetting periods at the end of each definition
- ❌ Wrong rdfs:domain (all three should be E31_3_Arbitration_Agreement)
- ❌ Wrong rdfs:range (P70.18 and P70.19 are E39_Actor, P70.20 is E1_CRM_Entity)
- ❌ Typos in property names

**Checkpoint:**

- [ ] All three properties inserted in correct order (P70.18, P70.19, P70.20)
- [ ] Each property has all required fields
- [ ] Periods present at end of each definition
- [ ] Proper indentation maintained throughout
- [ ] No syntax errors visible in editor

### Step 1.5: Validate the Ontology Syntax

After adding the class and properties, it's critical to validate that the RDF syntax is correct before proceeding.

**Save the file first:**

- Press Ctrl+S (Windows/Linux) or Cmd+S (Mac)
- Verify the file saved successfully

**Method 1: Using rapper (command-line RDF parser)**

If you have rapper installed (part of Raptor RDF Syntax Library):

```bash
# Validate the ontology file
rapper -i turtle -o ntriples gmn_ontology.rdf > /dev/null

# If successful, you'll see something like:
# rapper: Parsing file gmn_ontology.rdf with parser turtle
# rapper: Serializing with serializer ntriples
# rapper: Parsing returned 1250 triples

# If there are errors, you'll see error messages with line numbers
```

**What to look for:**

- ✓ "Parsing returned X triples" means success
- ❌ Parse error messages indicate syntax problems
- ❌ Line numbers in errors show where to fix

**Method 2: Using Python and rdflib**

If you have Python with rdflib installed:

```bash
python3 << 'EOF'
from rdflib import Graph

g = Graph()
try:
    g.parse("gmn_ontology.rdf", format="turtle")
    print(f"✓ Success! Parsed {len(g)} triples")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

**Method 3: Using Protégé (GUI)**

If you have Protégé desktop application:

1. Open Protégé
2. File → Open → Select gmn_ontology.rdf
3. If it loads without errors, syntax is valid
4. Check the "Classes" and "Object Properties" tabs to verify your additions

**Method 4: Online RDF Validator**

If you don't have local tools:

1. Open: http://www.easyrdf.org/converter
2. Paste your ontology content into the input box
3. Select "Input format: Turtle"
4. Click "Convert"
5. If it converts successfully, syntax is valid

**Common validation errors and fixes:**

| Error Message      | Likely Cause      | Fix                                      |
| ------------------ | ----------------- | ---------------------------------------- |
| "Expected ';'"     | Missing semicolon | Add `;` at end of property line          |
| "Expected '.'"     | Missing period    | Add `.` at end of class/property         |
| "Unexpected token" | Extra character   | Remove unexpected character              |
| "Undefined prefix" | Missing @prefix   | Check prefix declarations at top         |
| "Bad IRI"          | Malformed URI     | Check URI syntax (spaces, special chars) |

**Manual review checklist:**

Even if validation passes, manually verify:

- [ ] Class definition (E31_3_Arbitration_Agreement) is present
- [ ] Three properties (P70.18, P70.19, P70.20) are present
- [ ] Each definition ends with a period
- [ ] All semicolons present (except before final period)
- [ ] Proper indentation (4 spaces per level)
- [ ] Language tags (@en) on all labels and comments
- [ ] No typos in class/property names
- [ ] Correct parent classes and ranges

**If validation fails:**

1. **Read the error message carefully** - it usually indicates the line number
2. **Check the common mistakes** listed in previous steps
3. **Compare your code** to the provided examples character-by-character
4. **Check for invisible characters** - copy-paste issues can introduce these
5. **Restore from backup** if needed and try again

**If validation succeeds:**

Congratulations! Phase 1 is complete. Your ontology now includes:

- 1 new class (E31_3_Arbitration_Agreement)
- 3 new properties (P70.18, P70.19, P70.20)
- Updated metadata (version 1.4, modified date)

**Before moving to Phase 2:**

- [ ] Ontology file saved
- [ ] Validation passed
- [ ] Quick visual review completed
- [ ] Backup still available if needed

---

## Phase 2: Transformation Script Updates

### Overview

In this phase, you will add three transformation functions to the Python script. These functions convert the shortcut properties (P70.18, P70.19, P70.20) into full CIDOC-CRM compliant structures.

**Time estimate**: 25-30 minutes

**What you'll do:**

1. Locate and open the transformation script
2. Add AAT constant for arbitration (if not present)
3. Add three transformation functions
4. Update the transform_item() function to call them
5. Test the functions

**Files modified**: `gmn_to_cidoc_transform_script.py`

**Required knowledge:**

- Basic Python syntax (functions, dictionaries, lists)
- Understanding of the transformation pattern from sales contracts
- JSON-LD structure familiarity

### Step 2.1: Locate and Open the Transformation Script

**Navigate to your project directory** (if not already there):

```bash
cd /path/to/your/project
```

**Locate the transformation script:**

```bash
ls -l gmn_to_cidoc_transform_script.py
# or
find . -name "*transform*.py"
```

**Create a backup** (if not already done):

```bash
cp gmn_to_cidoc_transform_script.py gmn_to_cidoc_transform_script.py.backup-$(date +%Y%m%d-%H%M%S)
```

**Open the file in your text editor:**

```bash
# Examples for different editors:
code gmn_to_cidoc_transform_script.py          # VS Code
subl gmn_to_cidoc_transform_script.py          # Sublime Text
atom gmn_to_cidoc_transform_script.py          # Atom
nano gmn_to_cidoc_transform_script.py          # Nano
```

**Understanding the script structure:**

```
gmn_to_cidoc_transform_script.py
├── Imports (lines 1-20)
├── AAT Constants (lines 21-50)
│   ├── AAT_NAME = "..."
│   ├── AAT_WITNESS = "..."
│   ├── AAT_SALE = "..."
│   └── ... more constants ...
├── Helper Functions (lines 51-200)
│   ├── get_or_create_actor()
│   ├── get_or_create_place()
│   └── ... more helpers ...
├── Transform Functions (lines 201-1500)
│   ├── transform_p1_1_has_name()
│   ├── transform_p70_1_documents_seller()
│   ├── ... many more transforms ...
│   └── transform_p70_17_documents_sale_price_currency()
└── Main Function (lines 1501-1700)
    ├── transform_item()
    └── main()
```

**Checkpoint before proceeding:**

- [ ] Script file located and opened
- [ ] Backup created
- [ ] File structure familiar
- [ ] Can identify different sections (imports, constants, functions)

### Step 2.2: Add AAT Constant for Arbitration

**Location**: In the constants section near the top (approximately lines 21-50)

**What to find:**
Look for the section with AAT (Art & Architecture Thesaurus) constants. It should look like:

```python
# AAT (Getty Art & Architecture Thesaurus) Constants
AAT_NAME = "http://vocab.getty.edu/aat/300404670"
AAT_WITNESS = "http://vocab.getty.edu/aat/300025463"
AAT_SALE = "http://vocab.getty.edu/aat/300054751"
AAT_PAYMENT = "http://vocab.getty.edu/aat/300417635"
# ... more constants ...
```

**What to add:**

Add this constant at the end of the AAT constants section (maintain alphabetical order if possible):

```python
AAT_ARBITRATION = "http://vocab.getty.edu/aat/300417271"
```

**After insertion, it should look like:**

```python
# AAT (Getty Art & Architecture Thesaurus) Constants
AAT_ARBITRATION = "http://vocab.getty.edu/aat/300417271"
AAT_NAME = "http://vocab.getty.edu/aat/300404670"
AAT_PAYMENT = "http://vocab.getty.edu/aat/300417635"
AAT_SALE = "http://vocab.getty.edu/aat/300054751"
AAT_WITNESS = "http://vocab.getty.edu/aat/300025463"
# ... more constants ...
```

**Why this constant is needed:**

- AAT_ARBITRATION is a controlled vocabulary term from Getty's AAT
- It types the E7_Activity as specifically an arbitration activity
- This enables semantic queries and proper categorization
- It distinguishes arbitration activities from other E7_Activity types

**Verification:**

- [ ] Constant added with correct URL
- [ ] Proper Python syntax (string in quotes, ends with no comma)
- [ ] Variable name is AAT_ARBITRATION (all caps)
- [ ] No typos in the URL

### Step 2.3: Add transform_p70_18_documents_disputing_party Function

**Location**: In the transform functions section, after the last `transform_p70_17_*` function and before `transform_item()`

**How to find the insertion point:**

1. Search for "def transform_p70_17" (Ctrl+F or Cmd+F)
2. Scroll to the end of the last P70.17 function
3. You'll likely see a blank line or two
4. Insert the new function here, before `transform_item()`

**Visual guide:**

```python
def transform_p70_17_documents_sale_price_currency(data):
    """Transform sale price currency shortcut property"""
    # ... function implementation ...
    return data

# ← INSERT NEW FUNCTIONS HERE (1-2 blank lines before)

def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
```

**What to insert:**

Copy this complete function:

```python
def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function locates the existing E7_Activity node (or creates one) and adds
    disputing parties to it via P14_carried_out_by. Disputing parties are the
    individuals or organizations involved in the conflict being arbitrated.
    
    Args:
        data: The item data dictionary (JSON-LD structure)
    
    Returns:
        Modified data dictionary with shortcut property transformed
    
    Note:
        Both disputing parties and arbitrators use P14_carried_out_by because
        they are all active principals carrying out the arbitration agreement.
    """
    # Step 1: Check if the shortcut property exists in the data
    if 'gmn:P70_18_documents_disputing_party' not in data:
        return data
    
    # Step 2: Get the property values (array of disputing parties)
    parties = data['gmn:P70_18_documents_disputing_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Check if arbitration activity already exists, or create it
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity (may have been created by other properties)
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
    
    # Step 4: Initialize P14 (carried out by) array if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Step 5: Process each disputing party and add to the activity
    for party_obj in parties:
        # Handle both URI references and full objects
        if isinstance(party_obj, dict):
            # Already a full object with @id
            party_data = party_obj.copy()
            if '@type' not in party_data:
                party_data['@type'] = 'cidoc:E39_Actor'
        else:
            # Just a URI reference, convert to full object
            party_uri = str(party_obj)
            party_data = {
                '@id': party_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add the party to the arbitration activity
        existing_activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Step 6: Remove the shortcut property from the data
    del data['gmn:P70_18_documents_disputing_party']
    
    return data
```

**Understanding the function structure:**

The function has six main steps:

1. **Check existence**: Return early if property not present (optimization)
2. **Extract data**: Get the parties array and subject URI
3. **Find/create activity**: Reuse existing E7_Activity or create new one
4. **Initialize array**: Ensure P14_carried_out_by array exists
5. **Process parties**: Loop through and add each party to the activity
6. **Clean up**: Remove shortcut property from data

**Key concepts:**

- **Reusing the activity**: If P70_documents already exists (maybe from P70.19 or P70.20 processed first), we add to it rather than creating a duplicate
- **P14_carried_out_by**: Used because parties actively participate in the arbitration agreement
- **AAT typing**: The activity is typed as arbitration using the AAT constant
- **Flexible input**: Handles both simple URIs and full object structures

**After insertion:**

```python
def transform_p70_17_documents_sale_price_currency(data):
    # ... existing function ...
    return data

def transform_p70_18_documents_disputing_party(data):
    # ... new function just added ...
    return data

def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
```

**Common mistakes to avoid:**

- ❌ Wrong function name or typo in name
- ❌ Inconsistent indentation (Python requires consistent indentation)
- ❌ Missing `from uuid import uuid4` at top of file if not present
- ❌ Forgetting to use AAT_ARBITRATION constant
- ❌ Not handling both dict and string input formats

**Checkpoint:**

- [ ] Function inserted in correct location
- [ ] All indentation correct (4 spaces per level)
- [ ] Function name matches exactly: transform_p70_18_documents_disputing_party
- [ ] No syntax errors visible in editor
- [ ] AAT_ARBITRATION constant is used

### Step 2.4: Understanding the transform_p70_18 Function in Detail

Before adding the next two functions, let's deeply understand how `transform_p70_18_documents_disputing_party` works. This understanding will help you verify the next functions are working correctly.

**Complete function flow diagram:**

```
Input Data (JSON-LD):
{
    '@id': 'doc123',
    '@type': 'gmn:E31_3_Arbitration_Agreement',
    'gmn:P70_18_documents_disputing_party': [
        'actor1',
        {'@id': 'actor2', '@type': 'cidoc:E39_Actor'}
    ]
}

↓ Transform Function Called ↓

Step 1: Check if property exists
├─ if 'gmn:P70_18_documents_disputing_party' not in data
└─ Found! Continue...

Step 2: Extract party data
├─ parties = ['actor1', {'@id': 'actor2', ...}]
└─ subject_uri = 'doc123'

Step 3: Find or create E7_Activity
├─ Check if 'cidoc:P70_documents' exists
│   ├─ If yes: Use existing_activity = data['cidoc:P70_documents'][0]
│   └─ If no: Create new activity
│       ├─ activity_uri = 'doc123/arbitration'
│       ├─ Create activity object with:
│       │   ├─ @id: 'doc123/arbitration'
│       │   ├─ @type: 'cidoc:E7_Activity'
│       │   └─ P2_has_type: AAT_ARBITRATION
│       └─ Add to data['cidoc:P70_documents']
└─ Activity now exists in data structure

Step 4: Initialize P14 array
├─ Check if 'cidoc:P14_carried_out_by' in existing_activity
└─ If not, create empty array: []

Step 5: Process each party
├─ For 'actor1' (string):
│   ├─ Convert to: {'@id': 'actor1', '@type': 'cidoc:E39_Actor'}
│   └─ Append to P14 array
└─ For {'@id': 'actor2', ...} (dict):
    ├─ Copy the object
    ├─ Ensure @type is 'cidoc:E39_Actor'
    └─ Append to P14 array

Step 6: Clean up
├─ Delete 'gmn:P70_18_documents_disputing_party'
└─ Return modified data

↓ Output Data (JSON-LD) ↓

{
    '@id': 'doc123',
    '@type': 'gmn:E31_3_Arbitration_Agreement',
    'cidoc:P70_documents': [{
        '@id': 'doc123/arbitration',
        '@type': 'cidoc:E7_Activity',
        'cidoc:P2_has_type': {
            '@id': 'http://vocab.getty.edu/aat/300417271',
            '@type': 'cidoc:E55_Type'
        },
        'cidoc:P14_carried_out_by': [
            {'@id': 'actor1', '@type': 'cidoc:E39_Actor'},
            {'@id': 'actor2', '@type': 'cidoc:E39_Actor'}
        ]
    }]
}
```

**Step-by-step code explanation:**

**Step 1: Existence check**

```python
if 'gmn:P70_18_documents_disputing_party' not in data:
    return data
```

- If the property doesn't exist, return immediately (no work needed)
- This makes the function safe to call even on non-arbitration items
- Optimization: avoids unnecessary processing

**Step 2: Extract the parties**

```python
parties = data['gmn:P70_18_documents_disputing_party']
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
```

- Gets the array of parties from the shortcut property
- Gets the document's URI (or generates one if missing)
- The subject_uri is used to create the activity URI

**Step 3: Find or create the arbitration activity**

```python
existing_activity = None
if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
    existing_activity = data['cidoc:P70_documents'][0]
else:
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
```

- First checks if P70_documents already exists (maybe from another property)
- If it exists, reuses that activity (critical for consistency)
- If not, creates a new E7_Activity with:
  - Unique URI based on document + "/arbitration"
  - Typed as E7_Activity
  - Has P2_has_type pointing to AAT arbitration concept
- The activity is always added/exists in data['cidoc:P70_documents'][0]
- **Important**: We use [0] because P70_documents is an array, but for arbitration we only create one activity per document

**Why check for existing activity?**

- Properties P70.18, P70.19, and P70.20 all add to the SAME E7_Activity
- The transform functions can be called in any order
- If P70.19 runs first, it creates the activity
- When P70.18 runs second, it should ADD to that activity, not create a duplicate
- This ensures all parties, arbitrators, and subjects are in ONE arbit

### Step 2.5: Add transform_p70_19_documents_arbitrator Function

**Insert this complete function immediately after the previous one:**

```python
def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function locates the existing E7_Activity node (or creates one) and adds
    arbitrators to it via P14_carried_out_by. Arbitrators are the neutral third
    parties who conduct the arbitration and render binding decisions.
    
    Args:
        data: The item data dictionary (JSON-LD structure)
    
    Returns:
        Modified data dictionary with shortcut property transformed
    
    Note:
        Arbitrators and disputing parties both use P14_carried_out_by because
        they are all active principals carrying out the arbitration agreement.
    """
    # Step 1: Check if property exists in data
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    # Step 2: Get the property values (array of arbitrators)
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Check if arbitration activity already exists
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
    
    # Step 4: Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Step 5: Add arbitrators to the activity
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
    
    # Step 6: Remove shortcut property from data
    del data['gmn:P70_19_documents_arbitrator']
    
    return data
```

### Step 2.6: Add transform_p70_20_documents_dispute_subject Function

**Insert this complete function immediately after the previous one:**

```python
def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    
    This function locates the existing E7_Activity node and adds the dispute
    subject(s) via P16_used_specific_object. The dispute subject is the matter
    being arbitrated - can be property, rights, debts, contracts, etc.
    
    Args:
        data: The item data dictionary (JSON-LD structure)
    
    Returns:
        Modified data dictionary with shortcut property transformed
    
    Note:
        Unlike P70.18/P70.19 which use P14 (carried out by), this uses P16
        (used specific object) because the subject is operated on, not a participant.
    """
    # Step 1: Check if property exists in data
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    # Step 2: Get the property values (array of subjects)
    subjects = data['gmn:P70_20_documents_dispute_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Check if arbitration activity already exists
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
    
    # Step 4: Initialize P16 if it doesn't exist
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Step 5: Add dispute subjects to the activity
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
    
    # Step 6: Remove shortcut property from data
    del data['gmn:P70_20_documents_dispute_subject']
    
    return data
```

### Step 2.7: Update the transform_item() Function

**Location**: Find the `transform_item()` function (usually near line 1500-1600)

**Find this section:**

```python
def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    """
    # Name and identification properties
    item = transform_p1_1_has_name(item)
    # ... many more transformations ...
    
    # Sales contract properties
    item = transform_p70_1_documents_seller(item)
    # ... more sales contract properties ...
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # ← INSERT HERE
    
    return item
```

**Insert these three lines after sales contract properties:**

```python
    # Arbitration agreement properties
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
```

### Step 2.8: Save and Test Python Syntax

**Save the file**: Ctrl+S (or Cmd+S)

**Test syntax compilation:**

```bash
python3 -m py_compile gmn_to_cidoc_transform_script.py
```

**If successful**: No output, file compiles without errors

✅ **Phase 2 Complete!**

---

## Phase 3: Documentation Updates

### Overview

**Time estimate**: 15-20 minutes

### Step 3.1: Update Class Hierarchy

Find your class hierarchy section and update to:

```
E31_1_Contract (General contract class)
├── E31_2_Sales_Contract (Sales and acquisition contracts)
└── E31_3_Arbitration_Agreement (Arbitration agreements)
```

Add description:

```markdown
### E31_3_Arbitration Agreement

Represents arbitration agreement documents that record agreements between 
disputing parties to transfer the obligation to resolve their dispute to 
appointed arbitrator(s). All parties (disputing parties AND arbitrators) are 
active principals carrying out the agreement together via P14_carried_out_by.
```

### Step 3.2: Add Property Descriptions

```markdown
### P70.18 documents disputing party
**Domain:** E31_3_Arbitration_Agreement  
**Range:** E39_Actor  
**Path:** E31 → P70 → E7_Activity → P14 → E39_Actor

Links arbitration agreement to parties involved in the dispute.

### P70.19 documents arbitrator
**Domain:** E31_3_Arbitration_Agreement  
**Range:** E39_Actor  
**Path:** E31 → P70 → E7_Activity → P14 → E39_Actor

Links arbitration agreement to person(s) appointed to resolve the dispute.

### P70.20 documents dispute subject
**Domain:** E31_3_Arbitration_Agreement  
**Range:** E1_CRM_Entity  
**Path:** E31 → P70 → E7_Activity → P16 → E1_CRM_Entity

Links arbitration agreement to the subject matter of the dispute.
```

### Step 3.3: Add Usage Example

```markdown
## Example: Arbitration Agreement

**Input:**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/giovanni"},
    {"@id": "http://example.org/persons/marco"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/judge_antonio"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/buildings/palazzo_spinola"}
  ]
}
```

**Output:**
All three actors under P14_carried_out_by, subject under P16_used_specific_object.

```
✅ **Phase 3 Complete!**

---

## Phase 4: Testing and Validation

### Overview

**Time estimate**: 20-30 minutes

### Step 4.1: Create Test Data File

Create `test_arbitration.json`:

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "http://example.org/contracts/arb_test_001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {"@value": "Arbitration Agreement - Test Case"}
  ],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/giovanni_merchant"},
    {"@id": "http://example.org/persons/marco_merchant"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/judge_antonio"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/buildings/palazzo_spinola"}
  ],
  "gmn:P94i_2_has_enactment_date": [
    {"@value": "1450-06-15", "@type": "xsd:date"}
  ]
}
```

### Step 4.2: Run Transformation

```bash
python3 gmn_to_cidoc_transform_script.py test_arbitration.json test_output.json
```

**Expected output:**

```
✓ Transformation complete: test_output.json
```

### Step 4.3: Validate Output

Open `test_output.json` and verify:

**✅ Check 1: E7_Activity exists**

```json
"cidoc:P70_documents": [{
  "@id": "http://example.org/contracts/arb_test_001/arbitration",
  "@type": "cidoc:E7_Activity"
}]
```

**✅ Check 2: Activity is typed**

```json
"cidoc:P2_has_type": {
  "@id": "http://vocab.getty.edu/page/aat/300417271",
  "@type": "cidoc:E55_Type"
}
```

**✅ Check 3: All actors under P14**

```json
"cidoc:P14_carried_out_by": [
  {"@id": "http://example.org/persons/giovanni_merchant", "@type": "cidoc:E39_Actor"},
  {"@id": "http://example.org/persons/marco_merchant", "@type": "cidoc:E39_Actor"},
  {"@id": "http://example.org/persons/judge_antonio", "@type": "cidoc:E39_Actor"}
]
```

**✅ Check 4: Subject under P16**

```json
"cidoc:P16_used_specific_object": [
  {"@id": "http://example.org/buildings/palazzo_spinola", "@type": "cidoc:E1_CRM_Entity"}
]
```

**✅ Check 5: Shortcut properties removed**
No `gmn:P70_18`, `gmn:P70_19`, or `gmn:P70_20` in output

### Step 4.4: Validate JSON Structure

```bash
python3 -m json.tool test_output.json > /dev/null
```

**Expected**: No output (valid JSON)

### Step 4.5: Test Edge Cases

**Test Case 1: Multiple arbitrators**

```json
{
  "@id": "http://example.org/contracts/arb_test_002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator1"},
    {"@id": "http://example.org/persons/arbitrator2"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/debts/debt1"}
  ]
}
```

Transform and verify P14 contains THREE actors (1 party + 2 arbitrators).

**Test Case 2: Multiple subjects**

```json
{
  "@id": "http://example.org/contracts/arb_test_003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator1"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/buildings/building1"},
    {"@id": "http://example.org/debts/debt1"},
    {"@id": "http://example.org/contracts/contract1"}
  ]
}
```

Transform and verify P16 contains THREE entities.

### Step 4.6: CIDOC-CRM Compliance

Verify:

- [ ] E7_Activity is valid CIDOC-CRM class
- [ ] P2_has_type correctly links E7 to E55_Type
- [ ] P14_carried_out_by correctly links E7 to E39_Actor
- [ ] P16_used_specific_object correctly links E7 to E1_CRM_Entity
- [ ] P70_documents correctly links E31 to E7
- [ ] AAT 300417271 is accessible

**Test AAT URI:**

```bash
curl -I http://vocab.getty.edu/page/aat/300417271
```

Should return `HTTP/1.1 200 OK`

✅ **Phase 4 Complete!**

---

## Omeka-S Integration

### Step 5.1: Import Updated Ontology

1. Log into Omeka-S admin
2. Go to "Vocabularies"
3. Find GMN vocabulary
4. Click "Edit" or "Re-import"
5. Upload updated `gmn_ontology.rdf`
6. Confirm import

### Step 5.2: Create Item Template

1. Go to "Resource templates"
2. Click "Add new resource template"
3. Name: "Arbitration Agreement"
4. Add properties:
   - gmn:P1_1_has_name
   - gmn:P94i_2_has_enactment_date
   - gmn:P94i_1_was_created_by
   - gmn:P70_18_documents_disputing_party
   - gmn:P70_19_documents_arbitrator
   - gmn:P70_20_documents_dispute_subject
5. Set class: gmn:E31_3_Arbitration_Agreement
6. Save template

### Step 5.3: Test Data Entry

Create a test item in Omeka-S:

- Use Arbitration Agreement template
- Fill in all fields
- Save
- Export as JSON-LD
- Transform with script
- Verify output

✅ **Omeka-S Integration Complete!**

---

## Advanced Usage and Considerations

### Future Enhancements

Potential additions:

1. **Role Typing**: Add P14.1_in_the_role_of to distinguish parties from arbitrators
2. **Arbitration Award**: Link to resulting decision
3. **Time Duration**: Add deadline properties
4. **Costs**: Add fee properties

### SPARQL Queries

**Find all arbitrations:**

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>

SELECT ?agreement ?name
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement .
  OPTIONAL { ?agreement gmn:P1_1_has_name ?name . }
}
```

**Find arbitrations involving specific person:**

```sparql
PREFIX gmn: <http://www.genoesemerchantnetworks.com/ontology#>
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>

SELECT ?agreement
WHERE {
  ?agreement a gmn:E31_3_Arbitration_Agreement ;
             cidoc:P70_documents ?activity .
  ?activity cidoc:P14_carried_out_by <http://example.org/persons/giovanni> .
}
```

---

## Troubleshooting Guide

### Issue: Multiple E7_Activity nodes created

**Symptoms**: Each property creates its own activity

**Solutions:**

1. Verify all functions check for existing `cidoc:P70_documents`
2. Ensure activity URI is consistently generated
3. Check functions use `existing_activity` variable correctly

### Issue: Shortcut properties not removed

**Symptoms**: Shortcut properties remain in output

**Solutions:**

1. Verify function calls in `transform_item()`
2. Check function names match exactly
3. Ensure functions delete their shortcut properties

### Issue: TypeError during transformation

**Symptoms**: Python error about dictionary key

**Solutions:**

1. Check input JSON structure
2. Verify handling of both URI and object formats
3. Add type checking in functions

### Issue: AAT URI not accessible

**Solutions:**

1. Check internet connection
2. Verify URI spelling
3. Check Getty AAT status

---

## Reference Materials

### Key URIs

**Ontology:**

- Namespace: `http://www.genoesemerchantnetworks.com/ontology#`
- Class: `gmn:E31_3_Arbitration_Agreement`
- P70.18: `gmn:P70_18_documents_disputing_party`
- P70.19: `gmn:P70_19_documents_arbitrator`
- P70.20: `gmn:P70_20_documents_dispute_subject`

**Getty AAT:**

- Arbitration: `http://vocab.getty.edu/page/aat/300417271`

**CIDOC-CRM:**

- E7_Activity: `http://www.cidoc-crm.org/Entity/E7-Activity/`
- P14_carried_out_by: `http://www.cidoc-crm.org/Property/P14-carried-out-by/`
- P16_used_specific_object: `http://www.cidoc-crm.org/Property/P16-used-specific-object/`

### Related Documentation

**In this package:**

- README.md
- arbitration-agreement-documentation.md
- arbitration-agreement-ontology.ttl
- arbitration-agreement-transform.py
- arbitration-agreement-doc-note.txt

**External:**

- CIDOC-CRM: http://www.cidoc-crm.org/
- Getty AAT: http://www.getty.edu/research/tools/vocabularies/aat/

---

## Appendix: Command Reference

### Validation Commands

```bash
# Validate RDF
rapper -i turtle -o turtle gmn_ontology.rdf > /dev/null

# Validate Python
python3 -m py_compile gmn_to_cidoc_transform_script.py

# Validate JSON
python3 -m json.tool test_output.json > /dev/null

# Pretty-print JSON
python3 -m json.tool test_output.json > formatted.json
```

### Backup Commands

```bash
# Create timestamped backup
cp file.ext file.ext.backup-$(date +%Y%m%d-%H%M%S)

# List backups
ls -lh *.backup-*

# Restore from backup
cp file.ext.backup-20251026-143000 file.ext
```

### Transformation Commands

```bash
# Run transformation
python3 gmn_to_cidoc_transform_script.py input.json output.json

# Test multiple files
for file in test_*.json; do
    python3 gmn_to_cidoc_transform_script.py "$file" "output_${file}"
done
```

---

## Final Checklist

Before considering implementation complete:

**Ontology:**

- [ ] RDF validates without errors
- [ ] Class and 3 properties added
- [ ] Version updated to 1.4
- [ ] Backup exists

**Python:**

- [ ] Script compiles without errors
- [ ] Constant and 3 functions added
- [ ] Functions called in transform_item()
- [ ] Test files transform correctly

**Documentation:**

- [ ] Class hierarchy updated
- [ ] Property descriptions added
- [ ] Examples included

**Testing:**

- [ ] Basic test passes
- [ ] Edge cases work
- [ ] CIDOC-CRM compliant
- [ ] AAT URI accessible

---

**End of Implementation Guide**

**Congratulations!** You have successfully implemented Arbitration Agreements in the GMN ontology.

**Version:** 1.0  
**Last Updated:** October 26, 2025  
**Total Implementation Time:** 60-90 minutes

For questions or issues, refer to the troubleshooting section or consult the semantic documentation (arbitration-agreement-documentation.md).
