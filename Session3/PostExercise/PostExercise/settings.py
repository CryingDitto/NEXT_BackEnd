"""
Django settings for PostExercise project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os, json, datetime
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# secret.json
secret_file = os.path.join(BASE_DIR, 'secrets.json')  # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'postapp',
    'accounts',
    'corsheaders',# corsheaders
    'rest_framework', # drf
    'rest_framework_simplejwt', # jwt
    'rest_framework_simplejwt.token_blacklist', # jwt for logout
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PostExercise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PostExercise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# cors 설정(다른 포트 간의 소통을 위해)
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:5500', 'http://localhost:5500', 'http://localhost:8000']
CORS_ALLOW_CREDENTIALS = True

# drf
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        # authentication is needed
        # 회원가입 여부 체크
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # authorization
        # jwt를 이용하여 인증함
        'rest_framework_simplejwt.authentication.JWTAuthentication', # token을 이용한 인증
        'rest_framework.authentication.SessionAuthentication', # session을 통한 인증
        'rest_framework.authentication.BasicAuthentication',
    )

}


# JWT_AUTH = {
#     # 배포 시에는 django SECRET_KEY가 아닌 다른 값을 이용하길 권장
#     'JWT_SECRET_KEY': SECRET_KEY,
#     # JWT 암호화 알고리즘 종류
#     'JWT_ALGORITHM': 'HS256',
#     # JWT 갱신할 수 있게 할지 여부 설정
#     'JWT_ALLOW_REFRESH': True,
#     # Access Token의 유효기한
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     # Refresh Token의 유효기한
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
# }

# document
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
# https://medium.com/grad4-engineering/how-to-blacklist-json-web-tokens-in-django-43fb88ae3d17
SIMPLE_JWT = {
    # access token 기한
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7), # minutes=5
    # refresh token 기한
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=28),

    # True일 경우 refresh token 보내면 새로운 access token, refresh token 반환함
    # False일 경우 refresh token은 유지하고 access token만 새로 반환함
    'ROTATE_REFRESH_TOKENS': False, 
    # True일 경우 기존 refresh token이 블랙리스트가 됨 (사용 불가하다는 뜻인 듯)
    'BLACKLIST_AFTER_ROTATION': True, 
    'UPDATE_LAST_LOGIN': False,

    # 암호화 알고리즘
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',), # defulat value

    # 'TOKEN_USER_CLASS': 'accounts.User',

}