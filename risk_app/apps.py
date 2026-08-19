from django.apps import AppConfig


class RiskAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'risk_app'

    def ready(self):
        """Warm up the ML model once so prediction requests stay fast."""
        try:
            from risk_app.ml_service import load_model
            load_model()
        except Exception:
            # Keep the app running even if the model is unavailable at startup.
            # The prediction view can still surface a clear error for users.
            pass
