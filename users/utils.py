def transform_string_to_int(value):
    return int(value) if isinstance(value, str) and value.isdigit() else 0

def is_empty_value(value):
    return value is None or value == ''