from sqlalchemy.inspection import inspect


def filter_valid_fields(
        model,
        data,
        exclude_fields=['id', 'created_at', 'updated_at']
):
    """
    Filter valid fields for the given SQLAlchemy model.
    Args:
        model (db.Model): The SQLAlchemy model class.
        data (dict): The data to filter.
        exclude_fields (list): List of fields to exclude from filtering.
    Returns:
        dict: Filtered data containing only valid columns of the model.
    """

    if not isinstance(data, dict):
        return {}

    model_columns = {
        c.key
        for c in inspect(model).mapper.column_attrs
    }

    return {
        key: value
        for key, value in data.items()
        if key in model_columns and key not in exclude_fields}
