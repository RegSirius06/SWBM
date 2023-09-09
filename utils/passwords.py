from django.contrib.auth.password_validation import validate_password

def is_valid_password(password):
    try:
        validate_password(password)
    except Exception as e:
        return e
    return True