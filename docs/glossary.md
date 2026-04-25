# Glossary

This glossary explains common terms used in Rx Shortage Radar. It is written for software users and contributors, not as medical guidance.

## NDC

**NDC** means National Drug Code. In this project, NDC values identify listed drug products or packages as reported through FDA/openFDA source data. Package NDCs usually point to a specific package presentation, while product NDCs identify the product portion of an NDC.

Official references:

- FDA National Drug Code Directory: https://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm
- FDA NDC database background: https://www.fda.gov/drugs/development-approval-process-drugs/national-drug-code-database-background-information

## RxCUI

**RxCUI** means RxNorm Concept Unique Identifier. In this project, `rxcuis` are public RxNorm identifiers returned by openFDA where available. They are useful for grouping or matching drug concepts across systems, but they do not replace local formulary or clinical review.

Official reference:

- NLM RxNorm technical documentation: https://www.nlm.nih.gov/research/umls/rxnorm/docs/techdoc.html

## RxNorm

**RxNorm** is the National Library of Medicine drug terminology used to normalize medication names and concepts. Rx Shortage Radar uses the public RxNorm approximate-term API to help turn misspelled or free-text searches into normalized medication candidates.

Official references:

- NLM RxNorm overview: https://www.nlm.nih.gov/research/umls/rxnorm/
- NLM RxNorm APIs: https://lhncbc.nlm.nih.gov/RxNav/APIs/RxNormAPIs.html

## openFDA

**openFDA** is FDA's public API platform for accessing FDA datasets. Rx Shortage Radar uses the openFDA drug shortages endpoint to build the dashboard JSON, CSV, and RSS outputs.

Official references:

- openFDA overview: https://www.fda.gov/science-research/health-informatics-fda/openfda
- openFDA drug shortages endpoint: https://open.fda.gov/apis/drug/drugshortages/

## Current

**Current** is an FDA shortage status value in this dataset. Rx Shortage Radar treats it as an active shortage record from the public openFDA feed.

Official reference:

- FDA drug shortages FAQ: https://www.fda.gov/drugs/drug-shortages/frequently-asked-questions-about-drug-shortages

## Resolved

**Resolved** is an FDA shortage status value in this dataset. Rx Shortage Radar treats it as a shortage record that FDA/openFDA reports as resolved.

Official reference:

- openFDA drug shortages endpoint: https://open.fda.gov/apis/drug/drugshortages/

## To Be Discontinued

**To Be Discontinued** is an FDA shortage status value in this dataset. Rx Shortage Radar treats it as a public FDA/openFDA record indicating the product is expected to be discontinued or is in a discontinuation path.

Official reference:

- openFDA drug shortages searchable fields: https://open.fda.gov/apis/drug/drugshortages/searchable-fields/

## Public-Safety Note

Rx Shortage Radar is for public data exploration. It does not make medical, clinical, procurement, reimbursement, or patient-care decisions. Confirm all shortage information with authoritative FDA sources, manufacturers, pharmacists, prescribers, and local policies.

