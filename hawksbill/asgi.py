"""
ASGI config for hawksbillapi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os, sys
from pathlib import Path
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ["DJANGO_SETTINGS_MODULE"] = "hawksbill.settings.local_settings"
django.setup()


from apps.hawksbillapi.urls import websocket_urlpatterns


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(routes=websocket_urlpatterns),
            ),
        ),
    }
)
