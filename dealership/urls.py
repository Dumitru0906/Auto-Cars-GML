from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    # ==================================================
    # CAR LISTINGS
    # ==================================================

    path(
        'masini/',
        views.inventory,
        name='inventory'
    ),

    path(
        'masini/disponibile/',
        views.available_inventory,
        name='available_inventory'
    ),

    path(
        'masini/rezervate/',
        views.reserved_inventory,
        name='reserved_inventory'
    ),

    path(
        'masini/vandute/',
        views.sold_inventory,
        name='sold_inventory'
    ),

    # ==================================================
    # CAR DETAIL
    # ==================================================

    path(
        'masini/<int:pk>/',
        views.car_detail,
        name='car_detail'
    ),

    # ==================================================
    # FIND CAR
    # ==================================================

    path(
        'gaseste-mi-o-masina/',
        views.find_car,
        name='find_car'
    ),

    path(
        'gaseste-mi-o-masina/multumim/<uuid:public_id>/',
        views.find_car_success,
        name='find_car_success'
    ),

    # ==================================================
    # REVIEWS
    # ==================================================

    path(
        'recenzii/',
        views.reviews,
        name='reviews'
    ),

    # ==================================================
    # CONTACT
    # ==================================================

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

]