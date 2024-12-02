"""
utility functions for the selection app 
"""

def generate_choices(min_value: int, max_value: int, label_template: str) -> list:
    """
    Generate a list of dictionaries for choices with custom labels, values, and IDs.

    Args:
        min_value (int): Minimum value for the range.
        max_value (int): Maximum value for the range.
        label_template (str): Template string for labels with a placeholder {value}.

    Returns:
        list: A list of dictionaries with label, value, and ID.
    """
    return [
        {
            "id": idx,
            "label": label_template.format(value=value),
            "value": value,
        }
        for idx, value in enumerate(range(min_value, max_value + 1), start=1)
    ]



