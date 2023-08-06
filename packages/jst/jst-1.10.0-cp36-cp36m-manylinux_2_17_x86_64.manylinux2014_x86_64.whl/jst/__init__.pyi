from typing import Optional

def convert_bq(
    s: str,
    resolve_method: Optional[str] = None,
    normalize_case: Optional[bool] = None,
    force_nullable: Optional[bool] = None,
    tuple_struct: Optional[bool] = None,
    allow_maps_without_value: Optional[bool] = None,
): ...
def convert_avro(
    s: str,
    resolve_method: Optional[str] = None,
    normalize_case: Optional[bool] = None,
    force_nullable: Optional[bool] = None,
    tuple_struct: Optional[bool] = None,
    allow_maps_without_value: Optional[bool] = None,
): ...
