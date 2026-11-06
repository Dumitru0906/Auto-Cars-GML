from urllib.parse import quote

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import (
    CustomCarRequestForm,
    ReviewForm,
)

from .models import (
    Car,
    CustomCarRequest,
    Review,
)


WHATSAPP_NUMBER = '40757337253'


# ==================================================
# HOME
# ==================================================

def home(request):

    # Default forms
    home_find_car_form = CustomCarRequestForm()
    home_review_form = ReviewForm()

    # ----------------------------------------------
    # CUSTOM CAR REQUEST FROM HOMEPAGE
    # ----------------------------------------------

    if (
        request.method == 'POST'
        and request.POST.get('form_type') == 'find_car'
    ):

        home_find_car_form = CustomCarRequestForm(
            request.POST
        )

        if home_find_car_form.is_valid():

            car_request = (
                home_find_car_form.save()
            )

            whatsapp_url = (
                build_custom_request_whatsapp_url(
                    car_request
                )
            )

            return redirect(
                whatsapp_url
            )


    # ----------------------------------------------
    # REVIEW FROM HOMEPAGE
    # ----------------------------------------------

    elif (
        request.method == 'POST'
        and request.POST.get('form_type') == 'review'
    ):

        home_review_form = ReviewForm(
            request.POST
        )

        if home_review_form.is_valid():

            review = home_review_form.save(
                commit=False
            )

            review.approved = False

            review.save()

            return redirect(
                '/?review_submitted=1#recenzii'
            )


    # ----------------------------------------------
    # CARS
    # ----------------------------------------------

    available_cars = (
        Car.objects
        .filter(status='available')
        .prefetch_related('images')
    )

    reserved_cars = (
        Car.objects
        .filter(status='reserved')
        .prefetch_related('images')
    )

    sold_cars = (
        Car.objects
        .filter(status='sold')
        .prefetch_related('images')
    )


    # ----------------------------------------------
    # REVIEWS
    # ----------------------------------------------

    approved_reviews = (
        Review.objects
        .filter(approved=True)
    )

    review_submitted = (
        request.GET.get('review_submitted')
        == '1'
    )


    return render(
        request,
        'dealership/home.html',
        {
            'available_cars': available_cars,
            'reserved_cars': reserved_cars,
            'sold_cars': sold_cars,

            'approved_reviews':
                approved_reviews,

            'home_find_car_form':
                home_find_car_form,

            'home_review_form':
                home_review_form,

            'review_submitted':
                review_submitted,
        }
    )


# ==================================================
# OLD INVENTORY OVERVIEW
# ==================================================

def inventory(request):

    available_cars = (
        Car.objects
        .filter(status='available')
        .prefetch_related('images')
    )

    reserved_cars = (
        Car.objects
        .filter(status='reserved')
        .prefetch_related('images')
    )

    sold_cars = (
        Car.objects
        .filter(status='sold')
        .prefetch_related('images')
    )

    return render(
        request,
        'dealership/inventory.html',
        {
            'available_cars': available_cars,
            'reserved_cars': reserved_cars,
            'sold_cars': sold_cars,
        }
    )


# ==================================================
# STATUS-SPECIFIC LISTINGS
# ==================================================

def _status_inventory(
    request,
    status,
    page_title,
    hero_title,
    hero_intro,
    section_label,
    empty_title,
    empty_text,
):

    cars = (
        Car.objects
        .filter(status=status)
        .prefetch_related('images')
    )

    return render(
        request,
        'dealership/inventory_status.html',
        {
            'cars': cars,
            'status_key': status,
            'page_title': page_title,
            'hero_title': hero_title,
            'hero_intro': hero_intro,
            'section_label': section_label,
            'empty_title': empty_title,
            'empty_text': empty_text,
        }
    )


def available_inventory(request):

    return _status_inventory(
        request=request,
        status='available',
        page_title=(
            'Mașini disponibile | Auto Cars GML'
        ),
        hero_title='Mașini disponibile',
        hero_intro=(
            'Descoperă toate mașinile disponibile '
            'în prezent la Auto Cars GML.'
        ),
        section_label='STOC ACTUAL',
        empty_title=(
            'Momentan nu există mașini disponibile.'
        ),
        empty_text=(
            'Revino în curând pentru a vedea '
            'noile mașini adăugate în stoc.'
        ),
    )


def reserved_inventory(request):

    return _status_inventory(
        request=request,
        status='reserved',
        page_title=(
            'Mașini rezervate | Auto Cars GML'
        ),
        hero_title='Mașini rezervate',
        hero_intro=(
            'Aceste mașini sunt momentan rezervate '
            'și se află în curs de vânzare.'
        ),
        section_label='ÎN CURS DE VÂNZARE',
        empty_title=(
            'Momentan nu există mașini rezervate.'
        ),
        empty_text=(
            'Mașinile rezervate vor apărea aici '
            'atunci când există rezervări active.'
        ),
    )


def sold_inventory(request):

    return _status_inventory(
        request=request,
        status='sold',
        page_title=(
            'Mașini vândute | Auto Cars GML'
        ),
        hero_title='Mașini vândute',
        hero_intro=(
            'Vezi mașinile vândute anterior '
            'prin Auto Cars GML.'
        ),
        section_label='ISTORIC AUTO CARS GML',
        empty_title=(
            'Momentan nu există mașini '
            'vândute afișate.'
        ),
        empty_text=(
            'Mașinile vândute vor fi '
            'afișate aici.'
        ),
    )


# ==================================================
# CAR DETAIL
# ==================================================

def car_detail(request, pk):

    car = get_object_or_404(
        Car.objects.prefetch_related(
            'images'
        ),
        pk=pk
    )

    return render(
        request,
        'dealership/car_detail.html',
        {
            'car': car
        }
    )


# ==================================================
# WHATSAPP CUSTOM REQUEST
# ==================================================

def build_custom_request_whatsapp_url(
    car_request
):

    lines = [
        'Bună ziua!',
        '',
        (
            'Doresc să fac o cerere pentru '
            'găsirea unei mașini prin '
            'Auto Cars GML.'
        ),
        '',
        '--- DATE CLIENT ---',
        f'Nume: {car_request.full_name}',
        f'Telefon: {car_request.phone}',
    ]

    if car_request.email:

        lines.append(
            f'Email: {car_request.email}'
        )

    lines.extend([
        '',
        '--- MAȘINA CĂUTATĂ ---',

        f'Marcă: {car_request.brand}',

        (
            f'Model: '
            f'{car_request.model_name or "Oricare"}'
        ),

        (
            f'Buget maxim: '
            f'{car_request.budget_max} €'
        ),

        (
            'An minim: '
            + (
                str(car_request.year_min)
                if car_request.year_min
                else 'Nespecificat'
            )
        ),

        (
            'Combustibil: '
            + car_request.get_fuel_display()
        ),

        (
            'Cutie de viteze: '
            + car_request.get_transmission_display()
        ),

        (
            'Kilometraj maxim: '
            + (
                f'{car_request.max_mileage} km'
                if (
                    car_request.max_mileage
                    is not None
                )
                else 'Nespecificat'
            )
        ),
    ])

    if car_request.notes:

        lines.extend([
            '',
            '--- ALTE PREFERINȚE ---',
            car_request.notes,
        ])

    lines.extend([
        '',
        (
            'Aștept să discutăm despre '
            'opțiunile disponibile. '
            'Mulțumesc!'
        )
    ])

    message = '\n'.join(lines)

    return (
        f'https://wa.me/'
        f'{WHATSAPP_NUMBER}'
        f'?text={quote(message)}'
    )


# ==================================================
# FIND CAR PAGE
# ==================================================

def find_car(request):

    if request.method == 'POST':

        form = CustomCarRequestForm(
            request.POST
        )

        if form.is_valid():

            car_request = form.save()

            whatsapp_url = (
                build_custom_request_whatsapp_url(
                    car_request
                )
            )

            return redirect(
                whatsapp_url
            )

    else:

        form = CustomCarRequestForm()

    return render(
        request,
        'dealership/find_car.html',
        {
            'form': form
        }
    )


def find_car_success(
    request,
    public_id
):

    car_request = get_object_or_404(
        CustomCarRequest,
        public_id=public_id
    )

    whatsapp_url = (
        build_custom_request_whatsapp_url(
            car_request
        )
    )

    return render(
        request,
        'dealership/find_car_success.html',
        {
            'car_request':
                car_request,

            'whatsapp_url':
                whatsapp_url,
        }
    )


# ==================================================
# REVIEWS PAGE
# ==================================================

def reviews(request):

    if request.method == 'POST':

        review_form = ReviewForm(
            request.POST
        )

        if review_form.is_valid():

            review = review_form.save(
                commit=False
            )

            review.approved = False

            review.save()

            return redirect(
                '/recenzii/?submitted=1'
            )

    else:

        review_form = ReviewForm()

    approved_reviews = (
        Review.objects
        .filter(approved=True)
    )

    submitted = (
        request.GET.get('submitted')
        == '1'
    )

    return render(
        request,
        'dealership/reviews.html',
        {
            'reviews':
                approved_reviews,

            'review_form':
                review_form,

            'submitted':
                submitted,
        }
    )


# ==================================================
# CONTACT PAGE
# ==================================================

def contact(request):

    return render(
        request,
        'dealership/contact.html'
    )