from django.conf import settings


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {
        'DOMAIN_NAME': settings.DOMAIN_NAME,
        'SITE_URL': settings.SITE_URL,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_HEADER': settings.SITE_HEADER,
        'INDEX_TITLE': settings.INDEX_TITLE,
        'IP': request.META.get(
            'REMOTE_ADDR'
        ),  # これで取得できたIPをINTERNAL_IPSに追加する
    }


# def metadata(request):
#     """
#     Add some generally useful metadata to the template context
#     """
#     return {'shop_name': settings.OSCAR_SHOP_NAME,
#             'shop_tagline': settings.OSCAR_SHOP_TAGLINE,
#             'homepage_url': settings.OSCAR_HOMEPAGE,
#             'language_neutral_url_path': strip_language_code(request),
#             # Fallback to old settings name for backwards compatibility
#             'google_analytics_id': (getattr(settings, 'OSCAR_GOOGLE_ANALYTICS_ID', None)
#                                     or getattr(settings, 'GOOGLE_ANALYTICS_ID', None))}
