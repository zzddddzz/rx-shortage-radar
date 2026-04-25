# Shortages Dataset Schema

The `site/data/shortages.json` dataset powers the Rx Shortage Radar application. This dataset is automatically generated and regularly updated using public openFDA Drug Shortages data.

## Root Structure

| Field | Type | Description |
| :--- | :--- | :--- |
| `generated_at` | `string` | ISO 8601 timestamp indicating when the dataset was fetched and generated. |
| `records` | `array` | A list of drug shortage record objects. |

## Record Object (`records`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `string` | Unique identifier for the specific shortage record. |
| `generic_name` | `string` | The generic name of the drug. |
| `brand_names` | `array of strings` | Associated brand names for the drug. |
| `company_name` | `string` | Name of the manufacturing or distributing company. |
| `status` | `string` | The current status of the shortage (e.g., "Current", "Resolved", "To Be Discontinued"). |
| `presentation` | `string` | Description of the drug presentation, usually including strength and primary NDC. |
| `dosage_form` | `string` | The dosage form of the drug (e.g., "Tablet", "Injection", "Solution"). |
| `routes` | `array of strings` | Routes of administration (e.g., "ORAL", "INTRAVENOUS"). |
| `substances` | `array of strings` | Active ingredients or substances in the drug. |
| `therapeutic_categories` | `array of strings` | The therapeutic or pharmacological categories the drug belongs to. |
| `initial_posting_date` | `string` | Date the shortage was initially posted (YYYY-MM-DD). |
| `update_date` | `string` | Date the record was last updated by the FDA (YYYY-MM-DD). |
| `update_type` | `string` | The type of update that occurred (e.g., "Reverified", "Revised", "New"). |
| `discontinued_date` | `string` \| `null` | Date the drug was discontinued (YYYY-MM-DD), if applicable. |
| `related_info` | `string` | Additional notes from the manufacturer or FDA regarding the shortage, recovery estimates, or allocation details. |
| `package_ndc` | `string` | The primary package National Drug Code (NDC) associated with the record. |
| `package_ndcs` | `array of strings` | A comprehensive list of all associated package NDCs. |
| `product_ndcs` | `array of strings` | A comprehensive list of all associated product-level NDCs. |
| `rxcuis` | `array of strings` | RxNorm Concept Unique Identifiers (RxCUIs) associated with the drug. |
| `search_text` | `string` | A concatenated string of various fields, stripped of special characters, optimized for client-side full-text search. |
| `source_url` | `string` | URL pointing back to the openFDA JSON source. |