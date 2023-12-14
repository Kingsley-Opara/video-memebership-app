from email_validator import validate_email, EmailNotValidError

def _validate_email(email):
    is_valid = False
    msg = ''
    validated_email = ''
    try:
        valid_email = validate_email(email, check_deliverability=True)
        validated_email = valid_email.normalized
        is_valid = True
    except EmailNotValidError as e:
        msg = e
    return is_valid, msg, validated_email

