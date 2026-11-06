import uuid

from django.db import models
from django.utils import timezone


class Car(models.Model):

    STATUS_CHOICES = [
        ('available', 'Disponibilă'),
        ('reserved', 'Rezervată'),
        ('sold', 'Vândută'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Benzină'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hibrid'),
        ('electric', 'Electrică'),
        ('lpg', 'GPL'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Manuală'),
        ('automatic', 'Automată'),
    ]

    brand = models.CharField(
        max_length=50,
        verbose_name='Marcă'
    )

    model_name = models.CharField(
        max_length=100,
        verbose_name='Model'
    )

    year = models.PositiveIntegerField(
        verbose_name='An'
    )

    mileage = models.PositiveIntegerField(
        verbose_name='Kilometraj'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name='Preț'
    )

    fuel = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        verbose_name='Combustibil'
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        verbose_name='Cutie de viteze'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Descriere'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Status'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.brand} {self.model_name}"

    @property
    def main_image(self):

        main = self.images.filter(
            is_main=True
        ).first()

        return main or self.images.first()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mașină'
        verbose_name_plural = 'Mașini'


class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='cars/',
        verbose_name='Fotografie'
    )

    is_main = models.BooleanField(
        default=False,
        verbose_name='Fotografie principală'
    )

    def __str__(self):
        return f"Imagine - {self.car}"


class CustomCarRequest(models.Model):

    STATUS_CHOICES = [
        ('new', 'Nouă'),
        ('contacted', 'Contactat'),
        ('closed', 'Închisă'),
    ]

    FUEL_CHOICES = [
        ('any', 'Oricare'),
        ('petrol', 'Benzină'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hibrid'),
        ('electric', 'Electrică'),
        ('lpg', 'GPL'),
    ]

    TRANSMISSION_CHOICES = [
        ('any', 'Oricare'),
        ('manual', 'Manuală'),
        ('automatic', 'Automată'),
    ]

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    full_name = models.CharField(
        max_length=100,
        verbose_name='Nume'
    )

    phone = models.CharField(
        max_length=30,
        verbose_name='Telefon'
    )

    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )

    brand = models.CharField(
        max_length=50,
        verbose_name='Marcă dorită'
    )

    model_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Model dorit'
    )

    budget_max = models.PositiveIntegerField(
        verbose_name='Buget maxim (€)'
    )

    year_min = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='An minim'
    )

    fuel = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        default='any',
        verbose_name='Combustibil'
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default='any',
        verbose_name='Cutie de viteze'
    )

    max_mileage = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Kilometraj maxim'
    )

    notes = models.TextField(
        blank=True,
        verbose_name='Alte preferințe'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Status cerere'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data cererii'
    )

    def __str__(self):

        vehicle = self.brand

        if self.model_name:
            vehicle += f" {self.model_name}"

        return f"{self.full_name} - {vehicle}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cerere mașină'
        verbose_name_plural = 'Cereri mașini'


class Review(models.Model):

    RATING_CHOICES = [
        (5, '5 stele'),
        (4, '4 stele'),
        (3, '3 stele'),
        (2, '2 stele'),
        (1, '1 stea'),
    ]

    customer_name = models.CharField(
        max_length=100,
        verbose_name='Nume client'
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name='Evaluare'
    )

    car_model = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Mașină cumpărată'
    )

    comment = models.TextField(
        verbose_name='Recenzie'
    )

    approved = models.BooleanField(
        default=False,
        verbose_name='Aprobată'
    )

    review_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data originală a recenziei'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data adăugării în sistem'
    )

    def save(self, *args, **kwargs):

        if self.review_date is None:

            if self.created_at:

                created = self.created_at

                if timezone.is_aware(created):
                    created = timezone.localtime(created)

                self.review_date = created.date()

            else:

                self.review_date = timezone.localdate()

        super().save(
            *args,
            **kwargs
        )

    def __str__(self):

        return (
            f"{self.customer_name} - "
            f"{self.rating}/5"
        )

    class Meta:
        ordering = [
            '-review_date',
            '-created_at',
        ]

        verbose_name = 'Recenzie'
        verbose_name_plural = 'Recenzii'