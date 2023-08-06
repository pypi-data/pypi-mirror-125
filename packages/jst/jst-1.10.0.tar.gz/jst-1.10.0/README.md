# jsonschema-transpiler

A tool for transpiling [JSON Schema](https://json-schema.org/) into schemas for
[Avro](https://avro.apache.org/docs/current/index.html#schemas) and
[BigQuery](https://cloud.google.com/bigquery/docs/schemas).

## Installation

```sh
pip install jst
```

## Usage

```py
import json
import jst


json_schema = {
    "items": {
        "properties": {
            "field_1": {"type": "string"},
            "field_2": {"type": "integer"},
        },
        "type": "object",
    },
    "type": "array",
}
bq_schema = json.loads(jst.convert_bq(json.dumps(json_schema)))

assert bq_schema == [
    {
        "fields": [
            {"mode": "NULLABLE", "name": "field_1", "type": "STRING"},
            {"mode": "NULLABLE", "name": "field_2", "type": "INT64"},
        ],
        "mode": "REPEATED",
        "name": "root",
        "type": "RECORD",
    }
]
```
