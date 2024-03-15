from django.contrib.auth import get_user_model
from django.core.management.commands import createsuperuser
from django.core.exceptions import ValidationError

class Command(createsuperuser.Command):
    help = 'Create a superuser.'

    def handle(self, *args, **options):
        username_field = get_user_model().USERNAME_FIELD
        phone_number = None

        # Prompt for phone number
        while phone_number is None:
            phone_number = input("Phone number: ")
            try:
                get_user_model()._default_manager.get(**{username_field: phone_number})
            except get_user_model().DoesNotExist:
                pass
            else:
                self.stderr.write("Error: That phone number is already taken.")
                phone_number = None

        # Set username to phone number
        options['username'] = phone_number

        # Call the original createsuperuser command
        return super().handle(*args, **options)
