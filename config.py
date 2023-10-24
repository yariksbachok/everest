from datetime import timedelta


#redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create in-memory database
DATABASE_FILE = 'root:root@localhost/everest'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE_FILE

# Flask-Security config
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
# URLs
SECURITY_URL_PREFIX = "/admin"
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"



# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False


CELERY_CONFIG = {"broker_url": f"redis://{REDIS_HOST}:{REDIS_PORT}", "result_backend": f"redis://{REDIS_HOST}:{REDIS_PORT}", "broker_connection_retry_on_startup": True,
                 "beat_schedule" : {
                        'track-database-changes': {
                            'task': 'tasks.chek_status_order',
                            'schedule': timedelta(seconds=10)
                        }
}
}
#celery -A app.celery worker --pool=solo -l info
#celery -A app.celery beat -l info
#admin@admin.com adminadmin
