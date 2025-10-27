# GMN Ontology

The **Genoese Merchant Networks (GMN) CIDOC-CRM Extension Ontology** is a specialized vocabulary designed to model historical data from medieval and early modern Genoese merchant networks. This ontology extends the CIDOC Conceptual Reference Model (CIDOC-CRM) with simplified shortcut properties and classes tailored for use in the Omeka-S platform.

## Overview

The GMN ontology addresses the challenge of modeling complex historical relationships in systems like Omeka-S, which don't handle deeply nested data structures well. It provides direct, simplified properties that represent more complex CIDOC-CRM paths while maintaining semantic compatibility with the underlying standard.

**Version:** 1.5  
**Created by:** Steven Teasdale  
**Last Modified:** October 25, 2025

## Key Features

- **CIDOC-CRM Extension:** Built on top of the CIDOC-CRM standard, ensuring interoperability with other cultural heritage data
- **Simplified Properties:** Shortcut properties that flatten complex CIDOC-CRM paths for easier data entry and management
- **Specialized Classes:** Custom classes for merchant network entities including:
  - Buildings and moveable property
  - Contract types (sales, arbitration, cessions, correspondence, declarations, dowries, donations, etc.)
  - Social and professional groups
  - Family relationships
- **Omeka-S Optimized:** Designed specifically for platforms that require simpler data structures

## Documentation Structure

Detailed documentation for the ontology is organized in the following directories:

- **`classes/`** - Complete documentation for all ontology classes
- **`properties/`** - Complete documentation for all ontology properties  
- **`transformations/`** - Python scripts for transforming GMN shortcut properties to full CIDOC-CRM structures

## Use Cases

This ontology is designed to model:

- Notarial contracts and legal documents from medieval/early modern archives
- Property ownership and transfers (real estate and moveable goods)
- Social and familial relationships between merchants
- Professional networks and group affiliations
- Commercial transactions and business activities
- Legal processes including arbitration and dispute resolution

## Getting Started

The ontology is defined in RDF/Turtle format in `gmn_ontology.ttl`. To use this ontology:

1. Import the ontology into your RDF triple store or semantic web application
2. Reference the GMN namespace: `http://www.genoesemerchantnetworks.com/ontology#`
3. Use the simplified properties for data entry in Omeka-S or similar platforms
4. Apply the transformation scripts (in `transformations/`) to convert to full CIDOC-CRM when needed

## Namespace

```
@prefix gmn: <http://www.genoesemerchantnetworks.com/ontology#> .
```

## Contact

Steven Teasdale
https://orcid.org/0000-0003-1822-6246

---

For questions about specific classes and properties, please refer to the documentation in the `classes/` and `properties/` directories.
