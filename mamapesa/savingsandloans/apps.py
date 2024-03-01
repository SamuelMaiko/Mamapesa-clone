from django.apps import AppConfig


class SavingsandloansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'savingsandloans'
<<<<<<< HEAD
    
    def ready(self):
        from . import signals
=======
>>>>>>> 0c36e251c83e59b77eda538877d8700f0296849d
