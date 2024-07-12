from django.core.exceptions import ValidationError


class CustomerNameValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if not all(char.isalpha() or char.isspace() for char in value):
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            'main_app.validators.CustomerNameValidator',
            (self.message, ),
            {}
        )


class CustomerPhoneValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if not (value.startswith('+359') and len(value) == 13 and value[4:].isdigit()):
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            'main_app.validators.CustomerPhoneValidator',
            (self.message, ),
            {}
        )


# def validate_customer_email(value):
#     try:
#         EmailValidator()(value)
#     except ValidationError:
#         raise ValidationError("Enter a valid email address")


# def validate_customer_website_url(value):
#     try:
#         URLValidator()(value)
#     except ValidationError:
#         raise ValidationError("Enter a valid URL")


# class CustomerEmailValidator(EmailValidator):
#     def __call__(self, value):
#         try:
#             super().__call__(value)
#         except ValidationError:
#             raise ValidationError("Enter a valid email address")
#
#
# class CustomerURLValidator(URLValidator):
#     def __call__(self, value):
#         try:
#             super().__call__(value)
#         except ValidationError:
#             raise ValidationError("Enter a valid URL")
