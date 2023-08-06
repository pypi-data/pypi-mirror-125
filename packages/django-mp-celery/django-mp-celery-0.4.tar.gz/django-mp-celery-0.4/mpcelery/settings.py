

class CelerySettings(object):

    CELERY_BROKER_URL = "redis://0.0.0.0:6379/0"

    CELERY_RESULT_BACKEND = 'django_celery_results.backends.DatabaseBackend'

    @property
    def CELERY_TIMEZONE(self):
        return super().TIME_ZONE

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'django_celery_beat',
            'django_celery_results'
        ]


default = CelerySettings
