"""
ASGI config for dJan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

'''
    UPDATE BY Cheng 使用wsgi替换asgi BEGIN 20200421
'''
# from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dJan.settings')

# application = get_asgi_application()
application = get_wsgi_application()
'''
    UPDATE BY Cheng 使用wsgi替换asgi END 20200421
'''