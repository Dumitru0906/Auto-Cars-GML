from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Car


class StaticViewSitemap(Sitemap):

    priority = 0.8

    changefreq = 'weekly'

    def items(self):

        return [
            'home',
            'available_inventory',
            'sold_inventory',
            'reviews',
            'contact',
        ]

    def location(self, item):

        return reverse(item)


class CarSitemap(Sitemap):

    changefreq = 'weekly'

    priority = 0.9

    def items(self):

        return Car.objects.all()

    def location(self, obj):

        return reverse(
            'car_detail',
            args=[obj.pk]
        )