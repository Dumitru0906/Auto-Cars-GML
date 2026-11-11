from django.http import HttpResponse
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dealership.sitemaps import (
    StaticViewSitemap,
    CarSitemap,
)


sitemaps = {
    'static': StaticViewSitemap,
    'cars': CarSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    path(
        'robots.txt',
        lambda request: HttpResponse(
            "User-agent: *\n"
            "Allow: /\n"
            "Sitemap: https://autocarsgml.eu.pythonanywhere.com/sitemap.xml\n",
            content_type="text/plain"
        ),
    ),

    path('', include('dealership.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )