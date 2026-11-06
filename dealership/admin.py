from django.contrib import admin

from .models import (
    Car,
    CarImage,
    CustomCarRequest,
    Review,
)


# ==================================================
# ADMIN BRANDING
# ==================================================

admin.site.site_header = (
    'AUTO CARS GML – Administrare'
)

admin.site.site_title = (
    'AUTO CARS GML'
)

admin.site.index_title = (
    'Panou de administrare'
)


# ==================================================
# CAR IMAGES
# ==================================================

class CarImageInline(admin.TabularInline):

    model = CarImage

    extra = 1


# ==================================================
# CARS
# ==================================================

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'brand',
        'model_name',
        'year',
        'mileage',
        'price',
        'status',
    )

    list_filter = (
        'status',
        'brand',
        'fuel',
        'transmission',
    )

    search_fields = (
        'brand',
        'model_name',
    )

    inlines = [
        CarImageInline
    ]


# ==================================================
# CUSTOM CAR REQUESTS
# ==================================================

@admin.register(CustomCarRequest)
class CustomCarRequestAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'brand',
        'model_name',
        'budget_max',
        'phone',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'fuel',
        'transmission',
        'created_at',
    )

    search_fields = (
        'full_name',
        'phone',
        'email',
        'brand',
        'model_name',
    )

    readonly_fields = (
        'public_id',
        'created_at',
    )


# ==================================================
# REVIEWS
# ==================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'rating',
        'car_model',
        'review_date',
        'approved',
        'created_at',
    )

    list_filter = (
        'approved',
        'rating',
        'review_date',
        'created_at',
    )

    search_fields = (
        'customer_name',
        'car_model',
        'comment',
    )

    readonly_fields = (
        'created_at',
    )

    date_hierarchy = (
        'review_date'
    )