Base Endpoints
==============

User Create
-----------

Use this endpoint to register new user. Your user model manager should
implement `create_user <https://docs.djangoproject.com/en/dev/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user>`_
method and have `USERNAME_FIELD <https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD>`_
and `REQUIRED_FIELDS <https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS>`_
fields.

**Default URL**: ``auth/users/``


+----------+-----------------------------------+----------------------------------+
| Method   |  Request                          | Response                         |
+==========+===================================+==================================+
| ``POST`` | * ``{{ User.USERNAME_FIELD }}``   | ``HTTP_201_CREATED``             |
|          | * ``{{ User.REQUIRED_FIELDS }}``  |                                  |
|          | * ``password``                    | * ``{{ User.USERNAME_FIELD }}``  |
|          | * ``re_password``                 | * ``{{ User._meta.pk.name }}``   |
|          |                                   | * ``{{ User.REQUIRED_FIELDS }}`` |
|          |                                   |                                  |
|          |                                   | ``HTTP_400_BAD_REQUEST``         |
|          |                                   |                                  |
|          |                                   | * ``{{ User.USERNAME_FIELD }}``  |
|          |                                   | * ``{{ User.REQUIRED_FIELDS }}`` |
|          |                                   | * ``password``                   |
|          |                                   | * ``re_password``                |
+----------+-----------------------------------+----------------------------------+

User Activate
-------------

Use this endpoint to activate user account. This endpoint is not a URL which
will be directly exposed to your users - you should provide site in your
frontend application (configured by ``ACTIVATION_URL``) which will send ``POST``
request to activate endpoint. ``HTTP_403_FORBIDDEN`` will be raised if user is already
active when calling this endpoint (this will happen if you call it more than once).

**Default URL**: ``auth/users/activation/``

+----------+--------------------------------------+----------------------------------+
| Method   | Request                              | Response                         |
+==========+======================================+==================================+
| ``POST`` | * ``uid``                            | ``HTTP_204_NO_CONTENT``          |
|          | * ``token``                          |                                  |
|          |                                      | ``HTTP_400_BAD_REQUEST``         |
|          |                                      |                                  |
|          |                                      | * ``uid``                        |
|          |                                      | * ``token``                      |
|          |                                      |                                  |
|          |                                      | ``HTTP_403_FORBIDDEN``           |
|          |                                      |                                  |
|          |                                      | * ``detail``                     |
+----------+--------------------------------------+----------------------------------+

User Resend Activation E-mail
------------------------------

Use this endpoint to re-send the activation e-mail. Note that no e-mail would
be sent if the user is already active or if they don't have a usable password.
Also if the sending of activation e-mails is disabled in settings, this call
will result in ``HTTP_400_BAD_REQUEST``

**Default URL**: ``auth/users/resend_activation/``

+----------+--------------------------------------+----------------------------------+
| Method   | Request                              | Response                         |
+==========+======================================+==================================+
| ``POST`` | * ``{{ User.EMAIL_FIELD }}``         | ``HTTP_204_NO_CONTENT``          |
|          |                                      | ``HTTP_400_BAD_REQUEST``         |
+----------+--------------------------------------+----------------------------------+

User Info
---------

Use this endpoint to retrieve/update the authenticated user.

**Default URL**: ``auth/users/me/``

+----------+--------------------------------+----------------------------------+
| Method   |           Request              |           Response               |
+==========+================================+==================================+
| ``GET``  |    --                          | ``HTTP_200_OK``                  |
|          |                                |                                  |
|          |                                | * ``{{ User.USERNAME_FIELD }}``  |
|          |                                | * ``{{ User._meta.pk.name }}``   |
|          |                                | * ``{{ User.REQUIRED_FIELDS }}`` |
+----------+--------------------------------+----------------------------------+
| ``PUT``  | ``{{ User.REQUIRED_FIELDS }}`` | ``HTTP_200_OK``                  |
|          |                                |                                  |
|          |                                | * ``{{ User.USERNAME_FIELD }}``  |
|          |                                | * ``{{ User._meta.pk.name }}``   |
|          |                                | * ``{{ User.REQUIRED_FIELDS }}`` |
|          |                                |                                  |
|          |                                | ``HTTP_400_BAD_REQUEST``         |
|          |                                |                                  |
|          |                                | * ``{{ User.REQUIRED_FIELDS }}`` |
+----------+--------------------------------+----------------------------------+
| ``PATCH``| ``{{ User.FIELDS_TO_UPDATE }}``| ``HTTP_200_OK``                  |
|          |                                |                                  |
|          |                                | * ``{{ User.USERNAME_FIELD }}``  |
|          |                                | * ``{{ User._meta.pk.name }}``   |
|          |                                | * ``{{ User.REQUIRED_FIELDS }}`` |
|          |                                |                                  |
|          |                                | ``HTTP_400_BAD_REQUEST``         |
|          |                                |                                  |
|          |                                | * ``{{ User.REQUIRED_FIELDS }}`` |
+----------+--------------------------------+----------------------------------+

User Delete
-----------

Use this endpoint to delete authenticated user. By default it will simply verify
password provided in ``current_password``, delete the auth token if token
based authentication is used and invoke delete for a given ``User`` instance.
One of ways to customize the delete behavior is to override ``User.delete``.

**Default URL**: ``auth/users/me/``

+------------+---------------------------------+----------------------------------+
| Method     |  Request                        | Response                         |
+============+=================================+==================================+
| ``DELETE`` | * ``current_password``          | ``HTTP_204_NO_CONTENT``          |
|            |                                 |                                  |
|            |                                 | ``HTTP_400_BAD_REQUEST``         |
|            |                                 |                                  |
|            |                                 | * ``current_password``           |
+------------+---------------------------------+----------------------------------+

User Login
----------

Use this endpoint to obtain user
`authentication token <http://www.django-rest-framework.org/api-guide/authentication#tokenauthentication>`_.

**Default URL**: ``auth/token/login/``

+----------+----------------------------------+----------------------------------+
| Method   | Request                          | Response                         |
+==========+==================================+==================================+
| ``POST`` | * ``{{ User.USERNAME_FIELD }}``  | ``HTTP_200_OK``                  |
|          | * ``password``                   |                                  |
|          |                                  | * ``auth_token``                 |
+----------+----------------------------------+----------------------------------+

User Logout
-----------

.. note::
    To make this authenticated request below, it is compulsory to add this header 
    ``Authorization: Token auth_token`` (auth_token is retrieved when user login successfully)

Use this endpoint to logout user (remove user authentication token).

**Default URL**: ``auth/token/logout/``

+----------+----------------+----------------------------------+
| Method   |  Request       | Response                         |
+==========+================+==================================+
| ``POST`` | --             | ``HTTP_204_NO_CONTENT``          |
+----------+----------------+----------------------------------+