# Usage Examples

`site/data/shortages.csv` and `site/data/shortages.json` are public datasets
regenerated daily from the FDA openFDA drug shortages API. Both files are
committed to this repo and served on GitHub Pages.

See [data-schema.md](data-schema.md) for a complete field reference.

## Python — read the CSV

The snippet below fetches the live CSV from GitHub Pages and prints every
record whose status is `Current`.

```python
import csv
import urllib.request

URL = "https://zzddddzz.github.io/rx-shortage-radar/data/shortages.csv"

with urllib.request.urlopen(URL) as response:
    lines = response.read().decode("utf-8").splitlines()

reader = csv.DictReader(lines)
for row in reader:
    if row["status"] == "Current":
        print(row["generic_name"], "|", row["company_name"], "|", row["update_date"])
```

To read from a local copy instead, replace the fetch block with:

```python
with open("shortages.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["status"] == "Current":
            print(row["generic_name"], "|", row["company_name"], "|", row["update_date"])
```

Commonly useful columns: `generic_name`, `status`, `company_name`,
`update_date`, `initial_posting_date`, `dosage_form`, `routes`,
`therapeutic_categories`. The full column list is in
[data-schema.md](data-schema.md).

## JavaScript — read the JSON

The snippet below fetches the live JSON from GitHub Pages and logs the first
five `Current` shortage records.

```js
const URL = "https://zzddddzz.github.io/rx-shortage-radar/data/shortages.json";

fetch(URL)
  .then(res => res.json())
  .then(data => {
    const current = data.records.filter(r => r.status === "Current");
    current.slice(0, 5).forEach(r => {
      console.log(r.generic_name, "|", r.company_name, "|", r.update_date);
    });
  });
```

The top-level JSON object has five keys: `schema_version`, `generated_at`,
`source`, `summary`, and `records`. Each entry in `records` is a shortage
record. Field descriptions are in [data-schema.md](data-schema.md).
