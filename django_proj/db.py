# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'studentsdb',
        # 'USER': 'studentsdb',
        # 'PASSWORD': 'studentsdb',
        'USER': 'postgres',
        'PASSWORD': '12345qwert',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
            'CHARSET': 'utf8',
        }
    }
}