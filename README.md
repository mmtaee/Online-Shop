# Django Online Shop
    A Django 3 project / deployment settings with docker 
    online shop with api
    admin pannel for creating items
    anonymous user cart shop >> worked with cookie  
    send email user activation and user forgot password with Celery
    use redis for message broker
    docker for deployment

without docker :

        change settings.py 
                DEBUG = True
                ALLOWED_HOSTS = []
                commit >> STATIC_ROOT = os.path.join(BASE_DIR, "static/")
                uncommit >> STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
                CELERY_BROKER_URL = 'redis://localhost:6379/0'
                database config

with docker :

        >> docker-compose build
        >> docker-compose up -d

        <!-- see celery info -->
        >> sudo docker-compose exec web celery -A online_shop worker -l info

        <!-- create superuser -->
        >> sudo docker-compose run web /usr/local/bin/python manage.py createsuperuser

        <!-- auto migrations and migrate need time to make tables. -->
                <!-- nginx return response 400 during this -->


requirements :

        Django==3.0.5
        django-taggit==1.2.0
        djangorestframework==3.11.0
        Pillow==7.0.0
        pytz==2019.3
        requests==2.23.0
        six==1.14.0
        redis==3.4.1
        celery==4.4.2
        django-celery-results==1.2.1
        docker-compose
        gunicorn
        psycopg2


