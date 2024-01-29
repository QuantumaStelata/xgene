from django.conf import settings

from generic.services.requests import RequestService


class PoliroidRequestService(RequestService):
    host_domain = settings.POLIROID_API_HOST
