import re

def to_snake_case(name):
    """Convert camelCase or PascalCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def transform_querydict_keys(querydict):
    """Transform the keys of a QueryDict to snake_case and handle values properly."""
    transformed_dict = {}
    for key, value in querydict.items():
        snake_case_key = to_snake_case(key)
        
        # If the value is a list (typical for regular fields), get the first item.
        if isinstance(value, list):
            transformed_dict[snake_case_key] = value[0]
        else:
            # Otherwise, it's a file (e.g., InMemoryUploadedFile), so we keep it as is.
            transformed_dict[snake_case_key] = value
    
    return transformed_dict