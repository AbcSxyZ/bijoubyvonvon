from django.conf import settings


def template_settings(request):
    return {
            'matomo_url': settings.MATOMO_DOMAIN_PATH,
            }
