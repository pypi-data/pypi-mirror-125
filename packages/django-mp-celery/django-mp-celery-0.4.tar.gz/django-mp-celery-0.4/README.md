
### Auto integration of celery and celery beat

Installation:

1)  Add `django-mp-celery` to `requirements.txt`
 

2) Add `celerybeat-schedule` to `.gitignore` file

 
3) Add next code to `core/__init__.py`

``` python
from mpcelery.app import celery_app


__all__ = ['celery_app']


# this code is optional 
celery_app.conf.beat_schedule = {
    {
        'task-name': {
            'task': 'path.to.task_method',
            'schedule': 5  # each 5 seconds
        }
    }
}
```

4) 
IF you have `django-mp-basement` installed
* Add `mpcelery` to `settings_factory` 

else:
* add `django_celery_beat` to `INSTALLED_APPS`
* add `CELERY_BROKER_URL = "redis://0.0.0.0:6379/0"`

Run tasks:
* `celery -A core worker -l INFO`
* `celery -A core beat -l INFO`