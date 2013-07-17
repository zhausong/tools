DATABASE_ENGINE = 'appengine'
DEBUG = True
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.admin',
        'mysite.blog', 'appengine_django')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'mysite.urls'  ###
SECRET_KEY = '%ri0=0*@ss^ba((b5wf$0-_so3@^*ix0(37a9w4*xz&i4pzia_'
SERIALIZATION_MODULES = {'xml': 'appengine_django.serializer.xml'}  ###
SETTINGS_MODULE = 'settings'  ###
SITE_ID = 1  ###
TEMPLATE_DEBUG = True
TIME_ZONE = 'America/Los_Angeles'
