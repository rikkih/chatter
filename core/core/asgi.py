"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chatter import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('SERVER_GATEWAY_INTERFACE', 'Asynchronous')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(routing.websocket_urlpatterns),
})
