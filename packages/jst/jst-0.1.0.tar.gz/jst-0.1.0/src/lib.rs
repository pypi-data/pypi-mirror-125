use jst::{convert_avro, convert_bigquery, Context, ResolveMethod};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

fn create_context(
    resolve_method: Option<&str>,
    normalize_case: Option<bool>,
    force_nullable: Option<bool>,
    tuple_struct: Option<bool>,
    allow_maps_without_value: Option<bool>,
) -> Context {
    Context {
        resolve_method: match resolve_method {
            None => ResolveMethod::Cast,
            Some("cast") => ResolveMethod::Cast,
            Some("panic") => ResolveMethod::Panic,
            Some("drop") => ResolveMethod::Drop,
            _ => panic!("Unknown resolution method!"),
        },
        normalize_case: normalize_case.unwrap_or(false),
        force_nullable: force_nullable.unwrap_or(false),
        tuple_struct: tuple_struct.unwrap_or(false),
        allow_maps_without_value: allow_maps_without_value.unwrap_or(false),
    }
}

#[pymodule]
fn jst(_py: Python, m: &PyModule) -> PyResult<()> {
    /// convert_bq(s, resolve_method=None, normalize_case=None, force_nullable=None, tuple_struct=None, allow_maps_without_value=None)
    /// --
    /// Convert json schema to bigquery schema
    ///
    /// Args:
    ///     - s (str): json schema.
    ///     - resolve_method (Optional[str]): The resolution strategy for incompatible or under-specified schema.
    ///         Possible values are "cast", "panic", "drop", None(default)
    ///         If None, fallback to "cast"
    ///     - normalize_case(Optional[bool]): snake_case column-names for consistent behavior between SQL engines.
    ///     - force_nullable(Optional[bool]): Treats all columns as NULLABLE, ignoring the required section in the JSON Schema.
    ///     - tuple_struct(Optional[bool]): Treats tuple validation as an anonymous struct.
    ///     - allow_maps_without_value(Optional[bool]): Produces maps without a value field for incompatible or under-specified value schema.
    ///
    #[pyfn(m, name = "convert_bq")]
    fn py_convert_bq(
        _py: Python,
        s: &str,
        resolve_method: Option<&str>,
        normalize_case: Option<bool>,
        force_nullable: Option<bool>,
        tuple_struct: Option<bool>,
        allow_maps_without_value: Option<bool>,
    ) -> PyResult<String> {
        let context = create_context(
            resolve_method,
            normalize_case,
            force_nullable,
            tuple_struct,
            allow_maps_without_value,
        );

        let value = serde_json::from_str(s).unwrap();
        let result = convert_bigquery(&value, context).to_string();
        Ok(result)
    }

    /// convert_avro(s, resolve_method=None, normalize_case=None, force_nullable=None, tuple_struct=None, allow_maps_without_value=None)
    /// --
    /// Convert json schema to avro schema
    ///
    /// Args:
    ///     - s (str): json schema.
    ///     - resolve_method (Optional[str]): The resolution strategy for incompatible or under-specified schema.
    ///         Possible values are "cast", "panic", "drop", None(default)
    ///         If None, fallback to "cast"
    ///     - normalize_case(Optional[bool]): snake_case column-names for consistent behavior between SQL engines.
    ///     - force_nullable(Optional[bool]): Treats all columns as NULLABLE, ignoring the required section in the JSON Schema.
    ///     - tuple_struct(Optional[bool]): Treats tuple validation as an anonymous struct.
    ///     - allow_maps_without_value(Optional[bool]): Produces maps without a value field for incompatible or under-specified value schema.
    ///
    #[pyfn(m, name = "convert_avro")]
    fn py_convert_avro(
        _py: Python,
        s: &str,
        resolve_method: Option<&str>,
        normalize_case: Option<bool>,
        force_nullable: Option<bool>,
        tuple_struct: Option<bool>,
        allow_maps_without_value: Option<bool>,
    ) -> PyResult<String> {
        let context = create_context(
            resolve_method,
            normalize_case,
            force_nullable,
            tuple_struct,
            allow_maps_without_value,
        );
        let value = serde_json::from_str(s).unwrap();
        let result = convert_avro(&value, context).to_string();
        Ok(result)
    }
    Ok(())
}
