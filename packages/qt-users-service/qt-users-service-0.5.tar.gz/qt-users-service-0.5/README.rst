================
qt-users-service
================

qt-users-service is a Django app to authenticate users against a microservice.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "qt-users-service" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'qt-users-service',
    ]

2. Include the following to the settings.py::

    AUTH_USER_MODEL = "qt-users-service.User"
    AUTH_USER_TABLE = "users_user"
    AUTH_DB = "users_db"

3. Run ``python manage.py migrate``.

4. Start the development server and visit an API.

5. Try to get details from that API with a JWT-token.