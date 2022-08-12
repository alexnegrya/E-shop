def get_model_fields(model) -> tuple[str]: return tuple([field.split('|')[0] for field in model.FIELDS])


def validate_model_attrs(model, **attrs):
    fields = get_model_fields(model)
    data = {field: model.TEST_VALUES[i] for i, field in enumerate(fields)}
    data.update(attrs)
    data.pop(fields[0])
    model(**data)
