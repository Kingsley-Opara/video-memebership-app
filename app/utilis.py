from pydantic import BaseModel, error_wrappers
import json
from app.users.models import User

def validate_schema_or_errors(raw_data:dict, schema_model:BaseModel):
    data = {}
    error_str = None
    errors = []
    password = None
    try:
        cleaned_data = schema_model(**raw_data)
        data = cleaned_data.dict()
        print(data)
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    if error_str is None:
        password = data['password'].get_secret_value()

    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{'loc': 'non_field_error', 'msg': 'Unknown error'}]
    return data, errors, password