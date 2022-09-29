class DataValidationError(Exception):
    ...


class ContentValidation:

    valid_keys = [
        "title",
        "module",
        "students",
        "description",
        "is_active",
    ]

    valid_values = {
        "title": str,
        "module": str,
        "students": int,
        "description": str,
        "is_active": bool,
    }

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        self.data = kwargs
        self.errors = {}

    def is_valid(self) -> bool:
        try:
            self.validate_required_keys()
            self.validate_data_types()
            return True

        except (KeyError, DataValidationError):
            return False

    def validate_required_keys(self):
        for valid_key in self.valid_keys:
            if valid_key not in self.data.keys():
                self.errors[valid_key] = "Missing key"

        if self.errors:
            raise KeyError

    def validate_data_types(self):
        for valid_key, expected_type in self.valid_values.items():
            if type(self.data[valid_key]) is not expected_type:
                error_message = f"Must be a {expected_type.__name__}"
                self.errors[valid_key] = error_message

        if self.errors:
            raise DataValidationError
